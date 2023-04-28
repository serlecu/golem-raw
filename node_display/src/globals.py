import simplepyble as ble
import pygame
import time

lastLoopTime: float

# Bluetooth
deviceInfo: str
isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
matchedDevices: list

# Rail
killRail: bool = False
lastEndSwitch: bool = False
railDirection: bool = True
railSpeed: int = 50
railDelay: float = 1.0


# Pygame
screen: pygame.Surface

def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, deviceInfo
  lastLoopTime = time.time()

  scannCrono = 5
  scannFrequency = 5
  isScanning = False
  foundDevices = []
  matchedDevices = []
  deviceInfo = ""
