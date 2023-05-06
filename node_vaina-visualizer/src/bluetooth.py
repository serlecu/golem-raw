import time
import threading
import asyncio
import struct
import simplepyble as ble

import src.globals as g
from src.globals import *

BTAdapter: ble.Adapter #type: ignore
devicesChecked = False
retryinNotifications = False
connectingDevices = []

def setupBTAdapter():
  global BTAdapter
  print("Initializing Bluetooth...")

  isAdapterSet = False
  while not isAdapterSet:
      adapters = ble.Adapter.get_adapters() #type: ignore
      if len(adapters) == 0:
          print("No adapters found")
          time.sleep(2)
      else:
          for adapter in adapters:
              print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")

          BTAdapter = adapters[0] # I take the first adapter IDKW                   
          BTAdapter.set_callback_on_scan_start( lambda: onScanStart() )      
          BTAdapter.set_callback_on_scan_stop( lambda: onScanStop() )
          # This can be a source of problems when connecting, let's check
          # BTAdapter.set_callback_on_scan_found(lambda peripheral: filterDevice(peripheral, TARGET_UUID) )
          isAdapterSet = True


def scanBT():
    global BTAdapter
    BTAdapter.scan_for(3000)


def onScanStart():
    print("Scan started...")
    g.isScanning = True


def onScanStop():
    global devicesChecked, BTAdapter
    print("Scan complete.")
    filterDevices(BTAdapter.scan_get_results(), TARGET_UUID)
    devicesChecked = False
    g.isScanning = False


def filterDevices(devices, targetUUID):
    global devicesChecked

    # filter devices
    for device in devices:
        filterDevice(device, targetUUID)
    
    # check for duplicates
    for device in g.matchedDevices:
        if g.matchedDevices.count(device) > 1:
            g.matchedDevices.remove(device)
            print(f"Removed duplicate {device.identifier()} [{device.address()}].")


def filterDevice(device, targetUUID):
    if device.is_connectable():
        try:
            services = device.services()
        except Exception as e:
            print(f"Error: {e}")
        else:
            for service in services:
                if service.uuid() == targetUUID:
                    # print(f"Matching target service {service.uuid()}")
                    if not device.is_connected():
                        if not (device in g.matchedDevices):
                            print(f"New matched {device.identifier()} [{device.address()}].")
                            g.matchedDevices.append(device)
                        else:
                            print(f"Device {device.identifier()} already stored.")
                        break
                else:
                    print(f"Service not matching target")



# =================== handleBTConnections() ===================                     

def handleBTConnections(frequecy = 3000):
    global BTAdapter, devicesChecked, connectingDevices, retryinNotifications
    if( not BTAdapter.scan_is_active() ):

        # Establish Connections
        if( not devicesChecked ):
            for device in g.matchedDevices:
                if not device.is_connected():
                    if device.is_connectable():
                        if device not in connectingDevices:
                            connectingDevices.append(device)
                            connect_thread = threading.Thread(target=lambda d=device: connectBT(d), daemon=True)
                            connect_thread.start()
                        else:
                            print(f" - Device {device.identifier()} [{device.address()}] already connecting.")
                    else:
                        print(f"Device {device.identifier()} not connectable")
                        g.matchedDevices.remove(device)
                else:
                    print(f" - Device {device.identifier()} [{device.address()}] already connected.")
            devicesChecked = True

        # Retry Notifications
        if( len(g.failedNotifications) > 0 ):
            if ( connectingDevices == [] ):
                if( not retryinNotifications ):
                    retryNotification_thread = threading.Thread(target=retryNotificationSubscription, daemon=True)
                    retryNotification_thread.start()
                    retryinNotifications = True


def connectBT(device):
    global connectingDevices
    print(f"Connecting to {device.address()}...")
    device.set_callback_on_connected(lambda: onConnectedDevice(device) )
    device.set_callback_on_disconnected(lambda: onDisconnectedDevice(device) )
    time.sleep(0.5)
    try:
        device.connect()
    except Exception as e:
        device.disconnect()
        if device in connectingDevices:
            connectingDevices.remove(device)
        print(f" - Failed to connect to {device.identifier()}. Error: {e}")


def retryNotificationSubscription():
    global retryinNotifications

    for device, service, char in g.failedNotifications:
                if device.is_connected():
                    print(f"Retry failed notifications of {device.identifier()} [{device.address()}]...")
                    try:
                        asyncio.run( device.notify(service, char, lambda data, d=device: onCharacNotified(data, d.address()) ) )
                        # device.notify(service, char, lambda data, d=device: onCharacNotified(data, d.address()) )
                    except:
                        print(f" - Failed to subscribe {char} in {device.identifier()} [{device.address()}]")
                    else:
                        g.failedNotifications.remove((device, service, char))
                    time.sleep(1)
    retryinNotifications = False


