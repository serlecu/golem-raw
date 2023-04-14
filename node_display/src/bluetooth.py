import time
import threading

import bluetooth as bt
import simplepyble as ble

import bless
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions)
import logging
from typing import Any

import src.globals as g
from src.globals import *

BTAdapter: ble.Adapter #type: ignore
devicesChecked: bool = False
connectingDevices = []
matchedDevices = []

logger: logging.Logger
trigger: threading.Event


TARGET_SERVICE = "94f39d29-7d6d-437d-973b-fba39e49d4ee" # "19B10100-E8F2-537E-D104768A1214"

# Define UUIDs for the service and characteristic
# SERVICE_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
SERVICE_UUID = "19B10100-E8F2-537E-D104768A1214"
CHARACTERISTIC_UUID = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"# '19b10000-e8f2-537e-d104768a1214'


def setupBTAdapter():
    global BTAdapter, server_sock
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
        BTAdapter.set_callback_on_scan_start(lambda: onScanStart() )
        BTAdapter.set_callback_on_scan_stop(lambda: onScanStop() )
        BTAdapter.set_callback_on_scan_found(lambda peripheral: onDeviceFound(peripheral))
        isAdapterSet = True

    # ====== PYBLUEZ2 - SERVER =======
    global logger, trigger
    
    print("Starting BLESS ...")
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name=__name__)
    trigger = threading.Event()
    
    initServer()
    
#     server_port = server_sock.getsockname()[1]
#     server_name = "GOLEM_NODE_" + ':'.join(server_sock.getsockname()[0].split(":")[2:])
#     print(f"{server_name}")
#     service_uuid = SERVICE_UUID
#     g.deviceInfo = server_sock.getsockname()
#     
#     advertiseBT( server_sock, server_name, service_uuid )
    
def initServer():
    global trigger, logger
    
    trigger.clear()
    print("Setting up BLE Server...")
    serviceName = "Golem Screen"
    server = BlessServer(name=serviceName)
    server.read_request_func = onReadRequest
    server.write_request_function = onWriteRequest
    
    server.add_new_service(SERVICE_UUID)
    server.add_new_characteristic( SERVICE_UUID,
                                   CHARACTERISTIC_UUID,
                                   ( GATTCharacteristicProperties.read |
                                     GATTCharacteristicProperties.write |
                                     GATTCharacteristicProperties.notify ),
                                    None,
                                   ( GATTAttributePermissions.readable |
                                     GATTAttributePermissions.writeable ) )
#     logger.debug( server.get_characteristic( CHARACTERISTIC_UUID ) )
    
    print("Advertising BLE server...")
    try:
        server.start()
    except:
        print("Error on advertising services")
    else:
        print("Advertising...")
                                   

def onReadRequest( char: BlessGATTCharacteristic,
                   **kwargs
                   ) -> bytearray:
    global logger
    
    logger.debug(f"Reading {characteristic.value}")
    return char.value

def onWriteRequest( char: BlessGATTCharacteristic,
                    value: Any,
                   **kwargs ):
    global logger, trigger
    
    char.value = value
    logger.debug(f"Char value set to { char.value}")
    if char.value == b'\x0f':
        logger.debug("NICE")
        trigger.set()


def scanBT():
    BTAdapter.scan_for(4000)
    
    
def onScanStart():
    print("Scanning ...")
    g.isScanning = True
    
    
def onScanStop():
    global devicesChecked
    print("Scan complete")
    g.foundDevices = BTAdapter.scan_get_results()
    devicesChecked = False
    g.isScanning = False
    
    
def onDeviceFound(device):
    print(f"Found device [{device.identifier()}] [{device.address}].")
    filterDevice(device, TARGET_SERVICE)

def onDeviceFoundOther(device):
    customUUID = "4A98xxxx-1CC4-E7C1-C757-F1267DD021E8"
    print(f"Found: {device.identifier()} [{device.address()}]")
    if device.is_connectable():
        services = device.services()
        for service in services:
            for characteristic in service.characteristics():
                if service.uuid() == customUUID:
                    print("Found GOLEM service")
                    connectBT(device)
                    break


