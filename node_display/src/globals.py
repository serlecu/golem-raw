import simplepyble as ble
import pygame
import uuid
import time

lastLoopTime: float
nodeID: str

# Bluetooth
deviceInfo: str
isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
matchedDevices: list
failedNotifications: list

runningBLEserver: bool = False

# Rail
killRail: bool = False
lastEndSwitch: bool = False
railDirection: bool = True
railSpeed: int = 50
railDelay: float = 1.0
endSwitchCounter = 0
syncState = False


# Pygame
screen: pygame.Surface

def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, deviceInfo, nodeID
  lastLoopTime = time.time()
  nodeID = str(uuid.uuid1()).split("-")[1]

  scannCrono = 5
  scannFrequency = 10
  isScanning = False
  foundDevices = []
  matchedDevices = []
  deviceInfo = ""
  
  print(f"Initialize Golem Node #{nodeID}")
