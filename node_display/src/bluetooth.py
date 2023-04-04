import simplepyble as ble
import bluetooth as bt
import time
import src.globals as g


# Define UUIDs for the service and characteristic
SERVICE_UUID = "0000180F-0000-1000-8000-00805F9B34FB"
CHARACTERISTIC_UUID = "00002A19-0000-1000-8000-00805F9B34FB"

def advertService(address):
    from bluetooth import BluetoothSocket
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


def scanBT():
    g.isScanning = True
    g.BTAdapter.scan_for(1000)
    g.foundDevices = g.BTAdapter.scan_get_results()
    g.isScanning = False
    print("Scan complete")


def filter_devices(devices, name):
    filtered = []
    for device in devices:
        if device.name == name:
            filtered.append(device)
    return filtered

def connectBT(device):
    print("Connecting to {}".format(device.address()))
    device.connect()
    print("Successfully connected, listing services...")
    services = device.services()
    service_characteristic_pair = []
    for service in services:
        for characteristic in service.characteristics():
            service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

def sendBT(sock, data):
    print("Sending {}".format(data))
    # sock.send(data)

def receiveBT(sock):
    print("Receiving...")
    # data = sock.recv(1024)
    # print("Received {}".format(data))
    # return data

def onDeviceFound(device):
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

def onDeviceUpdated(device):
    print(f"Updated: {device.identifier()} [{device.address()}]")

def setupBTAdapter():
  print("Initializing Bluetooth...")
  print(f"Running on {ble.get_operating_system()}") #type: ignore

  isAdapterSet = False
  while not isAdapterSet:
    adapters = ble.Adapter.get_adapters() #type: ignore
    if len(adapters) == 0:
          print("No adapters found")
          time.sleep(2)
    else:
      for adapter in adapters:
          print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")

      g.BTAdapter = adapters[0] # I take the first adapter IDKW
      #print(g.BTAdapter.identifier())
      g.BTAdapter.set_callback_on_scan_start(lambda: print("Scan started."))
      g.BTAdapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
      g.BTAdapter.set_callback_on_scan_found(lambda peripheral: onDeviceFound(peripheral))
      g.BTAdapter.set_callback_on_scan_updated(lambda peripheral: onDeviceUpdated(peripheral))
      isAdapterSet = True

      advertService(g.BTAdapter.address())

def handleBTConnections():
    from bluetooth.ble import BeaconService

    service = BeaconService()
    service.start_advertising(SERVICE_UUID,
                              1, 1, 1, 200)

    print("Done.")

def handleBTData():
    pass