import pygame
from pygame.locals import *
# import math
# import noise
import random
# import threading
# import time
import os

pygame.init()


num0:str = str(random.randint(0,9))
num1:str = str(random.randint(0,9))
veces:int = 0


def dib_imag_estructura(ventana, values:list[int], pos:tuple=(0,0), size:tuple=(1920,1080), spacing:int=0, mode:int=0):
    global num0, num1
    files = os.listdir("node_vaina-visualizer/estructura_img")
    ilen = len(values)

    if mode == 1: # centered
        xpos = pos[0] - (ilen*size[0]+(ilen-1)*spacing)/2
    elif mode == 2: # right
        xpos = pos[0] - (ilen-1)*(size[0]+spacing)
    else: # left
        xpos = pos[0]

    for i in range(0, ilen):
        filename:str = files[values[i] % len(files)]
        print(filename)

        img = pygame.image.load("node_vaina-visualizer/estructura_img/"+ filename )
        surface = pygame.transform.scale( img, (size[0], size[1]) )
        ventana.blit(surface, (xpos+i*(size[0]+spacing), pos[1]))

    # imagen_carga1 = pygame.transform.scale(pygame.image.load("node_vaina-visualizer/estructura_img/img"+num0+".jpg"), (200, 200))
    # imagen_carga2 = pygame.transform.scale(pygame.image.load("node_vaina-visualizer/estructura_img/img"+num1+".jpg"), (200, 200))
    # ventana.blit(imagen_carga1,(ventana.get_width()/2-300, 100))
    # ventana.blit(imagen_carga2,(ventana.get_width()/2-50, 100))
    