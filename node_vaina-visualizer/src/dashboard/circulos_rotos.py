import pygame
import random

pygame.init()

def dib_circulorotos(ventana, values:list, thresholds:tuple[int,int], pos:tuple[int,int], size:tuple[int,int], spacer:int=125):
    colorCircle = (255,255,255)
    colorNumeros = (255,255,255)
    miFuente = pygame.font.SysFont("Arial", 11)

    # rellenar valores ausentes
    if len(values) < 2:
        for i in range(2-len(values)):
            values.append([0,0,0,0, 0,0,0,0])
    for sensor in values:
        if len(sensor) < 8:
            for i in range(8-len(sensor)):
                sensor.append(0)

    ilen = len(values)
    posx = pos[0] + size[1]*0.5
    posy = pos[1] + size[1]*0.5

    # linea horizontal
    pygame.draw.aaline(ventana,(100,100,100),(pos[0]+size[1]*0.5,posy),(pos[0]+size[0]-size[1]*0.5,posy),1)

    # cada circulo
    for i in range(0, ilen):
        # línea vertical
        pygame.draw.aaline(ventana,(100,100,100),(posx,posy-size[1]*0.5),(posx,posy+size[1]*0.5),1)
        
        #texto
        if i == 0:
            sectorX:int
            sectorY:int
            for j in range(0, 4):
                val = random.randint(0,1)
                valorText = miFuente.render(str(val),True,(colorNumeros))
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

        # ellipse 1/2
        apareceCirculo = random.randrange(-1,2)
        pygame.draw.circle(ventana, colorCircle, (posx, posy), size[1]*0.5, apareceCirculo, bool(values[i][0]), bool(values[i][1]), bool(values[i][2]), bool(values[i][3]))
        posx += size[1]+spacer
        
        # ellipse 2/2
        apareceCirculo = random.randrange(-1,2)
        pygame.draw.circle(ventana, colorCircle, (posx, posy), size[1]*0.5, apareceCirculo, bool(values[i][4]), bool(values[i][5]), bool(values[i][6]), bool(values[i][7]))
        posx += size[1]+spacer

    #linea horizontal
    # pygame.draw.aaline(ventana,(100,100,100),(pos[0],posy),(pos[0]+size[0],posy),1)
