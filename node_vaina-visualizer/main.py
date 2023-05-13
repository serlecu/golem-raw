import time
import threading

#import simplepyble as ble
import bluetooth as bluez
import pygame

from src.bluetooth import *
from src.graphics import *
from src.debugInDisplay import *

def Setup():
    import src.globals as g

    g.initGlobals()

    # Initialize Pygame
    pygame.init()

    g.screen = pygame.display.set_mode((480,480))
    pygame.display.set_caption("Golem: Vaina Visualizer")
    pygame.mouse.set_visible(False)

    # Initialize Bluetooth
    setupBTAdapter()

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
