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
from src.dashboard import * # raw visualization functions

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

randList_9: list[int]


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

    # -- WINDOW A -- (proyector)
    winA = Window("1st window",
                size=(1440,900),
                position=(0, 0) )
    winA.set_fullscreen(True)
    rendererA = Renderer(winA)

    tempSurfaceA = Surface((1440,900))
    tempSurfaceA.fill([255,0,0,255])
    # will use Texture.from_surface() + Texture.draw() to create textures from this surface

    texture = Texture.from_surface(rendererA, tempSurfaceA)
    rendererA.clear()
    texture.draw()
    rendererA.present()

    # -- WINDOW B -- (TV)
    winB = Window("2nd window",
                size=(3840, 2160), # 4K UHD
                position=(1441, 0) )
    winB.set_fullscreen(True)
    rendererB = Renderer(winB)

    tempSurfaceB = Surface((3840, 2160))
    tempSurfaceB.fill([0,255,0,255])
    # will use Texture.from_surface() + Texture.draw() to create textures from this surface

    texture = Texture.from_surface(rendererB, tempSurfaceB)
    rendererB.clear()
    texture.draw()
    rendererB.present()


    


# ====== MAIN GRAPHICS LOOP ====== #

def DrawLoop():
    global onlyOnce, clock, rendererA, rendererB, tempSurfaceA, tempSurfaceB

    if(onlyOnce):
        pass

    clock.tick()
    updateDashboard(rendererB, tempSurfaceB)
    updateProyector(rendererA, tempSurfaceA)
    
    onlyOnce = False


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
    # test_text(surface, str(f"WIN_2 FPS: {round(clock.get_fps(),2)}") , (200,200), (255,255,255))

    randList_1 = random.sample(range(0, 9), 2)
    viz_raw.dib_numero( surface, num=randList_1, pos=(150,200), size=(400,400), spacing=100 )
    randList_2 = random.sample(range(100,800), 5)
    viz_raw.lineasCirculo(surface, values=randList_2, pos=(200,900), size=(800,350), pointSize=10)
    randList_3 = random.sample(range(0,100), 8)
    viz_raw.dib_barras(surface, values=randList_3, pos=(200, 1500), maxWidth=800, stroke=20, spacing=20)

    randList_4 = random.sample(range(20, 100), 14)
    viz_raw.dibujoForma(surface, values=randList_4, pos=(1920, 1080), size=(300,56), stroke=3)
    randList_5 = []
    for i in range(4):
        randList_5.append([ random.randint(0,1),
                            random.randint(0,1),
                            random.randint(0,1),
                            random.randint(0,1) ])
                            # random.choice([True, False]),
                            # random.choice([True, False]),
                            # random.choice([True, False]),
                            # random.choice([True, False]) ])
    viz_raw.dib_circulorotos(surface, values=randList_5, pos=(1510, 1600), size=(900,136), spacer=125)

    randList_6 = random.sample(range(60,80), 4)
    viz_raw.dib_lineapuntos(surface, values=randList_6, pos=(2700, 200), size=(800,400) )
    randList_7 = ( random.randint(0,100)/100,
                   random.randint(0,100)/100,
                   random.randint(0,100)/100,
                   random.randint(2,5) )
        #random.sample(range(60,80), 4)
    viz_raw.dib_particulas(surface, pos=(2700, 800), size=(900, 400), stroke=1, newParticle=randList_7)
    randList_8 = random.sample(range(60,80), 4)
    viz_raw.dib_diagrama(surface)

    # create texture from surface and render it to its window
    texture = Texture.from_surface(renderer, surface)
    renderer.clear()
    texture.draw()
    renderer.present()


def updateProyector(renderer, surface):
    global clock, onlyOnce, randList_9

    if(onlyOnce):
        randList_9 = random.sample(range(0, 100), 1)

    # clean background
    surface.fill([0,0,0,255])
    # draw graphics into surface
    test_text(surface, str(f"WIN_1 FPS: {round(clock.get_fps(),2)}") , (200,200), (255,255,255))

    for i in range(len(randList_9)):
        if random.randint(0,100) < 5:
            randList_9[i] = random.randint(0,100)
    viz_raw.dib_imag_estructura(surface, values=randList_9 ,pos=(700,100), size=(600,600), spacing=100, mode=1)
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

