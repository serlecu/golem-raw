import simplepyble as ble
import pygame
import time

lastLoopTime: float

deviceInfo: str
isScanning: bool
scannCrono: float
scannFrequency: float
foundDevices: list #str/bluetooth.Device
matchedDevices: list

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