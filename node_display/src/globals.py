# import simplepyble as ble
import pygame
import uuid
import time
import random


nodeID: str
setupBleak: bool = False
setupBless: bool = False
setupPygame: bool = False
lastLoopTime: float = 0.0


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


# Offline Mode
offlineMode: bool = True
offlineListLen: int
offlineMacList: list = [
    "SLAG_a9:dc:27 -> b3:e3:15:a9:dc:27",
    "SLAG_b5:09:7e -> b3:e3:15:b5:09:7e",
    "SLAG_ee:7c:71 -> b3:e3:15:ee:7c:71",
    #"SLAG_de:92:da -> b3:e3:15:de:92:da",
    "85:f5:75:ce:4a:e3",
    "7e:4b:74:3f:1b:7d",
    "a2:fd:1c:3f:97:9f",
    "ed:ac:0d:81:05:be",
    "9b:a5:2f:a2:9a:f9",
    "b4:12:78:ea:01:d7",
    "db:da:84:c9:95:66",
    "b2:88:a1:4a:58:bc",
    "b3:89:a7:94:39:5c",
    "d5:17:69:c1:3c:15",
    "b3:e3:15:e5:a7:65",
    "eb:67:71:68:d8:a2",
    "bf:a5:fb:0c:b0:47" ]#,
    # "d3:44:01:6b:48:a5",
    # "cf:d6:b4:d6:06:dd",
    # "33:c9:74:00:c1:9d" ]


def initGlobals():
  global lastLoopTime, scannCrono, scannFrequency, isScanning, foundDevices
  global deviceInfo, nodeID, foundDevicesBleak, offlineMode, offlineListLen
  
  lastLoopTime = time.time()
  nodeID = str(uuid.uuid1()).split("-")[1]

  scannCrono = 5
  # ~ scannFrequency = 10
  isScanning = False
  foundDevices = []
  foundDevicesBleak = []
  # ~ matchedClients = []
  deviceInfo = ""

  if offlineMode:
    offlineListLen = random.randint(10, 16)
    print(f"Offline Mode: {offlineListLen} devices")
  
  print(f"Initialize Golem Node #{nodeID}")


def shuffleOfflineList():
  global offlineMacList, offlineListLen

  offlineListLen = random.randint(10, 16)
  random.shuffle(offlineMacList)

  