def notifyToChars(device, serviceCharsPairs):
    if len(serviceCharsPairs) > 0:
        print(f"Enabling notifications for {device.identifier()} ...")
        index = 0
        for service, char in serviceCharsPairs:
            try:
                device.notify(service, char, lambda data, d=device: onCharacNotified(data, d.address()) )
                # device.notify(service, char, lambda data, d=device: onCharacNotified(data, d.address()) )
                # https://simpleble.readthedocs.io/en/latest/simpleble/api.html#_CPPv4N9SimpleBLE4Safe10Peripheral6notifyERK13BluetoothUUIDRK13BluetoothUUIDNSt8functionIFv9ByteArrayEEE
            except Exception as e:
                print(f" - [{index}] Failed to enable notifications for char[{char}] in service[{service}] - {device.identifier()} - Will try later.")
                print(f" - {e}. {device.identifier()}")
                g.failedNotifications.append((device, service, char))
            else:
                print(f" - [{index}] Notifications enabled for char[{char}] of {device.identifier()}.")
            index += 1
            time.sleep(0.5)
        print("... end of notifications enabling.")


def onConnectedDevice(device):
    print(f"Connected to {device.address()}.")
    g.sensorDataList.append( VainaSensorNode(device.address(), device.identifier()) )
    pairsList = getServiceCharPairs(device)
    notifyToChars(device, pairsList)
    connectingDevices.remove(device)
    
def onDisconnectedDevice(device):
    print(f"Disconnected from {device.address()}.")
    # Remove device from matched list (will find again)
    if device in g.matchedDevices:
        g.matchedDevices.remove(device)
    # Cancel liked notificate retry    
    for failedNotification in g.failedNotifications:
        if failedNotification[0] == device:
            g.failedNotifications.remove(failedNotification)
    # Remove linked sensor object
    for sensorData in g.sensorDataList:
        if sensorData.deviceUUID == device.address():
            g.sensorDataList.remove(sensorData)
    # 
    # if device in connectingDevices:
    #     connectingDevices.remove(device)
    # Unsubscribe from notifications
    # for service in device.services():
    #     for char in service.characteristics():
    #         try:
    #             device.unsubscribe(service, char)
    #         except Exception as e:
    #             print(f" - Failed to unsubscribe from {device.identifier()}")
    #         else:
    #             print(f"Unsubscribed from {device.identifier()} [{device.address()}]")


def onCharacNotified(data, deviceAddres): #! sensorData.deviceUUID == MAC address
    if data != b'\x00':
        parsedData = parseBTData(data)
        #deviceUUID = extractSensorUUID(parsedData) #service UUID
        characUUID = extractCharacUUID(parsedData)
        characValue = extractCharacValue(parsedData)
        # print(f"Received from [{deviceAddres}]: {characUUID}")
        for sensorData in g.sensorDataList:
            if sensorData.deviceUUID == deviceAddres:
                sensorData.updateSensorDataFromUUID(characUUID, characValue)
                # Check:
                #print(f"Updated {sensorData.deviceUUID}.")
                break
  

def getServiceCharPairs(device, serviceUUID = None):
    serviceCharsPairs = []
    services = device.services()
    for service in services:
        #print (f"Service: {service.uuid()}")
        if serviceUUID == None: 
            chars = service.characteristics()
            for char in chars:
                #print (f"Characteristic: {char.uuid()}")
                serviceCharsPairs.append((service.uuid(), char.uuid()))
        else:
            if service.uuid() == serviceUUID:
                chars = service.characteristics()
                for char in chars:
                    serviceCharsPairs.append((service.uuid(), char.uuid()))
    return serviceCharsPairs


def extractSensorUUID(data): # UUID: 19b1XXXX
    uuid = '19b1000' + data[0] + '-e8f2-537e-4f6c-d104768a1214'
    return uuid


def extractCharacUUID(data):
    uuid = '19b100' + data[1] + data[2] + '-e8f2-537e-4f6c-d104768a1214'
    return uuid


def extractCharacValue(data):
    return data[3:]


# Transform raw bytes received from the device into int, float, etc.
def parseBTData(inData: bytearray):
    data_type, outData = detect_data_type(inData)
    # print(f"Raw: {inData} => {outData} | {data_type}")
    # print(f"{outData} | {data_type}")
    return outData


def detect_data_type(byteArray):
    try:
        # Try unpacking as int
        int_value = struct.unpack('i', byteArray)[0]
        return "int", int_value
    except struct.error:
        pass

    try:
        # Try unpacking as float
        float_value = struct.unpack('f', byteArray)[0]
        return "float", float_value
    except struct.error:
        pass

    try:
        # Try decoding as string
        string_value = byteArray.decode()
        string_value.rstrip('\x00')
        # print(f"Raw: {byteArray}. Decoded: {string_value}")
        return "string", string_value
    except UnicodeDecodeError:
        pass

    # If none of the above formats work, return "unknown"
    return "unknown", None


def printCharacteristics( device ):
    services = device.services()
    if len(services) == 0:
        print("No services found")
    else:
        for service in services:
            print(f"Service: {service.uuid()}")
            characts = service.characteristics()
            if len(characts) == 0:
                print("No characteristics found")
            for characteristic in service.characteristics():
                print(f" - Char: {characteristic.uuid()}")
               

def handleBTData(): # miss
    pass