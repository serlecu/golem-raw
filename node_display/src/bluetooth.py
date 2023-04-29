import time
import threading
import asyncio

import bluetooth as bt
import simplepyble as ble

import bless
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions
    )
import logging
from typing import Any

from bleak import BleakScanner
from typing import Sequence

import src.globals as g
from src.globals import *

# simpleBLe Client vars
BTAdapter: ble.Adapter #type: ignore
devicesChecked: bool = False
connectingDevices = []
matchedDevices = []

TARGET_SERVICE = 'A07498CA-AD5B-474E-940D-16F1FBE7E8CD'

# BLESS server vars
server: BlessServer
trigger: threading.Event = threading.Event()
notifyChar: BlessGATTCharacteristic

SERVICE_UUID:str = 'A07498CA-AD5B-474E-940D-16F1FBE7E8CD'
CHARACTERISTIC_UUID:str = '51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B'



# simpleBLE - Client
def setupBTAdapter():
    global BTAdapter, server_sock
    print("Initializing Bluetooth...")
    
    # ====== simpleBLE - Client ======
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

    # ====== BLESS - Server =======
    # ~ loop = asyncio.get_event_loop()
    # ~ loop.run_until_complete(initServerAsync(loop))
    

# BLESS
async def initServerAsync(loop):
    global trigger, server
    
    print("BLESS: Setting up BLE Server...")
    
    gatt:Dict = {
        SERVICE_UUID: {
            CHARACTERISTIC_UUID:{
                "Properties": GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(g.nodeID+"00").encode()
            },
        }
    }
    
    # ~ trigger.clear()
    
    serviceName = "Iron Ore Golem " + g.nodeID
    
    server = BlessServer(name=serviceName, name_overwrite=True, loop=loop)
    # ~ server.read_request_func = onReadRequest
    # ~ server.write_request_function = onWriteRequest
    
    # --- without gatt ---
    try:
        await server.add_new_service(SERVICE_UUID)
    except Exception as e:
        print(f"BLESS: Error adding Service: {e}")
    else:
        print(f"BLESS: service added {SERVICE_UUID}")
        
    try:
        await server.add_new_characteristic( SERVICE_UUID,
                                   CHARACTERISTIC_UUID,
                                   ( GATTCharacteristicProperties.read |
                                     GATTCharacteristicProperties.write |
                                     GATTCharacteristicProperties.notify ),
                                    str(g.nodeID+"00").encode(),
                                   ( GATTAttributePermissions.readable |
                                     GATTAttributePermissions.writeable ) )
    except Exception as e:
        print(f"BLESS: Error adding characteristic: {e}")
    else:
        print(f"BLESS: characteristic added {CHARACTERISTIC_UUID}")
        
        notifyChar = server.get_characteristic(CHARACTERISTIC_UUID)
        print(notifyChar)
        
    # ~ print("BLESS: Starting BLE server...")
    # ~ try:
        # ~ g.runningBLEserver = await server.start()
    # ~ except:
        # ~ print("BLESS: Error on advertising services")
        # ~ return False
    # ~ else:
        # ~ g.runningBLEserver = True
        # ~ print("BLESS: Advertising.")
        
        # ~ bless_thread = threading.Thread(target=runBlessListener(), daemon=True)
        # ~ bless_thread.start()
    # ~ print("BLESS: async done")
    await server.start()
    
    # --- With gatt ---
    # ~ await server.add_gatt(gatt)
    # ~ await server.start()
    
    if await server.is_advertising():
        print("BLESS: server up and running!")
    else:
        print("BLESS ERROR: server not advertising")

# BLESS        
def runBlessListener():
    global trigger, server
    
    while g.runningBLEserver:
        try:
            print("BLESS: waiting requests.")
            trigger.wait()
            trigger.clear()
            print("BLESS: back to listen.")
        except Exception as e:
            print(f"BLESS listener Error: {e}.")
        
    print("BLESS: end server")
    loop.close()
    server.stop()
    
                                   
# BLESS
def onReadRequest_Other(conn_handle: int, attr_handle: int, value: bytes):
    print(f"BLESS: received {value}")

def onReadRequest( char: BlessGATTCharacteristic,
                   **kwargs
                   ) -> bytearray:
    global logger
    
    logger.debug(f"BLESS: Reading {characteristic.value}")
    return char.value

