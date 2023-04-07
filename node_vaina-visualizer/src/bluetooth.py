import time
import threading
import simplepyble as ble

import src.globals as g

BTAdapter: ble.Adapter #type: ignore
devicesChecked = False

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
      BTAdapter.set_callback_on_scan_found(lambda peripheral: filterDevice(peripheral, g.targetUUID) )
      isAdapterSet = True


def scanBT():
    global BTAdapter
    BTAdapter.scan_for(4000)                        
    # g.foundDevices = BTAdapter.scan_get_results()   #type: ignore


def filterDevices(devices, targetUUID):
    for device in devices:
      filterDevice(device, targetUUID)


def filterDevice(device, targetUUID):
    if device.is_connectable():
      print(f"Found: {device.identifier()} [{device.address()}]")
      services = device.services()
      for service in services:
          if service.uuid() == targetUUID:
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
    global BTAdapter, devicesChecked
    if( not BTAdapter.scan_is_active() ): 
      if( not devicesChecked ):
        for device in g.matchedDevices:
            if not device.is_connected():
              connectBT(device)
              # connect_thread = threading.Thread(target=lambda: connectBT(device), daemon=True)
              # connect_thread.start()
            else:
              print(f"Device {device.identifier()} [{device.address()}] already connected.")
        devicesChecked = True
            

def handleBTData(): # miss
    pass


def connectBT(device):
    print("Connecting to {}".format(device.address()))
    device.set_callback_on_connected(lambda: onConnectedDevice(device) )
    device.set_callback_on_disconnected(lambda: onDisconnectedDevice(device) )
    try:
      device.connect()
    except:
      print("Failed to connect to {}".format(device.address()))


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
    printCharacteristics(device)
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
              #service_characteristic_pair.append((service.uuid(), characteristic.uuid()))