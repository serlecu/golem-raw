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
import noise

import src.globals as g # global variables
# from src.dashboard import * # raw visualization functions
import src.dashboard as db

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

totalSlides: int = 23
slidesFreq: float = 3
slidesCrono: float = 0
slidesUrn: list[int] = []
slideNumber: int = 0

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
    global onlyOnce, clock, rendererA, rendererB, tempSurfaceA, tempSurfaceB, slidesFreq, slidesCrono

    if(onlyOnce):
        pass

    clock.tick()
    updateDashboard(rendererB, tempSurfaceB)
    updateProyector(rendererA, tempSurfaceA)
    
    # Rise onlyOnce flag
    if(onlyOnce):
        onlyOnce = False

    # Update Timers
    if(slidesCrono < slidesFreq):
        slidesCrono += (time.time() - g.lastLoopTime) # not the best but reuses a variable


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
    # --- COLUMNA 1 --- #
    digitsList = []
    if g.noDataMode:
        digitsList = random.sample(range(0, 9), 2)
    else:
        digitsList = [int(i) for i in f"{int(g.scannCrono):02d}"]
    db.dib_numero( surface, num=digitsList[:2], pos=(150,200), size=(400,400), spacing=100 )
    
    accel_data = []
    if g.noDataMode:
        accel_data = random.sample(range(0,800), 5)
    else:
        for sensor in g.sensorDataList:
            for value in sensor.getAccelerometer():
                mapValue = abs(value)  # form -1./+1. to 0./+1.
                accel_data.append(mapValue)
    db.dib_sliders(surface, values=accel_data, pos=(200,900), size=(800,350), pointSize=10, vSpacing=50)
    
    lux_data = []
    if g.noDataMode:
        lux_data = random.sample(range(0,255), 8)
    else:
        for sensor in g.sensorDataList:
            for value in sensor.getLight():
                lux_data.append(value)
    db.dib_barras(surface, values=lux_data, pos=(200, 1500), maxWidth=800, stroke=20, spacing=20)

    # --- COLUMNA 2 --- #
    proximity_data = []
    if g.noDataMode:
        proximity_data = random.sample(range(0, 300), 3)
    else:
        for sensor in g.sensorDataList:
            proximity_data.append(sensor.getProximity())
    db.dib_arcos_sup(surface, values=proximity_data, pos=(1510, 200), size=(800,100))
    
    rssi_data:list[float] = []
    if g.noDataMode:
        rssi_data = random.sample(range(20, 100), 2)
    else:
        for sensor in g.sensorDataList:
            mapValue = abs(sensor.getRSSI()) / 120.0 # map to 0.-1.
            rssi_data.append(mapValue)
    db.dibujoForma(surface, values=rssi_data, pos=(1920, 1000), size=300, amp=56, stroke=3)
    
    ire_data = []
    if g.noDataMode:
        for i in range(4):
            ire_data.append([ random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1) ])
    else:
        for sensor in g.sensorDataList:
            ire_data.append(sensor.getImpulseResponse())
    db.dib_circulorotos(surface, values=ire_data, threshold=200, pos=(1510, 1600), size=(900,136), spacer=125)

    # --- COLUMNA 3 --- #
    gyro_data = []
    if g.noDataMode:
        gyro_data = random.sample(range(60,80), 4)
    else:
        for sensor in g.sensorDataList:
            for value in sensor.getGyroscope():
                mapValue = (value+0.5)*100 # map -0.5-+0.5 to 0-100
                gyro_data.append(mapValue)
    db.dib_lineapuntos(surface, values=gyro_data, pos=(2700, 200), size=(800,400) )

    magnet_data = []
    if g.noDataMode:
        magnet_data.append( [ float(random.randint(0,100)/100.0), float(random.randint(0,100)/100.0), float(random.randint(0,100)/100.0) ] )
        magnet_data.append( [ float(random.randint(0,100)/100.0), float(random.randint(0,100)/100.0), float(random.randint(0,100)/100.0) ] )
    else:
        for sensor in g.sensorDataList:
            mapData:list = []
            for value in sensor.getMagnetometer():
                mapValue = float((value+100.0)/200) # map -100./+100 to 0.-100
                mapData.append(mapValue)
            magnet_data.append(mapData)
    db.dib_particulas(surface, values=magnet_data, pos=(2700, 800), size=(900, 400), scale=(1.0,1.0), stroke=1)

    atmos_data = []
    if g.noDataMode:
        atmos_data = random.sample(range(0, 255), 10)
    else:
        for sensor in g.sensorDataList:
            atmos_data.append(sensor.getTemp())
            atmos_data.append(sensor.getHumidity())
            atmos_data.append(sensor.getPressure())
    db.dib_diagrama(surface, values=atmos_data, pos=(2900, 1400), size=(600, 400), radius=70, stroke=1)

    # create texture from surface and render it to its window
    texture = Texture.from_surface(renderer, surface)
    renderer.clear()
    texture.draw()
    renderer.present()


def updateProyector(renderer, surface):
    global clock, onlyOnce, slidesCrono, slidesFreq, slidesUrn, slideNumber, totalSlides

    if(onlyOnce):
        randList_9 = random.sample(range(0, 100), 1)

    # clean background
    surface.fill([0,0,0,255])
    # draw graphics into surface
    # test_text(surface, str(f"WIN_1 FPS: {round(clock.get_fps(),2)}") , (200,200), (255,255,255))

    # Random pick a img number to change
    if (slidesCrono >= slidesFreq):
        slideNumber = random.randint(0, totalSlides-1)
        while slideNumber in slidesUrn:
            slideNumber = random.randint(0, totalSlides-1)
        slidesUrn.append(slideNumber)
        if len(slidesUrn) >= totalSlides:
            slidesUrn = []
        slidesCrono = 0
    db.dib_imag_estructura(surface, values=slideNumber, pos=(surface.get_width(),0), size=(600,600), spacing=50, mode=2)
    db.sensor_table(surface, values=g.sensorDataList, pos=(0, 0), spacing=(200,30))

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

