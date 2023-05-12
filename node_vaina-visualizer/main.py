import time
import threading

#import simplepyble as ble
# import bluetooth as bluez
import pygame

from src.bluetooth import *
from src.graphics import *
from src.debugInDisplay import *

def Setup():
    import src.globals as g

    g.initGlobals()

    # Initialize Pygame
    # setupSimplePygame(g.screen)
    setupScreens()

    # Initialize Bluetooth
    setupBTAdapter()

    # End of Setup() ========================================

def Update():
    import src.globals as g

    while True:
        # Handle Bluetooth device scanning
        if((g.isScanning == False) and (g.scannCrono >= g.scannFrequency) and (len(g.sensorDataList)<2)):
            scan_thread = threading.Thread(target=scanBT, daemon=True)
            scan_thread.start()
            g.scannCrono = 0

        # Handle Pygame events
        handlePygameInteraction()

        # Handle Bluetooth connections and data
        handleBTConnections()
        handleBTData()

        # Draw graphics on the screen
        DrawLoop()
        # DrawDebugLayer()

        # Update the Pygame display
        #pygame.display.update()


        # Update Timers
        if(g.isScanning == False):
            if(g.scannCrono < 99):
                g.scannCrono += (time.time() - g.lastLoopTime)
            else:
                g.scannCrono = 0

            g.lastLoopTime = time.time()

  # End of Update() ========================================


# Start the event loop
if __name__ == "__main__":
    Setup()
    Update()
