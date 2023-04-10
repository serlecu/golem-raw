import time
import threading
import struct
import simplepyble as ble

import src.globals as g
from src.globals import *

BTAdapter: ble.Adapter #type: ignore
devicesChecked = False
connectingDevices = []
notifiedCharList = []

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
      BTAdapter.set_callback_on_scan_found(lambda peripheral: filterDevice(peripheral, TARGET_UUID) )
      isAdapterSet = True


def scanBT():
    global BTAdapter
    BTAdapter.scan_for(4000)                        
    # g.foundDevices = BTAdapter.scan_get_results()   #type: ignore


def filterDevices(devices, TARGET_UUID):
    for device in devices:
      filterDevice(device, TARGET_UUID)


def filterDevice(device, TARGET_UUID):
    if device.is_connectable():
      print(f"Found: {device.identifier()} [{device.address()}]")
      services = device.services()
      for service in services:
          if service.uuid() == TARGET_UUID:
              print(f"Matching target service {service.uuid()}")
              if (device not in g.matchedDevices):
                print(f"Device {device.identifier()} [{device.address()}] not in matched devices.")
                g.matchedDevices.append(device)
              else:
                print(f"Device {device.identifier()} already stored.")
          else:
              print(f"Service not matching target")


def handleBTConnections(frequecy = 3000):
    pass
    global BTAdapter, devicesChecked, connectingDevices
    if( not BTAdapter.scan_is_active() ): 
      if( not devicesChecked ):
        for device in g.matchedDevices:
            if not device.is_connected():
              #connectBT(device)
              if not device in connectingDevices:
                connectingDevices.append(device)
                connect_thread = threading.Thread(target=lambda: connectBT(device), daemon=True)
                connect_thread.start()
              else:
                print(f"Device {device.identifier()} [{device.address()}] already connecting.")
            else:
              print(f"Device {device.identifier()} [{device.address()}] already connected.")
        devicesChecked = True
            

def handleBTData(): # miss
    pass


def connectBT(device):
    global connectingDevices
    print("Connecting to {}".format(device.address()))
    device.set_callback_on_connected(lambda: onConnectedDevice(device) )
    device.set_callback_on_disconnected(lambda: onDisconnectedDevice(device) )
    try:
      device.connect()
    except:
      print("Failed to connect to {}".format(device.address()))
    finally:
      connectingDevices.remove(device)


def onScanStart():
    print("Scan started.")
    g.isScanning = True

def onScanStop():
    global devicesChecked, BTAdapter
    print("Scan complete.")
    # filterDevices(BTAdapter.scan_get_results(), g.targetUUID)
    devicesChecked = False
    g.isScanning = False


def onConnectedDevice(device):
    print(f"Connected to {device.address()}.")
    notifyToChars(device, getServiceCharPairs(device))
    # g.matchedDevices.append(device)
    g.sensorDataList.append( VainaSensorNode(device.address(), device.identifier()) )
    

def onDisconnectedDevice(device):
    print(f"Disconnected from {device.address()}.")
    g.matchedDevices.remove(device)
    for sensorData in g.sensorDataList:
      if sensorData.deviceUUID == device.address():
        g.sensorDataList.remove(sensorData)
        break


def onCharacNotified(data, uuid, deviceAddres): #! .deviceUUID is actually the MAC address
    # ----------------------------------------
    # print(f"Received from [{deviceAddres}]: {uuid}")
    # print(f"  {data} => {parseBTData(data)}")
    # for sensorData in g.sensorDataList:
    #   if sensorData.deviceUUID == deviceAddres:
    #     lastValue = sensorData.getSensorDataByUUID(uuid)
    #     sensorData.updateSensorDataFromUUID(uuid, parseBTData(data))
    #     # Check:
    #     print(f"Updated {sensorData.deviceUUID}. {lastValue} => {sensorData.getSensorDataByUUID(uuid)}.")
    #     break
    # ----------------------------------------
    # Using the folowing chunck because we cannot retrieve UUID of the notified characteristic
    # if data is not an empty bytearray
    
    if data != b'\x00':
      parsedData = parseBTData(data)
      deviceUUID = extractSensorUUID(parsedData)
      characUUID = extractCharacUUID(parsedData)
      characValue = extractCHaracValue(parsedData)
      print(f"Received from [{deviceUUID}]: {characUUID}")
      for sensorData in g.sensorDataList:
        # breakpoint()
        if sensorData.deviceUUID == deviceAddres:
          sensorData.updateSensorDataFromUUID(characUUID, characValue)
          # Check:
          print(f"Updated {sensorData.deviceUUID}.")
          break
  

def getServiceCharPairs(device, serviceUUID = None):
    serviceCharsPairs = []
    services = device.services()
    for service in services:
        print (f"Service: {service.uuid()}")
        if serviceUUID == None: 
          chars = service.characteristics()
          for char in chars:
              print (f"Characteristic: {char.uuid()}")
              serviceCharsPairs.append((service.uuid(), char.uuid()))
        else:
          if service.uuid() == serviceUUID:
            chars = service.characteristics()
            for char in chars:
                serviceCharsPairs.append((service.uuid(), char.uuid()))
    return serviceCharsPairs


def notifyToChars(device, serviceCharsPairs):
    if len(serviceCharsPairs) > 0:
      print("Enabling notifications ...")
      for service, char in serviceCharsPairs:
          device.notify(service, char, lambda data: onCharacNotified(data, char, device.address()) ) #! Atention to char to be a UUID
          # https://simpleble.readthedocs.io/en/latest/simpleble/api.html#_CPPv4N9SimpleBLE4Safe10Peripheral6notifyERK13BluetoothUUIDRK13BluetoothUUIDNSt8functionIFv9ByteArrayEEE
          print(f"Notifications enabled for {char} in {service}.")
          # notifiedCharList.append(content)


def extractSensorUUID(data): # UUID: 19b1XXXX
    uuid = '19b1000' + data[0] + '-e8f2-537e-4f6c-d104768a1214'
    return uuid


def extractCharacUUID(data):
    uuid = '19b100' + data[1] + data[2] + '-e8f2-537e-4f6c-d104768a1214'
    return uuid


def extractCHaracValue(data):
    return data[3:]


# Transform raw bytes received from the device into int, float, etc.
def parseBTData(inData: bytearray):
    data_type, outData = detect_data_type(inData)
    # print(f"Raw: {inData} => {outData} | {data_type}")
    print(f"{outData} | {data_type}")
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