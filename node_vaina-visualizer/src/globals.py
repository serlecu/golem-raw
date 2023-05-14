#from simplepyble import Adapter
from pygame import Surface
import time

lastLoopTime: float

noDataMode: bool = False
serialMode: bool = True
serialCrono:float = 0.0
killSerialThread: bool = False

isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
matchedDevices: list
failedNotifications: list[list] = []

screen: Surface
dashboardCrono: float = 0.0

sensorDataList: list #of VainaSensorNode

TARGET_UUID = '19b10000-e8f2-537e-4f6c-d104768a1214'

# Characteristics UUIDs
UUID_MAG = '19b10010-e8f2-537e-4f6c-d104768a1214'
UUID_ACCEL = '19b10011-e8f2-537e-4f6c-d104768a1214'
UUID_GYRO = '19b10012-e8f2-537e-4f6c-d104768a1214'
UUID_LIGHT = '19b10020-e8f2-537e-4f6c-d104768a1214'
UUID_GEST = '19b10030-e8f2-537e-4f6c-d104768a1214'
UUID_PROXIMITY = '19b10040-e8f2-537e-4f6c-d104768a1214'
UUID_TEMP = '19b10050-e8f2-537e-4f6c-d104768a1214'
UUID_HUMIDITY = '19b10060-e8f2-537e-4f6c-d104768a1214'
UUID_PRESSURE = '19b10070-e8f2-537e-4f6c-d104768a1214'
UUID_IR = '19b10080-e8f2-537e-4f6c-d104768a1214'

# Vaina1 variables
magVaina1:list[float] = [0,0,0]
accelVaina1:list[float] = [0,0,0]
gyroVaina1:list[float] = [0,0,0]
lightVaina1:list[int] = [0,0,0]
proxVaina1:int = 0
tempVaina1:float = 0
humVaina1:float = 0
pressVaina1:float = 0
irVaina1:list = [0,0,0,0,0,0,0,0]

# Vaina2 variables
magVaina2:list[float] = [0,0,0]
accelVaina2:list[float] = [0,0,0]
gyroVaina2:list[float] = [0,0,0]
lightVaina2:list[int] = [0,0,0]
proxVaina2:int = 0
tempVaina2:float = 0
humVaina2:float = 0
pressVaina2:float = 0
irVaina2:list = [0,0,0,0,0,0,0,0]

def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, matchedDevices, sensorDataList, screen
  lastLoopTime = time.time()

  scannCrono = 0
  scannFrequency = 10
  isScanning = False
  foundDevices = []
  matchedDevices = []
  sensorDataList = []


