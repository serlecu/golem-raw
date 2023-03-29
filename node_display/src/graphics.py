import pygame
import math

def draw_background(screen, color):
    screen.fill(color)

# testing method that drawas an animated ellipse
# it rotates around center of screen at given radius
def test_ellipse(screen, color, radius, angle):
    pygame.draw.ellipse(screen, color, (240-radius, 240-radius, radius*2, radius*2), 0)
    pygame.draw.ellipse(screen, (0,0,0), (240-radius, 240-radius, radius*2, radius*2), 1)
    pygame.draw.line(screen, (0,0,0), (240, 240), (240+radius*math.cos(angle), 240+radius*math.sin(angle)), 1)



