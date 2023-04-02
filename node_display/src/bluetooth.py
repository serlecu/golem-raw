import simplepyble as ble
import time
import src.globals as g

def setupBTAdapter():
  print("Initializing Bluetooth...")
  print(f"Running on {ble.get_operating_system()}")

  isAdapterSet = False
  while not isAdapterSet:
    adapters = ble.Adapter.get_adapters()
    if len(adapters) == 0:
          print("No adapters found")
          time.sleep(2)
    else:
      for adapter in adapters:
          print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")

      g.BTAdapter = adapters[0] # I take the first adapter IDKW
      g.BTAdapter.set_callback_on_scan_start(lambda: print("Scan started."))
      g.BTAdapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
      g.BTAdapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))
      isAdapterSet = True


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

def sendBT(sock, data):
    print("Sending {}".format(data))
    # sock.send(data)

def receiveBT(sock):
    print("Receiving...")
    # data = sock.recv(1024)
    # print("Received {}".format(data))
    # return data



def handleBTConnections():
    pass

def handleBTData():
    pass