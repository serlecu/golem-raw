import pygame
from pygame.locals import *
# import math
# import noise


# diametro = 110
# colorDiagrama = (100,100,100)
# grosorDiagrama = 1
# posi_circulo1X = 650
# posi_circulo1Y = 600
# posi_circulo2X = 450
# posi_circulo2Y = 600
# posi_circulo3X = 250
# posi_circulo3Y = 600
# posi_circulo4X = 525
# posi_circulo4Y = 350
# posi_circulo5X = 325
# posi_circulo5Y = 350

pygame.init()

def dib_diagrama( ventana, values:list, pos:tuple[int,int]=(0,0), size:tuple[int,int]=(600,400), radius:int=60, stroke:int=1, color:tuple[int,int,int]=(100,100,100) ):
    #arriba
    posi_circulo1X:int = int( pos[0])
    posi_circulo1Y:int = int( pos[1])
    posi_circulo2X:int = int( pos[0] + size[0]*0.5 - radius )
    posi_circulo2Y:int = int( pos[1])
    posi_circulo3X:int = int( pos[0] + size[0] -radius*2 )
    posi_circulo3Y:int = int( pos[1])
    #bajo
    posi_circulo4X:int = int( pos[0] + radius*1.5 )
    posi_circulo4Y:int = int( pos[1] + size[1]-radius*2 )
    posi_circulo5X:int = int( pos[0] + size[0] - radius*3.5 )
    posi_circulo5Y:int = int( pos[1] + size[1]-radius*2 )

    #global posi_circulo1X, posi_circulo1Y, posi_circulo2X, posi_circulo2Y, posi_circulo3X, posi_circulo3Y, posi_circulo4X, posi_circulo4Y, diametro, colorDiagrama, grosorDiagrama
    #funcion que dibuja circulos
    pygame.draw.ellipse(ventana, (color), (posi_circulo1X, posi_circulo1Y, radius*2, radius*2), stroke)
    pygame.draw.ellipse(ventana, (color), (posi_circulo2X, posi_circulo2Y, radius*2, radius*2), stroke)
    pygame.draw.ellipse(ventana, (color), (posi_circulo3X, posi_circulo3Y, radius*2, radius*2), stroke)
    pygame.draw.ellipse(ventana, (color), (posi_circulo4X, posi_circulo4Y, radius*2, radius*2), stroke)
    pygame.draw.ellipse(ventana, (color), (posi_circulo5X, posi_circulo5Y, radius*2, radius*2), stroke)
    #lineas horizontales
    pygame.draw.aaline(ventana, (color), (posi_circulo1X+radius*2,pos[1]+radius), (posi_circulo2X,pos[1]+radius), 1)
    pygame.draw.aaline(ventana, (color), (posi_circulo2X+radius*2,pos[1]+radius), (posi_circulo3X,pos[1]+radius), 1)
    pygame.draw.aaline(ventana, (color), (posi_circulo4X+radius*2,pos[1]+size[1]-radius), (posi_circulo5X,pos[1]+size[1]-radius), 1)
    # lineas oblicuas
    pygame.draw.aaline(ventana, (color), (posi_circulo1X+radius*1.3, posi_circulo1Y+radius*1.92), (posi_circulo4X+radius*0.5, posi_circulo4Y+radius*0.1), 1)
    pygame.draw.aaline(ventana, (color), (posi_circulo3X+radius*0.6, posi_circulo3Y+radius*1.92), (posi_circulo5X+radius*1.5, posi_circulo5Y+radius*0.1), 1)
    #linea vertical
    pygame.draw.aaline(ventana, (color), (pos[0]+size[0]*0.5, pos[1]+radius*2), (pos[0]+size[0]*0.5, pos[1]+size[1]-radius), 1)
    #fuente
    miFuente = pygame.font.SysFont("Arial", 16)
    minum1 = miFuente.render(str(values[0]),True,(255,255,255))
    minum2 = miFuente.render(str(values[1]),True,(255,255,255))
    minum3 = miFuente.render(str(values[2]),True,(255,255,255))
    minum4 = miFuente.render(str(values[3]),True,(255,255,255))
    minum5 = miFuente.render(str(values[4]),True,(255,255,255))
    minum6 = miFuente.render(str(values[5]),True,(255,255,255))
    minum7 = miFuente.render(str(values[6]),True,(255,255,255))
    minum8 = miFuente.render(str(values[7]),True,(255,255,255))
    minum9 = miFuente.render(str(values[8]),True,(255,255,255))
    minum10 = miFuente.render(str(values[9]),True,(255,255,255))
    # numero bola 1
    ventana.blit( minum1, (posi_circulo1X+radius*0.8, posi_circulo1Y+radius*0.6 ) )
    ventana.blit( minum2, (posi_circulo1X+radius*0.8, posi_circulo1Y+radius) )
    # numero bola 2
    ventana.blit( minum3, (posi_circulo2X+radius*0.8, posi_circulo2Y+radius*0.6 ) )
    ventana.blit( minum4, (posi_circulo2X+radius*0.8, posi_circulo2Y+radius ) )
      # numero bo
    ventana.blit( minum5, (posi_circulo3X+radius*0.8, posi_circulo3Y+radius*0.6 ) )
    ventana.blit( minum6, (posi_circulo3X+radius*0.8, posi_circulo3Y+radius ) )
    # numero bola 4
    ventana.blit( minum7, (posi_circulo4X+radius*0.8, posi_circulo4Y+radius*0.6 ) )
    ventana.blit( minum8, (posi_circulo4X+radius*0.8, posi_circulo4Y+radius ) )
     # numero bola 5
    ventana.blit( minum9, (posi_circulo5X+radius*0.8, posi_circulo5Y+radius*0.6 ) )
    ventana.blit( minum10, (posi_circulo5X+radius*0.8, posi_circulo5Y+radius ) )