import pygame

import src.globals as g

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
      textColor = (150, 150, 150)
      if device.is_connected():
        textColor = (255, 255, 255)
      elif not device.is_connectable():
        #cannot be connected
        textColor = (100, 100, 100)

      text = "{}. {} -> {}".format(i, device.identifier(), device.address())
      # text = "{}. {}".format(i, device)
      test_text(screen, text, (screen.get_width()/2, 100+ypos), textColor)
      ypos += 20
      
def debugScannedDevicesSimple(devices, screen):
  ypos = 0
  for i, device in enumerate(devices):
      textColor = (150, 150, 150)

      test_text(screen, str(device.address), (screen.get_width()/2, 100+ypos), textColor)
      ypos += 20


def DrawDebugLayer():
    test_text(g.screen, (f"[ {g.deviceInfo} ]"), (g.screen.get_width()/2, 20), (255, 255, 255))
    test_text(g.screen, (f"IsScanning: {not g.isScanning}"), (g.screen.get_width()/2, 40), (255, 255, 255))
    test_text(g.screen, (f"ScanCrono: {g.scannCrono}"), (g.screen.get_width()/2, 60), (255, 255, 255))
  
    # ~ if(len(g.foundDevices) > 0):
        # ~ debugScannedDevices(g.foundDevices, g.screen)
    # ~ else:
        # ~ test_text(g.screen, "No devices found", (g.screen.get_width()/2, 100), (255, 255, 255))
        
    if(len(g.foundDevicesBleak) > 0):
        debugScannedDevicesSimple(g.foundDevicesBleak, g.screen)
    else:
        test_text(g.screen, "No devices found", (g.screen.get_width()/2, 100), (255, 255, 255))
