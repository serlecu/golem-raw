import pygame
from pygame import gfxdraw
import math
import time

import src.globals as g # global variables

def draw_background(screen, color):
    screen.fill(color)

# testing animation
def test_ellipse(screen, color, radius, angle):
    centerX = (int)(screen.get_width()/2)
    centerY = (int)(screen.get_height()/2)
    gfxdraw.aaellipse(screen, centerX, centerY, radius, radius, color)
    gfxdraw.line(screen, centerX, centerY, centerX+(int)(radius*math.cos(angle)), centerY+(int)(radius*math.sin(angle)), (200,200,200))

# testing text
def test_text(screen, text, pos, color):
    font = pygame.font.Font(None, 24)
    text = font.render(text, True, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    screen.blit(text, textpos)



def DrawLoop():
    draw_background(g.screen, (0, 0, 0))
    test_ellipse(g.screen, (200, 200, 200, 100), 200, time.time())
