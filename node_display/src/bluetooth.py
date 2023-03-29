import bluetooth

def scanBT():
    print("Scanning...")
    devices = bluetooth.discover_devices(duration=2, lookup_class=False, lookup_names=True)
    
    print("Found {} devices".format(len(devices)))
    for device in devices:
        print("{} - {}".format(device.name, device.address))

    return devices