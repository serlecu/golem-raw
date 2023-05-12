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
    ilen = len(values)
    if ilen < 6:
      for i in range(6-len(values)):
            values.append(0)
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
    minum2 = miFuente.render(str(values[3]),True,(255,255,255))
    minum3 = miFuente.render(str(values[2]),True,(255,255,255))
    minum4 = miFuente.render(str(values[5]),True,(255,255,255))
    minum5 = miFuente.render(str(values[1]),True,(255,255,255))
    minum6 = miFuente.render(str(values[4]),True,(255,255,255))
    minum7 = miFuente.render(str(round(round(float(values[2])+float(values[0])/2.0,2))),True,(255,255,255))
    minum8 = miFuente.render(str(round(round(float(values[5])+float(values[3])/2,2))),True,(255,255,255))
    minum9 = miFuente.render(str(round(round(float(values[2])+float(values[1])/2,2))),True,(255,255,255))
    minum10 = miFuente.render(str(round(round(float(values[5])+float(values[4])/2,2))),True,(255,255,255))



    # numero bola 1
    textpos = minum1.get_rect()
    textpos.centerx = int(posi_circulo1X+radius*1.0)
    textpos.centery = int(posi_circulo1Y+radius*0.7)
    ventana.blit( minum1, textpos )
    textpos = minum2.get_rect()
    textpos.centerx = int(posi_circulo1X+radius*1.0)
    textpos.centery = int(posi_circulo1Y+radius*1.2)
    ventana.blit( minum2, textpos)
    # numero bola 2
    textpos = minum3.get_rect()
    textpos.centerx = int(posi_circulo2X+radius*1.0)
    textpos.centery = int(posi_circulo2Y+radius*0.7)
    ventana.blit( minum3, textpos )
    textpos = minum4.get_rect()
    textpos.centerx = int(posi_circulo2X+radius*1.0)
    textpos.centery = int(posi_circulo2Y+radius*1.2)
    ventana.blit( minum4, textpos )
      # numero bo
    textpos = minum5.get_rect()
    textpos.centerx = int(posi_circulo3X+radius*1.0)
    textpos.centery =  int(posi_circulo3Y+radius*0.7)
    ventana.blit( minum5, textpos)
    textpos = minum6.get_rect()
    textpos.centerx = int(posi_circulo3X+radius*1.0)
    textpos.centery = int(posi_circulo3Y+radius*1.2)
    ventana.blit( minum6, textpos )
    # numero bola 4
    textpos = minum7.get_rect()
    textpos.centerx = int(posi_circulo4X+radius*1.0)
    textpos.centery =  int(posi_circulo4Y+radius*0.7)
    ventana.blit( minum7, textpos)
    textpos = minum8.get_rect()
    textpos.centerx = int(posi_circulo4X+radius*1.0)
    textpos.centery = int(posi_circulo4Y+radius*1.2)
    ventana.blit( minum8, textpos )
     # numero bola 5
    textpos = minum9.get_rect()
    textpos.centerx = int(posi_circulo5X+radius*1.0)
    textpos.centery = int(posi_circulo5Y+radius*0.7)
    ventana.blit( minum9, textpos )
    textpos = minum10.get_rect()
    textpos.centerx = int(posi_circulo5X+radius*1.0)
    textpos.centery = int(posi_circulo5Y+radius*1.2)
    ventana.blit( minum10, textpos )


    # def test_text(screen, text, pos, color):
    # font = pygame.font.Font(None, 12)
    # text = text.replace('\x00','')
    # text = font.render(text, True, color)
    # textpos = text.get_rect()
    # textpos.centerx = pos[0]
    # textpos.centery = pos[1]
    # screen.blit(text, textpos)