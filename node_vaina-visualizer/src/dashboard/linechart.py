import pygame
from pygame.locals import *
import random



pygame.init()

def dib_lineapuntos(ventana):
    pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+325,ventana.get_height()/2-350), random.randrange(60,80), 2, False, False, False, True) # hacer cosa con true y false
    pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+325,ventana.get_height()/2-350), random.randrange(60,80), 2, False, False, True, False) #
    pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+325,ventana.get_height()/2-350),(ventana.get_width()/2+325,ventana.get_height()/2-250),1)
    pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+400,ventana.get_height()/2-350), random.randrange(60,80), 2, True, False, False, False) 
    pygame.draw.circle(ventana, (255,255,255), (ventana.get_width()/2+400,ventana.get_height()/2-350), random.randrange(60,80), 2, False, True, False, False) 
    pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+400,ventana.get_height()/2-450),(ventana.get_width()/2+400,ventana.get_height()/2-350),1)
    #linea horizontal
    pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+250,ventana.get_height()/2-350),(ventana.get_width()-200,ventana.get_height()/2-350),1)
    #numeros
    miFuente = pygame.font.SysFont("Arial", 12)
    valor1 = str(random.randrange(70,80))
    valor2 = str(random.randrange(70,80))
    valor1 = miFuente.render(valor1,1,(100,100,100))
    valor2 = miFuente.render(valor2,1,(100,100,100))
    ventana.blit(valor1,(ventana.get_width()/2+475,ventana.get_height()/2-345))
    ventana.blit(valor2,(ventana.get_width()/2+575,ventana.get_height()/2-345))