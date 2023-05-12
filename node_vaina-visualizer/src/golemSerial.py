import serial
import time
import struct

vaina1: serial.Serial
vaina2: serial.Serial

def openSerial():
    global vaina1, vaina2

    vaina1 = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1)
    # vaina2 = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)
    time.sleep(2)


def closeSerial():
    global vaina1, vaina2

    vaina1.close()
    # vaina2.close()


def readSerial():
    global vaina1, vaina2
                  
    data:bytes = vaina1.read_until(b'\x00',64)
    char = parseSerialData(data[:2])[0]


    print(f"{char} | {data}")
    parsed, type = parseSerialData(data[2:])
    print(f"{parsed} | {type}")





# Transform raw bytes received from the device into int, float, etc.
def parseSerialData(inData:bytes):
    data_type, outData = detect_data_type(inData)
    # print(f"Raw: {inData} => {outData} | {data_type}")
    # print(f"{outData} | {data_type}")
    return outData, data_type

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