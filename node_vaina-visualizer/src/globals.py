#from simplepyble import Adapter
from pygame import Surface
import time

lastLoopTime: float

#BTAdapter: Adapter
targetUUID = "19B10000-E8F2-537E-4F6C-D104768A1214"

isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
connectedDevices: list

screen: Surface

def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices
  lastLoopTime = time.time()

  scannCrono = 5
  scannFrequency = 5
  isScanning = False
  foundDevices = []