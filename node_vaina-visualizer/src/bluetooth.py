import time
import threading
import simplepyble as ble

import src.globals as g

BTAdapter: ble.Adapter #type: ignore

def setupBTAdapter():
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

      g.BTAdapter = adapters[0] # I take the first adapter IDKW                   #type: ignore
      g.BTAdapter.set_callback_on_scan_start(lambda: print("Scan started."))      #type: ignore
      #g.BTAdapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
      g.BTAdapter.set_callback_on_scan_found(lambda peripheral: filter_device(peripheral, g.targetUUID) )    #type: ignore
      isAdapterSet = True



def scanBT():
    g.isScanning = True
    g.BTAdapter.scan_for(4000)                        #type: ignore
    g.foundDevices = g.BTAdapter.scan_get_results()   #type: ignore
    g.isScanning = False
    print("Scan complete")

def filter_device(device, targetUUID):
    
    # Check if can connect
    if (device.is_connectable()):
        print(f"Found {device.identifier()} [{device.address()}]")
        services = device.services()
        for service in services:
            if service.uuid() == targetUUID:
                print(f"Matching target service {service.uuid()}")
                printCharacteristics(device)
                g.matchedDevices.append(device)
                connect_thread = threading.Thread(target=lambda: connectBT(device), daemon=True)
                connect_thread.start()
            else:
                print(f"Service {service.uuid()} not matching target {targetUUID}")

def connectBT(device):
    print("Connecting to {}".format(device.address()))
    device.set_callback_on_connected(lambda device: onConnectedDevice(device) )
    device.set_callback_on_disconnected(lambda device: onDisconnectedDevice(device) )
    device.connect()
    # if(device.connect()):
    #     printCharacteristics(device)
    # else:
    #     print("Failed to connect")
    #     return
    
def onConnectedDevice(device):
    print(f"Connected to {device.address()}.")
    g.matchedDevices.append(device)

def onDisconnectedDevice(device):
    print(f"Disconnected from {device.address()}.")
    g.matchedDevices.remove(device)

def sendBT(sock, data):
    print("Sending {}".format(data))
    # sock.send(data)

def receiveBT(sock):
    print("Receiving...")
    # data = sock.recv(1024)
    # print("Received {}".format(data))
    # return data

def printCharacteristics( device ):
    services = device.services()
    #service_characteristic_pair = []
    for service in services:
        print(f"Service: {service.uuid()}")
        for characteristic in service.characteristics():
            print(f" - Char: {characteristic.uuid()}")
            #service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

def handleBTConnections():
    pass

def handleBTData():
    pass