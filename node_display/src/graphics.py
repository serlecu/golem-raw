import pygame
from pygame import gfxdraw
import math

def draw_background(screen, color):
    screen.fill(color)

# testing method: drawas an animated ellipse
# it rotates around center of screen at given radius
def test_ellipse(screen, color, radius, angle):
    centerX = (int)(screen.get_width()/2)
    centerY = (int)(screen.get_height()/2)
    gfxdraw.aaellipse(screen, centerX, centerY, radius, radius, color)
    gfxdraw.line(screen, centerX, centerY, centerX+(int)(radius*math.cos(angle)), centerY+(int)(radius*math.sin(angle)), (0,0,0))

# testing method: overlay text
# draws a given text at given position
def test_text(screen, text, pos, color):
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    screen.blit(text, textpos)


