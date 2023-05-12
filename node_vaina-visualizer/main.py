import time

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
    # setupScreens()

    # End of Setup() ========================================

def Update():
    import src.globals as g

    while True:

        # Handle Pygame events
        # handlePygameInteraction()

        # Handle Serial Reading
        readSerial()

        # Draw graphics on the screen
        # DrawLoop()
        # DrawDebugLayer()

        g.lastLoopTime = time.time()

  # End of Update() ========================================


# Start the event loop
if __name__ == "__main__":
    Setup()
    Update()
