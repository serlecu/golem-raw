import pygame
import random
import os

# pygame.init()


num0:str = str(random.randint(0,9))
num1:str = str(random.randint(0,9))
veces:int = 0


def dib_imag_estructura(ventana, values:int, pos:tuple=(0,0), size:tuple=(1920,1080), spacing:int=0, mode:int=0):
    global num0, num1
    files = os.listdir("/Users/golem/Desktop/golem-node-screen/node_vaina-visualizer/estructura_img")
    if ".DS_Store" in files:
        files.remove(".DS_Store")

    if mode == 1: # centered
        xpos = pos[0] - size[0]/2
    elif mode == 2: # right
        xpos = pos[0] - size[0]
    else: # left
        xpos = pos[0]

    filename:str = files[values % len(files)]
    img = pygame.image.load("/Users/golem/Desktop/golem-node-screen/node_vaina-visualizer/estructura_img/"+ filename )
    surface = pygame.transform.scale( img, (size[0], size[1]) )
    ventana.blit(surface, (xpos, pos[1]))

    # ilen = len(values)

    # if mode == 1: # centered
    #     xpos = pos[0] - (ilen*size[0]+(ilen-1)*spacing)/2
    # elif mode == 2: # right
    #     xpos = pos[0] - (ilen-1)*(size[0]+spacing)
    # else: # left
    #     xpos = pos[0]

    # Multi img version
    # for i in range(0, ilen):
    #     filename:str = files[values[i] % len(files)]
    #     img = pygame.image.load("node_vaina-visualizer/estructura_img/"+ filename )
    #     surface = pygame.transform.scale( img, (size[0], size[1]) )
    #     ventana.blit(surface, (xpos+i*(size[0]+spacing), pos[1]))
    