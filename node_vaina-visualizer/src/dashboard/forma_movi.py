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

def dibujoForma(ventana, values:list[int], pos:tuple[int,int], size:tuple[int,int]=(150,100), stroke:int=1, upSp=80):
    global h
    d = 0
    id = len(values)
    dr = 2 * math.pi / id

    for j in range(0,stroke):
        points = []
        for i in range(0, id+1): #range(0, id+5):
            ind = i%id
            # angle
            a = dr * ind
            # diameter (size[0]=outer, size[1]=inner)
            #d = (size[0] + noise.pnoise1(h/upSp + ind, octaves=4) * size[1]  +  math.cos(ind) * 7) + j
            d = (size[0] + (values[ind]/100) * size[1]  +  math.cos(ind) * 7) + j
            # position
            x = math.cos(a)*d + pos[0]
            y = math.sin(a)*d + pos[1]
            points.append((x, y))
        color = int(255/stroke * j)
        pygame.draw.aalines(ventana, (color, color, color), False, points, blend=2) 
        h+=2