import serial
import serial.tools.list_ports
import time
import random
import noise
import struct
from . import globals as g

import src.golemAudio as audio

twodevices = False
vaina1Port = ""
vaina2Port = ""
vaina1PortNew = ""
vaina2PortNew = ""


serialCronoMax:float = 0.1
lastSerialLoopTime:float = 0.0

vaina1Connected = False
vaina2Connected = False
vaina1: serial.Serial
vaina2: serial.Serial

def setupSerial():
    findPorts()
    openSerial()


def handleSerialThread():
    while not g.killSerialThread:
        handleSerial()
        time.sleep(0.1)


def handleSerial():
    findPorts()
    openSerial()

    readSerial()

    # reconnectSerial()


def findPorts():
    global vaina1Port, vaina2Port, vaina1PortNew, vaina2PortNew

    # if vaina1Port == "": # or vaina2Port == "":
    # print("Finding ports...")

    filteredDevices:list = []
    try:
        devices = serial.tools.list_ports.comports()
        # print(f"Devices: {devices}")
        print(f"Vaina1: {vaina1Port}. Vaina2: {vaina2Port}")
    except:
        print("Error finding ports")
        return
    else:
        for device in devices:
            print(f"Port: {device[0]} {device[1]}")
            if device[1] == "Nano 33 BLE":
                filteredDevices.append([device[0],""])
        
        if len(filteredDevices) > 1:
            vaina1PortNew = filteredDevices[0][0]
            vaina2PortNew = filteredDevices[1][0]
        elif len(filteredDevices) > 0:
            vaina1PortNew = filteredDevices[0][0]
            vaina2PortNew = ""
        else:
            vaina1PortNew = ""
            vaina2PortNew = ""

        print(f"New Ports: [Vaina1: {vaina1PortNew}. Vaina2: {vaina2PortNew} ]")  

        # for i in range(0,len(filteredDevices)):
        #     if filteredDevices[i][0] == vaina1Port:
        #         filteredDevices[i][1] = "vaina1"

        #     elif filteredDevices[i][0] == vaina2Port:
        #         filteredDevices[i][1] = "vaina1"

        #     else:
        #         if filteredDevices[i][1] == "":
        #             vaina1Port = filteredDevices[i][0]
        #             filteredDevices[i][1] = "vaina1"
        #         elif filteredDevices[i][1] == "":
        #             vaina2Port = filteredDevices[i][0]
        #             filteredDevices[i][1] = "vaina2" 
        # print(f"New Ports: [Vaina1: {vaina1Port}. Vaina2: {vaina2Port} ]")  


def openSerial():
    global vaina1, vaina2, vaina1Connected, vaina2Connected, vaina1Port, vaina2Port

    print("Opening serial ports...")

    if not (vaina1Port == vaina1PortNew):
        print("New vaina port 2 available")
        if not (vaina1PortNew == ""):
            try:
                vaina1 = serial.Serial(vaina1PortNew, 9600, timeout=1)
                time.sleep(1)
            except Exception as e:
                print(e)
                print("Trying again later...")
                try:
                    vaina1.close()
                except:
                    print("Port for vaina 1 wasn't open")
                vaina1Connected = False
                vaina1Port = ""
                # time.sleep(5)
            else:
                vaina1Port = vaina1PortNew
                vaina1Connected = True
                print("Connected to vaina1.")

    if not (vaina2Port == vaina2PortNew):
        print("New vaina port 2 available")
        if not(vaina2PortNew == ""):
            try:
                vaina2 = serial.Serial(vaina2PortNew, 9600, timeout=1)
                time.sleep(1)
            except Exception as e:
                print(e)
                print("Trying again later...")
                try:
                    vaina2.close()
                except:
                    print("Port for vaina 2 wasn't open")
                vaina2Connected = False
                vaina2Port = ""
                # time.sleep(5)
            else:
                vaina2Port = vaina2PortNew
                vaina2Connected = True
                print("Connected to vaina2.")

    print("End Serial ports opening.")


def reconnectSerial():
    global vaina1, vaina2, vaina1Connected, vaina2Connected, vaina1Port, vaina2Port
    print("Reconnecting serial ports..."
          )
    if not vaina1Connected:
        try:
            vaina1 = serial.Serial(vaina1Port, 9600, timeout=1)
        except Exception as e:
            print(e)
            print("Trying again later...")
            vaina1Connected = False
            vaina1Port = ""
        else:
            vaina1Connected = True
            print("Connected to vaina1.")

    if not vaina2Connected:
        try:
            vaina2 = serial.Serial(vaina2Port, 9600, timeout=1)
        except Exception as e:
            print(e)
            print("Trying again later...")
            vaina2Connected = False
            vaina2Port = ""
        else:
            vaina2Connected = True
            print("Connected to vaina2.")

    print("Serial ports reconnected if success.")

    
