import time
import threading

from src.golemSerial import *
from src.graphics import *
from src.debugInDisplay import *

def Setup():
    import src.globals as g

    g.initGlobals()

    # Open Serial Port
    openSerial()

    # Initialize Pygame
    # setupSimplePygame(g.screen)
    setupScreens()

    serialThread = threading.Thread(target=handleSerialThread, daemon=True)
    serialThread.start()

    # End of Setup() ========================================


def Update():
    import src.globals as g

    while True:

        # Handle Pygame events
        handlePygameInteraction()

        # Handle Serial Reading
        # handleSerial()

        # Draw graphics on the screen
        DrawLoop()
        # DrawDebugLayer()

        g.dashboardCrono += time.time() - g.lastLoopTime
        if(g.dashboardCrono > 99):
            g.dashboardCrono = 0
        g.lastLoopTime = time.time()

  # End of Update() ========================================


# Start the event loop
if __name__ == "__main__":
    Setup()
    Update()
