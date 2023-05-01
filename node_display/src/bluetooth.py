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

from bleak import BleakScanner, BleakClient

from typing import Sequence

import src.globals as g

# General BLE flags and arrays
devicesChecked: bool = False
connectingDevices = []
matchedDevices = []

# BLEAK scanner vars
scanner: BleakScanner
TARGET_SERVICE:str = 'A07498CA-AD5B-474E-940D-16F1FBE7E8CD'

# BLESS server vars
serverName: str
server: BlessServer
trigger: threading.Event = threading.Event()
notifyChar: BlessGATTCharacteristic

SERVICE_UUID:str = 'A07498CA-AD5B-474E-940D-16F1FBE7E8CD'
CHARACTERISTIC_UUID:str = '51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B'


# BLEAK (BLE client) manages deviceDiscovery, connections and subscription
# BLESS (BLE server) manages advertising and notification of characteristics


# simpleBLE - Client
def setupBTAdapter():
    global scanner
    print("Initializing Bluetooth...")
    
    scanner = BleakScanner()
    
    g.setupBleak = True


# BLEAK in-betweener
def scanBT():
    global scanner
    asyncio.run(scanBTbleak(scanner))
    
# BLEAK
async def scanBTbleak(scanner):
    global devicesChecked
    #_onScanStart
    g.isScanning = True
    print("BLEAK: Scan started")
    
    await scanner.start()
    await asyncio.sleep(4.0)
    await scanner.stop()
    time.sleep(0.1)
    
    g.foundDevicesBleak = scanner.discovered_devices
    
    #_onScanStop
    print("BLEAK: Scan complete")
    
    # filter devices
    print("BLEAK: Filtering Found Devices...")
    for device in g.foundDevicesBleak :
        filterDevice(device, TARGET_SERVICE)
    print("BLEAK: ...end filtering Found Devices.")
    
    devicesChecked = False
    g.isScanning = False
    
                
# BLEAK 
def filterDevice(device, targetService):
    global matchedDevices, serverName
    
    if "Ore_GOLEM_" in device.name and device.name is not serverName:
        if (device in matchedDevices):
            print(f"BLEAK alert: Device [{device.identifier()}] already stored.")
        else:
            print(f"BLEAK: Match [{device.identifier()}].")
            matchedDevices.append(device)


# ========= HANDLE CONNECTIONS ===========
                    
# BLEAK
def handleBTConnections():
    global devicesChecked, matchedDevices, connectingDevices 
    
#     print("Handling connections")
    if (not g.isScanning) and (not devicesChecked):
            for device in matchedDevices:
                if (not device.is_connected()) and (device not in connectingDevices):
                        connectingDevices.append(device)
                        # ~ connect_thread = threading.Thread(target=lambda d=device: connectBleak(d), daemon=True)
                        connect_thread = threading.Thread(target=lambda d=device: handleClientBleak(d), daemon=True)
                        connect_thread.start()
                #! Problably i'll also need to check if paired
                else:
                    print(f"BLEAK alert: Device [{device.address()}] already connecting or connected.")
    
    
# BLEAK - dirty async inside thread    
def handleClientBleak(device):
    asyncio.run(connectBleak(device))
    

# BLEAK
async def connectBleak(device):
    global connectingDevices, matchedDevices
    print(f"BLEAK: Connecting to {device.address()} ...")
    
    try:
        await device.connect()
    except Exception as e:
        print(f"BLEAK ERROR: Failed to connect to {device.address()}. {e}")
        if device in matchedDevices:
            matchedDevices.remove(device)
        if device in connectingDevices:
            connectingDevices.remove(device)
    else:
        device.disconnected_callback = (lambda d=device: onDisconnectedDeviceBleak(d))
        await onConnectedDeviceBleak(device)
    

# BLEAK
async def onConnectedDeviceBleak(device):
    print(f"BLEAK: Connection success {device.name()} [{device.address()}]")
    try:
        # subscribe to the one characteristic notifications
        await start_notify(char_specifier=CHARACTERISTIC_UUID, callback=onCharacNotified )
    except Exception as e:
        print(f"BLEAK ERROR: on notify. {e}")
        
    connectingDevices.remove(device)
    
    
# BLEAK
def onCharacNotified(char, byteArray):
    data = byteArray.decode()
    clientName: str = "Ore_GOLEM_"+data[:3]
    print(f"BLEAK: Recieved msg from {clientName}: {data}")
    if data[-2:] == "01":
        g.syncState = True
    else:
        g.syncState = False


# BLEAK
def onDisconnectedDeviceBleak(device):
    print(f"BLEAK alert: Device {device.name()} [{device.address()}] disconnected")
    if device in g.matchedDevices:
        g.matchedDevices.remove(device)
        
    if device in connectingDevices:
        connectingDevices.remove(device)
        
        
# ======= BLESS server ======= #

# BLESS Server
async def initServerAsync(loop):
    global trigger, server, serverName
    
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
    
    serverName = "Ore_GOLEM_" + g.nodeID
    
    server = BlessServer(name=serverName, name_overwrite=True, loop=loop)
    
    
    # ~ adapterList = find_adapters(server.bus)
    # ~ for a in adapterList:
        # ~ print(a)
    # ~ asyncio.sleep(10)
    
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
        g.setupBless = True
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



# Testing
# ~ g.initGlobals()

# ~ loop = asyncio.get_event_loop()
# ~ loop.run_until_complete(initServerAsync(loop))
