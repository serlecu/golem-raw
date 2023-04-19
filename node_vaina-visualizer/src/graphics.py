import pygame
from pygame import gfxdraw
from pygame.locals import *
# import noise

import math
import time
import random

import src.globals as g # global variables

onlyOnce = True

def draw_background(screen, color):
    screen.fill(color)

# testing animation
def test_ellipse(screen, color, radius, angle):
    centerX = (int)(screen.get_width()/2)
    centerY = (int)(screen.get_height()/2)
    gfxdraw.aaellipse(screen, centerX, centerY, radius, radius, color)
    gfxdraw.line(screen, centerX, centerY, centerX+(int)(radius*math.cos(angle)), centerY+(int)(radius*math.sin(angle)), (0,0,0))

# testing text
def test_text(screen, text, pos, color):
    font = pygame.font.Font(None, 24)
    text = font.render(text, True, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    screen.blit(text, textpos)

# ==== Unknown Pleasure diagram ====
window_size = (0, 0)
inset = 0
_len = 0
rRes = 0
angInc = 2

points = []
radiusOffset = 0
noiseOff = 0
img: pygame.Surface
imgOpc: pygame.Surface


def setupUnknownPleasure(screen):
    global inset, _len, rRes, angInc, points, radiusOffset, noiseOff, img, imgOpc, window_size

    _len = min(pygame.display.Info().current_w, pygame.display.Info().current_h) - 40
    window_size = (_len, _len)
    inset = _len / 10
    rRes = 10

    img = pygame.Surface((_len, _len))
    imgOpc = pygame.Surface((_len, _len), pygame.SRCALPHA)
    noiseOff = round(random.randint(0, 10000))
    radiusOffset = ((_len / 2) - 4 * inset) / rRes

    startCol = pygame.Color("#010B34")
    endCol = pygame.Color('#210134')
    startOpc = pygame.Color("#010B34dd")
    endOpc = pygame.Color('#210134dd')

    img.fill(pygame.Color("#000000"))
    imgOpc.fill(pygame.Color("#00000000"))

    for y in range(_len):
        for x in range(_len):
            img.set_at((x, y), startCol.lerp(endCol, y / _len))
            imgOpc.set_at((x, y), startOpc.lerp(endOpc, y / _len))

    pygame.display.flip()

    # pygame.gl.glMatrixMode(pygame.gl.GL_TEXTURE)
    # pygame.gl.glScalef(1.0 / _len, 1.0 / _len, 1.0)

    initRadial(screen)


def initRadial(screen):
    global points, _len, window_size, inset, radiusOffset, angInc

    for r in range(int(window_size[0] / 2 - 2 * inset), int(1.5 * inset), int(-radiusOffset)):
        ring = []
        for a in range(0, 360, int(math.pi*2)): 
            # noiseVal = noise.snoise3(r * math.cos(math.radians(a + math.radians(noiseOff) * (math.radians(60))) / 20),
            #                          r * math.sin(math.radians(a + math.radians(noiseOff) * (math.radians(60))) / 20),
            #                          0,
            #                          octaves=6)
            noiseVal = random.random()
            rOff = map_value(noiseVal, 0.0, 1.0, 0, _len / 5)
            aOff = ( a + float(map_value(r, (2 * inset), (window_size[0] / 2 - 1.5 * inset), 0, (math.pi / 2.0)) ) )
            ring.append(pygame.math.Vector2(aOff, rOff))
        points.append(ring)


def UpdateUnknownPleasure(screen):
    global angInc, noiseOff, points, radiusOffset, img, imgOpc, window_size, _len

    screen.blit(img, (0, 0), (0, 0, window_size[0], window_size[1]))
    UPRadial(screen)
    noiseOff += 1


def UPRadial(screen):
    global angInc, noiseOff, points, radiusOffset, img, imgOpc, window_size, _len

    for i in range(len(points)):
        z = 0
        ring = points[i]
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect(), 0)  # clear the screen
        for a in range(0, 361, angInc):
            r = window_size[0] / 2 - 2 * inset - i * radiusOffset
            speed = int((i + len(points)) / len(points)) * noiseOff
            ringIndex = int(a / angInc + speed) % int(360 / angInc) -1
            print(f"ring size: {len(ring)}, index: {ringIndex}")
            rOff = ring[ringIndex % len(ring)].y
            newR = r + rOff * math.pow(map_value(math.cos(math.radians(ring[int(a / angInc) % int(360 / angInc)].x)), -1, 1, 0, 1), 2)
            x = newR * math.cos(math.radians(a)) + window_size[0] / 2
            y = newR * math.sin(math.radians(a)) + window_size[1] / 2
            pygame.draw.aaline(screen, (255, 255, 255), (x, y), (window_size[0] / 2, window_size[1] / 2), 1)
            tex_x = x / window_size[0]
            tex_y = y / window_size[1]
            pygame.draw.circle(screen, imgOpc.get_at((int(tex_x * img.get_width()), int(tex_y * img.get_height()))), (int(x), int(y)), 1)
        z += 1

def map_value(value, from_low, from_high, to_low, to_high):
    """
    Maps a value from one range to another.
    
    Args:
        value (float): The value to be mapped.
        from_low (float): The lower bound of the original range.
        from_high (float): The upper bound of the original range.
        to_low (float): The lower bound of the target range.
        to_high (float): The upper bound of the target range.
        
    Returns:
        float: The mapped value in the target range.
    """
    from_range = from_high - from_low
    to_range = to_high - to_low
    value_scaled = (value - from_low) / from_range
    mapped_value = to_low + (value_scaled * to_range)
    return mapped_value


# ====== MAIN ====== #

def DrawLoop():
    global onlyOnce

    if(onlyOnce):
        onlyOnce = False
        setupUnknownPleasure(g.screen)

    draw_background(g.screen, (50, 50, 50))
    test_ellipse(g.screen, (200, 200, 200), 200, time.time())
    # UpdateUnknownPleasure(g.screen)

