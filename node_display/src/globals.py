# import simplepyble as ble
import pygame
import uuid
import time

nodeID: str
setupBleak: bool = False
setupBless: bool = False
setupPygame: bool = False
lastLoopTime: float


# Bluetooth
deviceInfo: str
isScanning: bool
scannCrono: float = 3.0
scannFrequency: float = 10.0
killBleak: bool = False
foundDevicesBleak: list#[BLEDevice]
# ~ matchedClients: list#[BleakClient]

isConnecting:bool = False
connectCrono: float = 0.0
connectFreq: float = 5.0
failedNotifications: list

runningBLEserver: bool = False

# Rail
i2cConnected = False
killRail: bool = False
lastEndSwitch: bool = False
railDirection: bool = True
railSpeed: int = 60
railDelay: float = 1.0
endSwitchCounter = 0
syncState = False


# Pygame
screen: pygame.Surface

def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices, deviceInfo, nodeID, foundDevicesBleak
  lastLoopTime = time.time()
  nodeID = str(uuid.uuid1()).split("-")[1]

  scannCrono = 5
  # ~ scannFrequency = 10
  isScanning = False
  foundDevices = []
  foundDevicesBleak = []
  # ~ matchedClients = []
  deviceInfo = ""
  
  print(f"Initialize Golem Node #{nodeID}")
  