def onWriteRequest( char: BlessGATTCharacteristic,
                    value: Any,
                   **kwargs ):
    global logger, trigger
    
    print(f"BLESS: Write request - {char} -> {value}")
    
    
    char.value = value
    logger.debug(f"Char value set to { char.value}")
    if char.value == b'\x0f':
        logger.debug("NICE")
        trigger.set()


# simpleBLE - Client
def scanBT():
    # ~ BTAdapter.scan_for(4000)
    
    asyncio.run(scanBTbleak())
    
    
# BLEAK
async def scanBTbleak():
    #_onScanStart
    g.isScanning = True
    print("Scan started")
    
    scanner = BleakScanner() #service_uuids=[TARGET_SERVICE])
    await scanner.start()
    await asyncio.sleep(4.0)
    await scanner.stop()
    time.sleep(0.1)
    g.foundDevicesBleak = scanner.discovered_devices
    print(f"Found {len(scanner.discovered_devices)} devices")
    
    #_onScanStop
    global devicesChecked
    print("Scan complete")
    for device in g.foundDevicesBleak :
        print(f"{device.name} {device.address}")
    devicesChecked = False
    g.isScanning = False
    
# simpleBLE - Client
def onScanStart():
    print("Scanning ...")
    g.isScanning = True
    
# simpleBLE - Client    
def onScanStop():
    global devicesChecked
    print("Scan complete")
    g.foundDevices = BTAdapter.scan_get_results()
    devicesChecked = False
    g.isScanning = False
    
    
# simpleBLE - Client   
def onDeviceFound(device):
    print(f"Found device [{device.identifier()}] [{device.address}].")
    filterDevice(device, TARGET_SERVICE)


# simpleBLE - Client  
def filterDevice(device, targetService):
    global matchedDevices
    
    if device.is_connectable():
        services = device.services()
        for service in services:
            if service.uuid() == targetService:
                print("Found GOLEM service")
                if (device in matchedDevices):
                    print(f"Device [{device.identifier()}] already stored.")
                else:
                    print(f"Match [{device.identifier()}].")
                    matchedDevices.append(device)
                break


# ========= HANDLE CONNECTIONS ===========

def handleBTConnections():
    global BTAdapter, devicesChecked, connectingDevices, matchedDevices
    
#     print("Handling connections")
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
    
                
# NOT USING - WHAT IS THIS??
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


# simpleBLE - client
def onConnectedDevice(device):
    print(f"Connection success {device.identifier()} [{device.address()}]")
    try:
        notifyToChars(device, getServiceCharPairs(device, TARGET_SERVICE))
    except Exception as e:
        print(f"simpleBLE: Error on notify: {e}")
        
    connectingDevices.remove(device)
    
    
# simpleBLE - client
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
    
    
# simpleBLE - client    
def onDisconnectedDevice(device):
    print(f"simpleBLE: Device {device.identifier()} [{device.address()}] disconnected")
    if device in g.matchedDevices:
        g.matchedDevices.remove(device)
    if device in connectingDevices:
        connectingDevices.remove(device)
   
   
# simpleBLE - client
def notifyToChars(device, serviceCharPairs):
    if len(serviceCharPairs) > 0:
        print(f"Enabling notifications for {device.address()}...")
        for service, char in serviceCharPairs:
            if service == TARGET_SERVICE and char == CHARACTERISTIC_UUID:
                try:
                    device.notify(service, char, lambda data, d=device: onCharacNotified(data, d.address()) )
                except:
                    print(f"Failed to enable notifications for char[{char}] in service[{service}].")
                    print(f"Will try again to subscribe to device {device.address()} ...")
                    g.failedNotifications.append( (device, service, char) )        

        print(f"... end enabling notifications for {device.address()}.")
        
        
# simpleBLE - client
def onCharacNotified(data, deviceAddress):
    print(f"Recieved msg from {deviceAddress}: {data}")
    g.syncState = True


# BLESS - server
def handleBTData():
    global server

    if g.endSwitchCounter > 1:
        print("BLESS: notify endSwitch")
        try:
            notify(server, g.nodeID+"01" )
        except Exception as e:
            print(f"BLESS ERROR: couldn't get characteristic. {e}")
        else:
            g.endSwitchCounter = 0

            
def notify(server, value:str):
    server.get_characteristic(CHARACTERISTIC_UUID,).value = value.encode() 
    server.update_value(SERVICE_UUID, CHARACTERISTIC_UUID)
        
