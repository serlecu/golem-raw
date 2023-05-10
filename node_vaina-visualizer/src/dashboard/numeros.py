import pygame
from pygame.locals import *
# import math
# import noise
import random
import os

pygame.init()

def dib_numero(ventana): 
        num0:str = str(random.randint(0,9))
        num1:str = str(random.randint(0,9))
        numero_carga1 = pygame.transform.scale(pygame.image.load("node_vaina-visualizer/numeros_img/num"+num0+".jpg"), (200, 200))
        numero_carga2 = pygame.transform.scale(pygame.image.load("node_vaina-visualizer/numeros_img/num"+num1+".jpg"), (200, 200))
        pygame.time.delay(20)

        ventana.blit(numero_carga1, (100, 100))
        ventana.blit(numero_carga2, (300, 100))