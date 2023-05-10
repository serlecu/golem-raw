import pygame
from pygame.locals import *
import math
#import noise
import random

pygame.init()
colorBarras = (255,255,255)
AltoBarras = 6


def dib_barras(ventana):
   
   #barras
   AnchoBarras1:int = int(random.randint(0,400))
   AnchoBarras2:int = int(random.randint(0,400))
   AnchoBarras3:int = int(random.randint(0,400))
   pygame.draw.rect(ventana,colorBarras,pygame.Rect(100,ventana.get_height()-250,AnchoBarras1,AltoBarras,),0)
   pygame.draw.rect(ventana,colorBarras,pygame.Rect(100,ventana.get_height()-225,AnchoBarras2,AltoBarras,),0)
   pygame.draw.rect(ventana,colorBarras,pygame.Rect(100,ventana.get_height()-200,AnchoBarras3,AltoBarras,),0)
   #numeros
   miFuente = pygame.font.SysFont("Arial", 16)
   valorA = str(random.randrange(70,80))
   valorB = str(random.randrange(70,80))
   valorA = miFuente.render(valorA,1,(100,100,100))
   valorB = miFuente.render(valorB,1,(100,100,100))
   ventana.blit(valorA,(100,ventana.get_height()/2+200))
   ventana.blit(valorB,(200,ventana.get_height()/2+200))
    