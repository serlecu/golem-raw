import pygame
from pygame.locals import *
import random



pygame.init()

def dib_lineapuntos(ventana, values:list, pos:tuple[int,int], size:tuple[int,int]):
    font = pygame.font.SysFont("Arial", 24)
    
    if len(values) < 6:
        for i in range(6-len(values)):
            values.append(0)
    # print(values)

    posx = pos[0] + size[0]*0.2
    posy = pos[1] + size[1]*0.5
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), int(values[0]), 2, False, False, False, True) # hacer cosa con true y false
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), int(values[1]), 2, False, False, True, False) #
    pygame.draw.aaline(ventana, (100,100,100), (posx,posy), (posx,posy+size[1]*0.5), 1)
    
    posx = pos[0]+size[0]*0.4
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), int(values[3]), 2, True, False, False, False) 
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), int(values[4]), 2, False, True, False, False) 
    pygame.draw.aaline(ventana, (100,100,100), (posx,posy), (posx,posy-size[1]*0.5), 1)
    
    textValue1 = font.render(str(round(values[2],2)),True,(100,100,100))
    textValue2 = font.render(str(round(values[5],2)),True,(100,100,100))
    ventana.blit( textValue1, (pos[0]+size[0]*0.6, posy + 24))
    ventana.blit( textValue2, (pos[0]+size[0]*0.8, posy + 24))

    pygame.draw.aaline(ventana, (100,100,100), (pos[0], posy), (pos[0]+size[0], posy), 1)