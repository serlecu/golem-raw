#from simplepyble import Adapter
from pygame import Surface
import time

lastLoopTime: float



isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
matchedDevices: list
failedNotifications: list = []

screen: Surface

sensorDataList: list #of VainaSensorNode

TARGET_UUID = '19b10000-e8f2-537e-4f6c-d104768a1214'

# Characteristics UUIDs
UUID_MAGX = '19b10010-e8f2-537e-4f6c-d104768a1214'
UUID_MAGY = '19b10011-e8f2-537e-4f6c-d104768a1214'
UUID_MAGZ = '19b10012-e8f2-537e-4f6c-d104768a1214'
UUID_LIGHT = '19b10020-e8f2-537e-4f6c-d104768a1214'
UUID_COLORR = '19b10021-e8f2-537e-4f6c-d104768a1214'
UUID_COLORG = '19b10022-e8f2-537e-4f6c-d104768a1214'
UUID_COLORB = '19b10023-e8f2-537e-4f6c-d104768a1214'
UUID_PROXIMITY = '19b10040-e8f2-537e-4f6c-d104768a1214'
UUID_TEMP = '19b10050-e8f2-537e-4f6c-d104768a1214'
UUID_HUMIDITY = '19b10060-e8f2-537e-4f6c-d104768a1214'
UUID_PRESSURE = '19b10070-e8f2-537e-4f6c-d104768a1214'
UUID_IR = '19b10080-e8f2-537e-4f6c-d104768a1214'    


def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, matchedDevices, sensorDataList, screen
  lastLoopTime = time.time()

  scannCrono = 5
  scannFrequency = 5
  isScanning = False
  foundDevices = []
  matchedDevices = []
  sensorDataList = []


# Struct for a Vaina Sensor Data
# it has to store the device uuid and all the sensor data
class VainaSensorNode: #! UUID is actually the MAC address
  def __init__(self, _uuid: str, _name: str = ""):
    self.deviceUUID = _uuid
    self.deviceName = _name
    self.magX: float = 0
    self.magY: float = 0
    self.magZ: float = 0
    self.light: int = 255
    self.colorR: int = 255
    self.colorG: int = 255
    self.colorB: int = 255
    self.proximity: float = 0
    self.temp: float = 21
    self.humidity: float = 124
    self.pressure: float = 0
    self.impulseResponse: list = []

  def __str__(self):
    return f"VainaSensorNode({self.deviceUUID})"
  
  def __eq__(self, other):
    return self.deviceUUID == other.deviceUUID
  
  def __hash__(self):
    return hash(self.deviceUUID)

  def getSensorData(self):
    return {
      'uuid': self.deviceUUID,
      'magX': self.magX,
      'magY': self.magY,
      'magZ': self.magZ,
      'light': self.light,
      'colorR': self.colorR,
      'colorG': self.colorG,
      'colorB': self.colorB,
      'proximity': self.proximity,
      'temp': self.temp,
      'humidity': self.humidity,
      'pressure': self.pressure,
      'impulseResponse': self.impulseResponse
    }

  def updateSensorData(self, data: dict):
    self.magX = data['magX']
    self.magY = data['magY']
    self.magZ = data['magZ']
    self.light = data['light']
    self.colorR = data['colorR']
    self.colorG = data['colorG']
    self.colorB = data['colorB']
    self.proximity = data['proximity']
    self.temp = data['temp']
    self.humidity = data['humidity']
    self.pressure = data['pressure']
    self.impulseResponse = data['impulseResponse']

  def updateSensorDataFromUUID(self, uuid: str, data):
    if uuid == UUID_MAGX:
      self.magX = data
    elif uuid == UUID_MAGY:
      self.magY = data
    elif uuid == UUID_MAGZ:
      self.magZ = data
    elif uuid == UUID_LIGHT:
      self.light = data
    elif uuid == UUID_COLORR:
      self.colorR = data
    elif uuid == UUID_COLORG:
      self.colorG = data
    elif uuid == UUID_COLORB:
      self.colorB = data
      print(self.colorB)
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

  def getSensorDataByUUID(self, uuid: str):
    if uuid == UUID_MAGX:
      return self.magX
    elif uuid == UUID_MAGY:
      return self.magY
    elif uuid == UUID_MAGZ:
      return self.magZ
    elif uuid == UUID_LIGHT:
      return self.light
    elif uuid == UUID_COLORR:
      return self.colorR
    elif uuid == UUID_COLORG:
      return self.colorG
    elif uuid == UUID_COLORB:
      return self.colorB
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
    return self.deviceUUID
  
  def getDeviceName(self):
    return self.deviceName

  def getMagX(self):
    return self.magX

  def getMagY(self):
    return self.magY

  def getMagZ(self):
    return self.magZ

  def getLight(self):
    return self.light

  def getColorR(self):
    return self.colorR

  def getColorG(self):
    return self.colorG

  def getColorB(self):
    return self.colorB

  def getProximity(self):
    return self.proximity

  def getTemp(self):
    return self.temp

  def getHumidity(self):
    return self.humidity

  def getPressure(self):
    return self.pressure

  def getImpulseResponse(self):
    return self.impulseResponse