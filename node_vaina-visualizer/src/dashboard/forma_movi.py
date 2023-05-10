import pygame
# import random
import math
import noise
from pygame.locals import *
pygame.init()

h = 60
id = 18
upSp = 80
dr = 2 * math.pi / id

def dibujoForma(ventana,id,upSp,dr):
    global h
    d = 0
    points = []
    for i in range(0, id+5):
        ind = i%id
        a = dr * ind
        d = 150 + noise.pnoise1(h/upSp + ind, octaves=4) * 100  +  math.cos(ind) * 7
        x = math.cos(a)*d + ventana.get_width()/2 - 75
        y = math.sin(a)*d + ventana.get_height()/2
        points.append((x, y))
    pygame.draw.aalines(ventana, (255, 255, 255), False, points, blend=2) 
    h+=2