def readSerial():
    global vaina1, vaina2, vaina1Connected, vaina2Connected
    global vaina1Port, vaina2Port, serialCronoMax, lastSerialLoopTime
    print("Reading serial...")
    
    if g.serialCrono >= serialCronoMax:
        serialCrono = 0.0

        newData1 = False
        header1:str = ""
        uuid1:str = ""
        value1 = None
        newData2 = False
        header2:str = ""
        uuid2:str = ""
        value2 = None

        # Si hay conexión leer y parsear datos
        if vaina1Connected:    
            # Leer datos de vaina1
            if vaina1Connected:
                data1:bytes = b'\x00'
                try:
                    # Read data from serial1                    
                    data1 = vaina1.read_until(b'\n',256)
                except Exception as e:
                    print(e)
                    vaina1Connected = False
                    vaina1Port = ""
                else:
                    print(f"VAINA1 in: {data1}")
                    if data1 != b'\x00' and b'$' in data1 and b'\n' in data1:
                        # if data1[0] == b'$':
                            #Eliminar primer caracter cabecera '$'
                            data1 = data1[1:]

                            string_value = data1.decode()
                            if string_value[-1:] == "\n":
                                val_array = string_value.split('$')
                                if len(val_array) > 1:
                                    string_value = val_array[-1]
                                else:
                                    string_value = val_array[0]
                            else:
                                string_value = string_value.split('$')[-2]
                                string_value = string_value.strip('\n')#.strip('\r')

                            #Aislar la cabecera (2 primeros caracteres)
                            header1 = string_value[:2]
                            if header1 == "80":
                                print("VAINA2: got IR ========================")
                            uuid1 = '19b100' + header1 + '-e8f2-537e-4f6c-d104768a1214'
                            #Aislar el dato y extraer el tipo
                            vtype1, value1  = parseFromString(string_value[2:])
                            if value1 != None:
                                print(f"Vaina1 Char {header1}: {value1} | {vtype1}")
                                newData1 = True
        # Si no hay conexión en Vaina1 hacer datos random
        # else:
        #     # print("No vaina1")
        #     header1 = random.choice(["10","11","12","20","40","50","60","70","80"])
        #     uuid1 = '19b100' + header1 + '-e8f2-537e-4f6c-d104768a1214'
        #     if header1:
        #     # print(f"Char {uuid1}: {value1} | {type}")
        #         if header1  == "10":
        #             # value1 = []
        #             # for i in range(len(g.magVaina1)):
        #             #     value =  200 * round(noise.pnoise1(g.magVaina1[i]/50 + i, 1), 2) -100
        #             #     value1.append(value)                          
                                               
        #             value1 = random.sample(range(25, 17600), 3) # -100/+100
        #             value1 = [round(x/100-100,2) for x in value1]
        #         elif header1 == "11":
        #             value1 = random.sample(range(0, 200), 3) # -1/+1
        #             value1 = [round(x/100-1,2) for x in value1]
        #         elif header1 == "12":
        #             value1 = random.sample(range(0, 100), 3) # -50/+50
        #             value1 = [round(x/100-50,2) for x in value1]
        #         elif header1 == "20":
        #             value1 = random.sample(range(0, 255), 3)
        #         elif header1 == "40":
        #             value1 = random.randint(0,255)
        #         elif header1 == "50":
        #             value1 = round(random.randint(2100,3500)/100,2)
        #         elif header1 == "60":
        #             value1 = round(random.randint(2000,4500)/100,2)
        #         elif header1 == "70":
        #             value1 = round(random.randint(10000,10100)/100,2)
        #         elif header1 == "80":
        #             value1 = random.sample(range(8000, 8000000000), 8) # -64/-6
        #             value1 = [round(x*0.1,2) for x in value1]
                    
        #     newData1 = True
        #     pass


        # Si hay conexión leer y parsear datos            
        if vaina2Connected:
            # Leer datos de vaina2
            if vaina2Connected:
                data2:bytes = b'\x00'
                try:
                    # Read data from serial2
                    data2 = vaina2.read_until(b'\n',256)
                except Exception as e:
                    print(e)
                    vaina2Connected = False
                    vaina2Port = ""
                    for device in g.sensorDataList:
                        if device.getDeviceUUID() == "vaina2":
                            g.sensorDataList.remove(device)
                else:
                    print(f"VAINA2 in: {data2}")
                    if data2 != b'\x00' and b'$' in data2 and b'\n' in data2:
                        # if data2[0] == b'$':
                            #Eliminar primer caracter cabecera '$'
                            data2 = data2[1:]

                            string_value = data2.decode()
                            if string_value[-1:] == '\n':
                                val_array = string_value.split('$')
                                if len(val_array) > 1:
                                    string_value = val_array[-1]
                                else:
                                    string_value = val_array[0]
                            else:
                                string_value = string_value.split('$')[-2]
                                string_value = string_value.strip('\n')#.strip('\r')
                            
                            #Aislar la cabecera (2 primeros caracteres)
                            header2 = string_value[:2]
                            if header2 == "80":
                                print("VAINA2: got IR ========================")
                            uuid2 = '19b100' + header2 + '-e8f2-537e-4f6c-d104768a1214'
                            #Aislar el dato y extraer el tipo
                            vtype2, value2  = parseFromString(string_value[2:])
                            if value2 != None:
                                print(f"Vaina2 Char {header2}: {value2} | {vtype2}")
                                newData2 = True
        # Si no hay conexión en Vaina2 hacer datos random
        # else:
        #     # print("No vaina2")
        #     header2 = random.choice(["10","11","12","20","40","50","60","70","80"])
        #     uuid2 = '19b100' + header2 + '-e8f2-537e-4f6c-d104768a1214'
        #     if header2:
        #     # print(f"Char {uuid2}: {value2} | {type}")
        #         if header2  == "10":
        #             value2 = random.sample(range(25, 17600), 3)
        #             value2 = [round(x/100-100,2) for x in value2]
        #         elif header2 == "11":
        #             value2 = random.sample(range(0, 200), 3)
        #             value2 = [round(x/100-1,2) for x in value2]
        #         elif header2 == "12":
        #             value2 = random.sample(range(-50, 50), 3)
        #             value2 = [round(x/100-50,2) for x in value2]
        #         elif header2 == "20":
        #             value2 = random.sample(range(0, 255), 3)
        #         elif header2 == "40":
        #             value2 = random.randint(0,255)
        #         elif header2 == "50":
        #             value2 = round(random.randint(2100,3500)/100,2)
        #         elif header2 == "60":
        #             value2 = round(random.randint(2000,4500)/100,2)
        #         elif header2 == "70":
        #             value2 = round(random.randint(10000,10100)/100,2)
        #         elif header2 == "80":
        #             value2 = random.sample(range(8000, 8000000000), 8)
        #             value2 = [round(x*0.1,2) for x in value2]
                    
        #     newData2 = True
        #     pass


        # Actualizar datos de vaina1
        if newData1:
            # print(f"Char {uuid1}: {value1} | {type}")
            if header1  == "10":
                g.magVaina1 = value1
            elif header1 == "11":
                g.accelVaina1 = value1
            elif header1 == "12":
                g.gyroVaina1 = value1
            elif header1 == "20":
                # if value1[0] < g.lightVaina1[0]:  # type: ignore
                #     audio.cambioLuz()
                # elif value1[0] > g.lightVaina1[0]: # type: ignore
                #     audio.cambioLuz()
                # else:
                #     audio.noCambioLuz()
                g.lightVaina1 = value1
            elif header1 == "40":
                g.proxVaina1 = value1
            elif header1 == "50":
                g.tempVaina1 = value1
            elif header1 == "60":
                g.humVaina1 = value1
            elif header1 == "70":
                g.pressVaina1 = value1
            elif header1 == "80":
                g.irVaina1 = value1
                print("VAINA1: passed IR ========================")
            else:
                print(f"Unknown header {header1} from vaina1")
        
        # Actualizar datos de vaina2
        if newData2:
            # print(f"Char {uuid2}: {value2} | {type}")
            if header2  == "10":
                g.magVaina2 = value2
            elif header2 == "11":
                g.accelVaina2 = value2
            elif header2 == "12":
                g.gyroVaina2 = value2
            elif header2 == "20":
                g.lightVaina2 = value2
            elif header2 == "40":
                g.proxVaina2 = value2
            elif header2 == "50":
                g.tempVaina2 = value2
            elif header2 == "60":
                g.humVaina2 = value2
            elif header2 == "70":
                g.pressVaina2 = value2
            elif header2 == "80":
                g.irVaina2 = value2
                print("VAINA2: passed IR ========================")
            else:
                print(f"Unknown header {header2} from vaina2")

        
    else:
        g.serialCrono += lastSerialLoopTime
        lastSerialLoopTime = time.time() - lastSerialLoopTime
    
    print("Serial read.")


def parseFromString(string_value:str):
    try:
        # Try unpacking as int
        int_value = int(string_value)
        return "int", int_value
    except ValueError:
        pass

    try:
        # Try unpacking as float
        float_value = float(string_value)
        return "float", float_value
    except ValueError:
        pass

    try:
        # Try unpacking as int_array
        str_array = string_value.split(',')
        int_array = [int(x) for x in str_array]
        return "int_array", int_array
    except ValueError:
        pass

    try:
        # Try as array of floats
        str_array = string_value.split(',')
        float_array = [float(x) for x in str_array]
        return "float_array", float_array
    except ValueError:
        pass

    print(f"Couldn't parse: {string_value}")
    # If none of the above formats work, return "unknown"
    return "unknown", None