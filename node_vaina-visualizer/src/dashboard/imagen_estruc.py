import pygame
from pygame.locals import *
# import math
# import noise
import random
# import threading
# import time
# import os

pygame.init()


num0:str = str(random.randint(0,9))
num1:str = str(random.randint(0,9))
veces:int = 0


def dib_imag_estructura(ventana):
    global num0, num1, veces
    veces += 1
    if veces == 25:
        num0 = str(random.randint(0,9))       
    if veces == 30:
        num1 = str(random.randint(0,9))  
    if veces >= 100:
        veces = 0
    imagen_carga1 = pygame.transform.scale(pygame.image.load("node_vaina-visualizer/estructura_img/img"+num0+".jpg"), (200, 200))
    imagen_carga2 = pygame.transform.scale(pygame.image.load("node_vaina-visualizer/estructura_img/img"+num1+".jpg"), (200, 200))
    ventana.blit(imagen_carga1,(ventana.get_width()/2-300, 100))
    ventana.blit(imagen_carga2,(ventana.get_width()/2-50, 100))
    