# Struct for a Vaina Sensor Data
# it has to store the device uuid and all the sensor data
class VainaSensorNode: #! UUID is actually the MAC address
  def __init__(self, _uuid: str, _name: str = ""):
    self.deviceUUID:str = _uuid
    self.deviceName:str = _name
    self.rssi: int = 0

    self.mag: list = [0,0,0]
    self.accel: list = [0,0,0]
    self.gyro: list = [0,0,0]
    self.light: list = [0,0,0]
    self.gest: int = 0
    self.proximity: float = 0
    self.temp: float = 21
    self.humidity: float = 124
    self.pressure: float = 0
    self.impulseResponse: list = [0,0,0,0,0,0,0,0]

    self.reading: bool = False
    self.writeing: bool = False

  def __str__(self):
    return f"VainaSensorNode({self.deviceUUID})"
  
  def __eq__(self, other):
    return self.deviceUUID == other.deviceUUID
  
  def __hash__(self):
    return hash(self.deviceUUID)

  def getSensorData(self):
    # while self.writeing:
    #   time.sleep(0.01)
    return {
      'uuid': self.deviceUUID,
      'mag': self.mag,
      'accel': self.accel,
      'gyro': self.gyro,
      'light': self.light,
      'gest': self.gest,
      'proximity': self.proximity,
      'temp': self.temp,
      'humidity': self.humidity,
      'pressure': self.pressure,
      'impulseResponse': self.impulseResponse
    }

  def updateSensorData(self, data: dict):
    self.writeing = True

    self.mag = data['mag']
    self.accel = data['accel']
    self.magZ = data['gyro']
    self.light = data['light']
    self.gest = data['gest']
    self.proximity = data['proximity']
    self.temp = data['temp']
    self.humidity = data['humidity']
    self.pressure = data['pressure']
    self.impulseResponse = data['impulseResponse']

    self.writeing = False

  def updateSensorDataFromUUID(self, uuid: str, data):
    self.writeing = True

    if uuid == UUID_MAG:
      self.mag = data
    elif uuid == UUID_ACCEL:
      self.accel = data
    elif uuid == UUID_GYRO:
      self.gyro = data
    elif uuid == UUID_LIGHT:
      self.light = data
    elif uuid == UUID_GEST:
      self.gest = data
    elif uuid == UUID_PROXIMITY:
      self.proximity = data
    elif uuid == UUID_TEMP:
      self.temp = data
    elif uuid == UUID_HUMIDITY:
      self.humidity = data
    elif uuid == UUID_PRESSURE:
      self.pressure = data
    elif uuid == UUID_IR:
      self.impulseResponse = data
    else:
      print(f"UUID {uuid} not found")
      
      self.writeing = False

  def setRSSI(self, rssi: int):
    self.writeing = True

    self.rssi = rssi

    self.writeing = False

  def getSensorDataByUUID(self, uuid: str):
    # while self.writeing:
    #   time.sleep(0.01)

    if uuid == UUID_MAG:
      return self.mag
    elif uuid == UUID_ACCEL:
      return self.accel
    elif uuid == UUID_GYRO:
      return self.gyro
    elif uuid == UUID_LIGHT:
      return self.light
    elif uuid == UUID_GEST:
      return self.gest
    elif uuid == UUID_PROXIMITY:
      return self.proximity
    elif uuid == UUID_TEMP:
      return self.temp
    elif uuid == UUID_HUMIDITY:
      return self.humidity
    elif uuid == UUID_PRESSURE:
      return self.pressure
    elif uuid == UUID_IR:
      return self.impulseResponse
    else:
      print(f"UUID {uuid} not found")

  def getDeviceUUID(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.deviceUUID
  
  def getDeviceName(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.deviceName
  
  def getRSSI(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.rssi

  def getMagnetometer(self):
    # while self.writeing:
    #   time.sleep(0.01)

    if type(self.mag) == list:
      return self.mag
    if type(self.mag) == str:
      return list(map(float, self.mag.split(',')))
    else:
      return [0, 0, 0]

  def getAccelerometer(self):
    # while self.writeing:
    #   time.sleep(0.01)

    if type(self.accel) == list:
      return self.accel
    if type(self.accel) == str:
      return list(map(float, self.accel.split(',')))
    else:
      return [0, 0, 0]

  def getGyroscope(self):
    # while self.writeing:
    #   time.sleep(0.01)

    if type(self.gyro) == list:
      return self.gyro
    if type(self.gyro) == str:
      return list(map(float, self.gyro.split(',')))
    else:
      return [0, 0, 0]

  def getLight(self):
    # while self.writeing:
    #   time.sleep(0.01)

    if type(self.light) == list:
      return self.light
    if type(self.light) == str:
      return list(map(float, self.light.split(',')))
    else:
      return [0, 0, 0]

  def getGesture(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.gest

  def getProximity(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return int(self.proximity)

  def getTemp(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.temp

  def getHumidity(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.humidity

  def getPressure(self):
    # while self.writeing:
    #   time.sleep(0.01)

    return self.pressure

  def getImpulseResponse(self):
    # while self.writeing:
    #   time.sleep(0.01)

    if type(self.impulseResponse) == list:
      return self.impulseResponse
    if type(self.impulseResponse) == str:
      return list(map(float, self.impulseResponse.split(',')))
    else:
      return [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0] 