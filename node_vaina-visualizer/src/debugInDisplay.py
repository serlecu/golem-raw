import pygame

import src.globals as g
#from globals import *

def test_text(screen, text, pos, color):
    font = pygame.font.Font(None, 12)
    text = font.render(text, True, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    screen.blit(text, textpos)

def debugScannedDevices(devices, screen):
  ypos = 0
  for i, device in enumerate(devices):
      texColor = (255, 255, 255)
      if(device.is_connected()):
        textColor = (0, 255, 0)
      else:
        textColor = (255, 0, 0)
      text = "{}. {} -> {}".format(i, device.identifier(), device.address())
      # text = "{}. {}".format(i, device)
      test_text(screen, text, (screen.get_width()/2, 100+ypos), textColor)
      ypos += 20


def debugSensorData():
    xpos = g.screen.get_width()/2
    ypos = 100
    for dataList in g.sensorDataList: # dataList is a VainaSensorData object
      #print(f"Darwing sensor {dataList} ...")
      for key, value in dataList.getSensorData().items(): # returns a dict (key, value)
        if key == 'uuid':
          #print(f"UUID: {value}")
          test_text(g.screen, f"Device [{value}]:", (xpos, ypos), (255, 255, 255))
        else:
          #print(f"{key}: {value}")
          test_text(g.screen, " - {}: {}".format(key, value), (xpos, ypos), (255, 255, 255))
        ypos += 15
      ypos += 15


def DrawDebugLayer():
    test_text(g.screen, "IsScanning: {}".format(g.isScanning), (g.screen.get_width()/2, 20), (255, 255, 255))
    test_text(g.screen, "ScanCrono: {}".format(g.scannCrono), (g.screen.get_width()/2, 40), (255, 255, 255))
    
    # if(len(g.foundDevices) > 0):
    #   debugScannedDevices(g.foundDevices, g.screen)
    # else:
    #   test_text(g.screen, "No devices found", (g.screen.get_width()/2, 100), (255, 255, 255))

    if(len(g.matchedDevices) > 0):
      debugScannedDevices(g.matchedDevices, g.screen)
    else:
      test_text(g.screen, "No matched devices", (g.screen.get_width()/2, 50), (255, 255, 255))

    if(len(g.sensorDataList) > 0):
      debugSensorData()
    else:
       test_text(g.screen, "No sensor data", (g.screen.get_width()/2, 100), (255, 255, 255))
