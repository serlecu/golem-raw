import pygame
from pygame.locals import *
import random



pygame.init()

def dib_lineapuntos(ventana, values:list, pos:tuple[int,int], size:tuple[int,int]):
    font = pygame.font.SysFont("Arial", 24)

    posx = pos[0] + size[0]*0.2
    posy = pos[1] + size[1]*0.5
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), values[0], 2, False, False, False, True) # hacer cosa con true y false
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), values[1], 2, False, False, True, False) #
    pygame.draw.aaline(ventana, (100,100,100), (posx,posy), (posx,posy+size[1]*0.5), 1)
    
    posx = pos[0]+size[0]*0.4
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), values[2], 2, True, False, False, False) 
    pygame.draw.circle(ventana, (255,255,255), (posx,posy), values[3], 2, False, True, False, False) 
    pygame.draw.aaline(ventana, (100,100,100), (posx,posy), (posx,posy-size[1]*0.5), 1)
    
    textValue1 = font.render(str(values[0]),True,(100,100,100))
    textValue2 = font.render(str(values[1]),True,(100,100,100))
    ventana.blit( textValue1, (pos[0]+size[0]*0.6, posy + 24))
    ventana.blit( textValue2, (pos[0]+size[0]*0.8, posy + 24))

    pygame.draw.aaline(ventana, (100,100,100), (pos[0], posy), (pos[0]+size[0], posy), 1)






    # pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+325,ventana.get_height()/2-350), random.randrange(60,80), 2, False, False, False, True) # hacer cosa con true y false
    # pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+325,ventana.get_height()/2-350), random.randrange(60,80), 2, False, False, True, False) #
    # pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+325,ventana.get_height()/2-350),(ventana.get_width()/2+325,ventana.get_height()/2-250),1)
    # pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+400,ventana.get_height()/2-350), random.randrange(60,80), 2, True, False, False, False) 
    # pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+400,ventana.get_height()/2-350), random.randrange(60,80), 2, False, True, False, False) 
    # pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+400,ventana.get_height()/2-450),(ventana.get_width()/2+400,ventana.get_height()/2-350),1)
    
    # #linea horizontal
    # pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+250,ventana.get_height()/2-350),(ventana.get_width()-200,ventana.get_height()/2-350),1)
    # #numeros
    # miFuente = pygame.font.SysFont("Arial", 12)
    # valor1 = str(random.randrange(70,80))
    # valor2 = str(random.randrange(70,80))
    # valor1 = miFuente.render(valor1,True,(100,100,100))
    # valor2 = miFuente.render(valor2,True,(100,100,100))
    # ventana.blit(valor1,(ventana.get_width()/2+475,ventana.get_height()/2-345))
    # ventana.blit(valor2,(ventana.get_width()/2+575,ventana.get_height()/2-345))