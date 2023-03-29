import time
import os
import pygame

from src.bluetooth import *
from src.graphics import *

# Initialize Pygame
os.environ["DISPLAY"] = ":0"
pygame.init()

# Set up the Pygame display
screen = pygame.display.set_mode((480,480),pygame.FULLSCREEN)
pygame.display.set_caption("Golem: Display Node")
pygame.mouse.set_visible(False)

# Initialize the Bluetooth client

# Scan for Bluetooth devices
foundDevices = scanBT()

# Main loop
while True:
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

    # Draw graphics on the screen
    draw_background(screen, (50, 50, 50))
    test_ellipse(screen, (200, 200, 200), 200, time.time())

    #test_text(screen, "Hello World!", (240, 240), (255, 255, 255))
    debugScannedDevices(foundDevices, screen)

    # Update the Pygame display
    pygame.display.update()

    # Send and receive data from the Bluetooth device


    