def filterDevice(device, targetService):
    global matchedDevices
    
    if device.is_connectable():
        services = device.services()
        for service in services:
            if service.uuid() == targetService:
                if (device in matchedDevices):
                    print(f"Device [{device.identifier()}] already stored.")
                else:
                    print(f"Match [{device.identifier()}].")
                    matchedDevices.append(device)
                break


# ========= HANDLE CONNECTIONS ===========

def handleBTConnections():
    global BTAdapter, devicesChecked, connectingDevices, matchedDevices
    
    print("Handling connections")
    if (not BTAdapter.scan_is_active()):
        if (not devicesChecked):
            for device in matchedDevices:
                if device.is_connected():
                    print(f"Device [{device.address()}] already connected.")
                else:
                    if device not in connectingDevices:
                        connectingDevices.append(device)
                        connect_thread = threading.Thread(target=lambda d=device: connectBT(d), daemon=True)
                        connect_thread.start()
                    else:
                        print(f"Already connecting to device [{device.address()}].")
    
                

def handleClient(client, address):
    reqBytes = b'' + client.recv(1024)
    
    if not reqBytes:
        print(f"Connection with {client} closed")
        client.close()
    reqString = reqBytes.decode()
    print(f"Received: {reqString}")

def connectBT(device):
    global connectingDevices, matchedDevices
    print(f"Connecting to {device.address()} ...")
    device.set_callbeck_on_connected(lambda d=device: onConnectedDevice(d) )
    device.set_callbeck_on_connected(lambda d=device: onDisconnectedDevice(d) )
    try:
        device.connect()
    except:
        print(f"Failed to connect to {device.address()}")
        if device in matchedDevices:
            matchedDevices.remove(device)
        if device in connectingDevices:
            connectingDevices.remove(device)


def onConnectedDevice(device):
    print(f"Connection success {device.address()}")
    notifyToChars(device, getServiceCharPairs(device, TARGET_SERVICE))
    #g.sensorDataList.append( VainaSensorNode(device.address(), device.identifier()) )
    connectingDevices.remove(device)
    
    
def onDisconnectedDevice(device):
    print("Device {device.address()} disconnected")
    if device in g.matchedDevices:
        g.matchedDevices.remove(device)
    if device in connectingDevices:
        connectingDevices.remove(device)
#     for sensorData in g.sensorDataList:
#         if sensorData.deviceUUID == deviceaddress():
#             g.sensorDataList.remov(sensorData)
#             break
   

def notifyToChars(device, serviceCharPairs):
    if len(serviceCharPairs) > 0:
        print(f"Enabling notifications for {device.address()}...")
        for service, char in serviceCharPairs:
            try:
                device.notify(service, char, lambda data, d=device: onCharacNotified(data, d.address()) )
            except:
                print(f"Failed to enable notifications for char[{char}] in service[{service}].")
#                 print(f"Try again to subscribe to device {device.address()} ...")
#                 notifyToChars(device,ServicePairs)   #! This is dangerous!!
                device.disconnect()
        print(f"... end enabling notifications for {device.address()}.")
        

def onCharacNotified(data, deviceAddress):
    print(f"Recieved msg from {deviceAddress}: {data}")


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


def advertService(address):
    pass
    #from bluetooth import BluetoothSocket
    #BTServer = BluetoothSocket( bt.Protocols.RFCOMM )
    #BTServer.bind(("", bt.PORT_ANY))
    # BTServer.listen(1)

    # # Define the GATT server and characteristic
    # gatt_server = bt.GATTServer()
    # characteristic = bt.Characteristic(CHARACTERISTIC_UUID, ["read", "write"], value)

    # # Define the service and add the characteristic to it
    # service = bt.Service(SERVICE_UUID, [characteristic])

    # # Add the service to the GATT server
    # gatt_server.add_service(service)


def handleBTData():
    pass
