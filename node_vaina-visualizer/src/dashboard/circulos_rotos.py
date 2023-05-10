import pygame
from pygame.locals import *
# import math
# import noise
import random

pygame.init()

def dib_circulorotos(ventana, values:list, pos:tuple[int,int], size:tuple[int,int], spacer:int=125):
    colorCircle = (255,255,255)
    colorNumeros = (255,255,255)
    miFuente = pygame.font.SysFont("Arial", 11)

    ilen = len(values)
    posx = pos[0] + size[1]*0.5
    posy = pos[1] + size[1]*0.5

    # linea horizontal
    pygame.draw.aaline(ventana,(100,100,100),(pos[0]+size[1]*0.5,posy),(pos[0]+size[0]-size[1]*0.5,posy),1)

    # cada circulo
    for i in range(0, ilen):
        if i == 0:
            sectorX:int
            sectorY:int
            for j in range(0, 4):
                # val = True
                # if values[i][j] == 0:
                #     values[i][j] = False
                valorText = miFuente.render(str(values[i][j]),True,(colorNumeros))
                if j == 0:
                    sectorX = int(posx-size[1]*0.25)
                    sectorY = int(posy+size[1]*0.25)
                elif j == 1:
                    sectorX = int(posx+size[1]*0.25)
                    sectorY = int(posy+size[1]*0.25)
                elif j == 2:
                    sectorX = int(posx-size[1]*0.25)
                    sectorY = int(posy-size[1]*0.25)
                else:
                    sectorX = int(posx+size[1]*0.25)
                    sectorY = int(posy-size[1]*0.25)
                ventana.blit(valorText,(sectorX, sectorY))

        apareceCirculo = random.randrange(-1,2)
        pygame.draw.circle(ventana, colorCircle, (posx, posy), size[1]*0.5, apareceCirculo, bool(values[i][0]), bool(values[i][1]), bool(values[i][2]), bool(values[i][3]))
        posx += size[1]+spacer


    # parteCirculo1 = random.choice([True, False])
    # parteCirculo2 = random.choice([True, False])
    # parteCirculo3 = random.choice([True, False])
    # parteCirculo4 = random.choice([True, False])
    # apareceCirculo1 = random.randrange(-1,2)
    # apareceCirculo2 = random.randrange(-1,2)
    # apareceCirculo3 = random.randrange(-1,2)
    # apareceCirculo4 = random.randrange(-1,2)

     #numeros
    """
    valorA = str(parteCirculo1)
    valorB = str(parteCirculo2)
    valorC = str(parteCirculo3)
    valorD = str(parteCirculo4)

    if valorA == "True" and valorB == "True" and valorC == "True" and valorD == "True":
        valorA = "1"
        valorC = "1"
        valorB = "1"
        valorD = "1"
    else:    
        valorA = "0"
        valorC = "0"
        valorB = "0"
        valorD = "0"
    """
    # valorA = str(values[0][0])
    # valorB = str(values[0][1])
    # valorC = str(values[0][2])
    # valorD = str(values[0][3])
    # valorA = miFuente.render(valorA,True,(colorNumeros))
    # valorB = miFuente.render(valorB,True,(colorNumeros))
    # valorC = miFuente.render(valorC,True,(colorNumeros))
    # valorD = miFuente.render(valorD,True,(colorNumeros))
    # ventana.blit(valorA,(posx-size[0]*0.5, posy+size[1]*0.5))
    # ventana.blit(valorB,(posx+size[0]*0.5, posx+size[0]*0.5))
    # ventana.blit(valorC,(posx-size[0]*0.5, posx-size[0]*0.5))
    # ventana.blit(valorD,(posx+size[0]*0.5, posx-size[0]*0.5))

    #linea horizontal
    pygame.draw.aaline(ventana,(100,100,100),(pos[0],posy),(pos[0]+size[0],posy),1)
    
    # #circulos
    # apareceCirculo1 = random.randrange(-1,2)
    # parteCirculo1 = random.choice([True, False])
    # parteCirculo2 = random.choice([True, False])
    # parteCirculo3 = random.choice([True, False])
    # parteCirculo4 = random.choice([True, False])

    # pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2-250, ventana.get_height()/2+300), 30, apareceCirculo1, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
    # pygame.time.delay(15)
    # apareceCirculo2 = random.randrange(-1,2)
    # parteCirculo1 = random.choice([True, False])
    # parteCirculo2 = random.choice([True, False])
    # parteCirculo3 = random.choice([True, False])
    # parteCirculo4 = random.choice([True, False])

    # pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2-125, ventana.get_height()/2+300), 30, apareceCirculo2, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
    # pygame.time.delay(15)
    # apareceCirculo3 = random.randrange(-1,2)
    # parteCirculo1 = random.choice([True, False])
    # parteCirculo2 = random.choice([True, False])
    # parteCirculo3 = random.choice([True, False])
    # parteCirculo4 = random.choice([True, False])

    # pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2, ventana.get_height()/2+300), 30, apareceCirculo3, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
    # pygame.time.delay(15)
    # apareceCirculo4 = random.randrange(-1,2)
    # parteCirculo1 = random.choice([True, False])
    # parteCirculo2 = random.choice([True, False])
    # parteCirculo3 = random.choice([True, False])
    # parteCirculo4 = random.choice([True, False])
    # pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2+125, ventana.get_height()/2+300), 30, apareceCirculo4, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
   
    
