import serial
import time
import struct
from . import globals as g

vaina1: serial.Serial
vaina2: serial.Serial

def openSerial():
    global vaina1, vaina2

    vaina1 = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1)
    vaina2 = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)
    time.sleep(2)

    g.sensorDataList.append(vaina1)
    g.sensorDataList.append(vaina2)


def closeSerial():
    global vaina1, vaina2

    vaina1.close()
    # vaina2.close()


def readSerial():
    global vaina1, vaina2
    newData1 = False
    uuid1 = ""
    value1 = ""
    newData2 = False
    uuid2 = ""
    value2 = ""

    # Read data from serial1                  
    data1:bytes = vaina1.read_until(b'\x00',64)
    if data1 != b'\x00':
      header1, htype1 = parseSerialData(data1[:2])
      uuid1 = '19b100' + str(header1) + '-e8f2-537e-4f6c-d104768a1214'
      value1, vtype1 = parseSerialData(data1[2:])
      # print(f"Char {uuid1}: {value1} | {type}")
      newData1 = True

    # Read data from serial2
    data2:bytes = vaina2.read_until(b'\x00',64)
    if data2 != b'\x00':
      header2, htype2 = parseSerialData(data2[:2])
      uuid2 = '19b100' + str(header2) + '-e8f2-537e-4f6c-d104768a1214'
      value2, vtype2 = parseSerialData(data2[2:])
      # print(f"Char {uuid2}: {value2} | {vtype2}")
      newData2 = True

    # Write values to the sensorDataList
    for sensorData in g.sensorDataList:
            if sensorData.deviceUUID == vaina1 and newData1:
                sensorData.updateSensorDataFromUUID(uuid1, value1)# .replace('\x00',''))
                # Check:
                #print(f"Updated {sensorData.deviceUUID}.")
                break
            elif sensorData.deviceUUID == vaina2 and newData2:
                sensorData.updateSensorDataFromUUID(uuid2, value2)# .replace('\x00',''))
                # Check:
                #print(f"Updated {sensorData.deviceUUID}.")
                break


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