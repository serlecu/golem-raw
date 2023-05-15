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


def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, matchedDevices, sensorDataList, screen
  lastLoopTime = time.time()

  scannCrono = 2
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
    self.mag: list = []
    self.accel: list = []
    self.gyro: list = []
    self.light: list = []
    self.gest: int = 0
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

  def updateSensorDataFromUUID(self, uuid: str, data):
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

  def getSensorDataByUUID(self, uuid: str):
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
    return self.deviceUUID
  
  def getDeviceName(self):
    return self.deviceName

  def getMagnetometer(self):
    return self.mag

  def getAccelerometer(self):
    return self.accel

  def getGyroscope(self):
    return self.gyro

  def getLight(self):
    return self.light

  def getGesture(self):
    return self.gest

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