import time
import os
import threading
import pygame

from src.bluetooth import *
from src.graphics import *
from src.debug_display import *
from src.rail import*

import simplepyble as ble

def Setup():
  import src.globals as g

  g.initGlobals()
  
  # Init Rail
  initRail()
  rail_thread = threading.Thread(target=railControl, daemon=True)
  rail_thread.start()
  

  # Initialize Pygame
  print("PYGAME INIT")
  os.environ["DISPLAY"] = ":0"
  pygame.init()
  
  # get os
  platform_os = os.uname()[0]
  print("OS: " + platform_os)

  if platform_os == "Darwin":
    g.screen = pygame.display.set_mode((480,480))
  else:
    # ~ g.screen = pygame.display.set_mode((480,480),pygame.FULLSCREEN)
    g.screen = pygame.display.set_mode((480,480))
  pygame.display.set_caption("Golem: Display Node")
  pygame.mouse.set_visible(False)

  # Initialize BLE Client
  setupBTAdapter()
  
  # Initialize BLE Server
  asyncio.run(initServerAsync())
  
  # Dirty way of waiting
  # ~ while not g.runningBLEserver:
    # ~ time.sleep(0.5)
  # This thread is blocking everything!!!!
  # ~ bless_thread = threading.Thread(target=runBlessListener(), daemon=True)
  # ~ bless_thread.start()
  

# End of Setup() ========================================


def Update():
  import src.globals as g

  while True:
    # Handle Bluetooth device scanning
    if((g.isScanning == False) and (g.scannCrono <= 0)):
      scan_thread = threading.Thread(target=scanBT, daemon=True)
      scan_thread.start()
      g.scannCrono = g.scannFrequency
       
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit the application if the X button is pressed
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Quit if the 'esc' key is pressed
                pygame.quit()
                quit()

    # Handle Bluetooth connections and data
    handleBTConnections()
    handleBTData()

    # Draw graphics on the screen
    DrawLoop()
    DrawDebugLayer()

    # Update the Pygame display
    pygame.display.update()


    # Update Timers
    if(g.isScanning == False):
      g.scannCrono -= (time.time() - g.lastLoopTime)

    g.lastLoopTime = time.time()

  # End of Update() ========================================
    

# Start the event loop
if __name__ == "__main__":
  Setup()
  Update()
