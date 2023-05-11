import pygame
from pygame.locals import *

pygame.init()

def dib_numero(ventana, num:list[int], pos:tuple[int,int], size:tuple[int,int]=(200,200), spacing:int=0): 
        for n in range(0,len(num)):
                img = pygame.image.load("node_vaina-visualizer/numeros_img/num"+str(num[n])+".png")
                numero_carga1 = pygame.transform.scale(img, size)
                ventana.blit(numero_carga1, (pos[0]+(n*(size[0]) + spacing), pos[1]))