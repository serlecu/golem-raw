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
      #text = "{} -> {}".format(device.name, device.address)
      text = "{}. {}".format(i, device)
      test_text(screen, text, (screen.get_width()/2, 100+ypos), (255, 255, 255))
      ypos += 20


def DrawDebugLayer():
  test_text(g.screen, "IsScanning: {}".format(g.isScanning), (g.screen.get_width()/2, 20), (255, 255, 255))
  test_text(g.screen, "ScanCrono: {}".format(g.scannCrono), (g.screen.get_width()/2, 40), (255, 255, 255))
  #test_text(screen, "Threads: {}".format(threads), (100, 160), (255, 255, 255))
  debugScannedDevices(g.foundDevices, g.screen)