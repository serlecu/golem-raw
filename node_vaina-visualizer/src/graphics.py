import pygame
from pygame import gfxdraw
#from pygame.locals import *
from pygame import Surface
from pygame._sdl2 import Window, Texture, Renderer
from pygame.font import Font

# import noise
import math
import time
import random

import src.globals as g # global variables

# global variables
clock = pygame.time.Clock()
winA : Window
winB : Window
rendererA : Renderer
rendererB : Renderer
tempSurfaceA : Surface
tempSurfaceB : Surface

onlyOnce = True
running = True


# ====== SETUP ====== #

def setupSimplePygame(surface):
    # Initialize Pygame
    pygame.init()

    surface = pygame.display.set_mode((1080,720))
    pygame.display.set_caption("Golem: Vaina Visualizer")
    pygame.mouse.set_visible(False)


# pygame setup for dual screen
def setupScreens():
    global winA, winB, rendererA, rendererB, tempSurfaceA, tempSurfaceB
    pygame.font.init()
    pygame.display.init()
    pygame.key.set_repeat(1000, 10)

    # -- WINDOW 1 --
    winA = Window("1st window",
                size=(1440,900),
                position=(0, 400) )
    winA.set_fullscreen(True)
    rendererA = Renderer(winA)

    rendererA.draw_color = (0,0,0,255)
    rendererA.clear()
    rendererA.present()

    # -- WINDOW 2 --
    winB = Window("2nd window",
                size=(2560, 1440),
                position=(1441, 400) )
    winB.set_fullscreen(True)
    rendererB = Renderer(winB)

    rendererB.draw_color = (0,0,0,0)
    rendererB.clear()
    rendererB.present()

    tempSurfaceA = Surface((1440,900))
    tempSurfaceA.fill([0,0,0,])
    tempSurfaceB = Surface((2560,1440))
    tempSurfaceB.fill([0,0,0,])
    # will use Texture.from_surface() + Texture.draw() to create textures from this surface


# ====== MAIN GRAPHICS LOOP ====== #

def DrawLoop():
    global onlyOnce, rendererA, rendererB, tempSurfaceA, tempSurfaceB

    if(onlyOnce):
        onlyOnce = False

    clock.tick()
    updateDashboard(rendererB, tempSurfaceB)
    updateProyector(rendererA, tempSurfaceA)

    # draw_background(g.screen, (50, 50, 50))
    # test_ellipse(g.screen, (200, 200, 200), 200, time.time())
    # UpdateUnknownPleasure(g.screen)


# ====== LOOP FUNCS ====== #

def handlePygameInteraction(): # ON MAIN LOOP
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


def updateDashboard(renderer, surface):
    global clock

    # clean background
    surface.fill([0,0,0,255])
    # draw graphics into surface
    test_text(surface, str(f"WIN_2 FPS: {round(clock.get_fps(),2)}") , (200,200), (255,255,255))
    # viz_raw.lineasCirculo(surface)
    # # viz_raw.dibujoForma(ventana,fm.id, fm.upSp, fm.dr) # en forma_movi
    # viz_raw.dib_diagrama(surface)
    # viz_raw.dib_barras(surface)
    # viz_raw.dib_numero(surface)
    # viz_raw.dib_particulas(surface)
    # viz_raw.dib_lineapuntos(surface)
    # viz_raw.dib_circulorotos(surface)
    # create texture from surface and render it to its window
    texture = Texture.from_surface(renderer, surface)
    renderer.clear()
    texture.draw()
    renderer.present()


def updateProyector(renderer, surface):
    global clock

    # clean background
    surface.fill([0,0,0,255])
    # draw graphics into surface
    test_text(surface, str(f"WIN_1 FPS: {round(clock.get_fps(),2)}") , (200,200), (255,255,255))
    # viz_raw.dib_imag_estructura(surface)
    # create texture from surface and render it to its window
    texture = Texture.from_surface(renderer, surface)
    renderer.clear()
    texture.draw()
    renderer.present()


# ====== HELPER FUNCS ====== #

def draw_background(surface, color):
    surface.fill(color)

# testing animation
def test_ellipse(surface, color, radius, angle):
    centerX = (int)(surface.get_width()/2)
    centerY = (int)(surface.get_height()/2)
    gfxdraw.aaellipse(surface, centerX, centerY, radius, radius, color)
    gfxdraw.line(surface, centerX, centerY, centerX+(int)(radius*math.cos(angle)), centerY+(int)(radius*math.sin(angle)), (0,0,0))

# testing text
def test_text(surface, text, pos, color):
    font = Font(None, 24)
    text = font.render(text, True, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    surface.blit(text, textpos)

