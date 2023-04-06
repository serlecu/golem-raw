import time
#import simplepyble as ble
import select
import bluetooth as bluez
import src.globals as g

class AsyncDiscoverer(bluez.DeviceDiscoverer):

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, address, device_class, rssi, name):
        print("{} - {}".format(address, name))

        # get some information out of the device class and display it.
        # voodoo magic specified at:
        # https://www.bluetooth.org/foundry/assignnumb/document/baseband
        major_classes = ("Miscellaneous",
                         "Computer",
                         "Phone",
                         "LAN/Network Access Point",
                         "Audio/Video",
                         "Peripheral",
                         "Imaging")
        major_class = (device_class >> 8) & 0xf
        if major_class < 7:
            print(" " + major_classes[major_class])
        else:
            print("  Uncategorized")

        print("  Services:")
        service_classes = ((16, "positioning"),
                           (17, "networking"),
                           (18, "rendering"),
                           (19, "capturing"),
                           (20, "object transfer"),
                           (21, "audio"),
                           (22, "telephony"),
                           (23, "information"))

        for bitpos, classname in service_classes:
            if device_class & (1 << (bitpos-1)):
                print("   ", classname)
        print("  RSSI:", rssi)

    def inquiry_complete(self):
        self.done = True



def setupBTAdapter():
  print("Initializing Bluetooth...")
#   print(f"Running on {ble.get_operating_system()}")

#   isAdapterSet = False
#   while not isAdapterSet:
#     adapters = ble.Adapter.get_adapters()
#     if len(adapters) == 0:
#           print("No adapters found")
#           time.sleep(2)
#     else:
#       for adapter in adapters:
#           print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")

#       g.BTAdapter = adapters[0] # I take the first adapter IDKW
#       g.BTAdapter.set_callback_on_scan_start(lambda: print("Scan started."))
#       g.BTAdapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
#       g.BTAdapter.set_callback_on_scan_found(lambda peripheral: filter_device(peripheral, g.targetUUID) )
#       isAdapterSet = True



def scanBT():
    # g.isScanning = True
    # g.BTAdapter.scan_for(1000)
    # g.foundDevices = g.BTAdapter.scan_get_results()
    # g.isScanning = False
    nearby_devices = bluez.discover_devices(duration=2,
                                                lookup_names=True,
                                                lookup_class=False,
                                                flush_cache=True)
    print(f"Found {len((nearby_devices))} devices.")
    print("Scan complete")

def filter_device(device, targetUUID):
    print(f"Found {device.identifier()} [{device.address()}]")
    # Check if can connect
    if (device.isconnectable()):
        services = device.services()
        
        for service in services:
            if service.uuid() == targetUUID:
                device.set_callback_on_connected(lambda device: onConnectedDevice(device) )
                device.set_callback_on_disconnected(lambda device: print(f"Lost connection with {device.address}."))
                device.connect()
                # Do subscribe ?

def onConnectedDevice(device):
    print(f"Connected with {device.address()}.")
    g.connectedDevices.append(device)

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