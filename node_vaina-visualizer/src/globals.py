#from simplepyble import Adapter
from pygame import Surface
import time

lastLoopTime: float

#BTAdapter: Adapter
targetUUID = '19b10000-e8f2-537e-4f6c-d104768a1214'

isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
connectedDevices: list

screen: Surface

def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, connectedDevices
  lastLoopTime = time.time()

  scannCrono = 5
  scannFrequency = 5
  isScanning = False
  foundDevices = []
  connectedDevices = []