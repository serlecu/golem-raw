import pygame
from pygame.locals import *
# import math
# import noise


diametro = 110
colorDiagrama = (100,100,100)
grosorDiagrama = 1
posi_circulo1X = 650
posi_circulo1Y = 600
posi_circulo2X = 450
posi_circulo2Y = 600
posi_circulo3X = 250
posi_circulo3Y = 600
posi_circulo4X = 525
posi_circulo4Y = 350
posi_circulo5X = 325
posi_circulo5Y = 350

pygame.init()

def dib_diagrama(ventana, values:list):
    #global posi_circulo1X, posi_circulo1Y, posi_circulo2X, posi_circulo2Y, posi_circulo3X, posi_circulo3Y, posi_circulo4X, posi_circulo4Y, diametro, colorDiagrama, grosorDiagrama
    #funcion que dibuja circulos
    pygame.draw.ellipse(ventana, (colorDiagrama), (ventana.get_width()-posi_circulo1X, ventana.get_height()-posi_circulo2Y, diametro,diametro), grosorDiagrama)
    pygame.draw.ellipse(ventana, (colorDiagrama), (ventana.get_width()-posi_circulo2X, ventana.get_height()-posi_circulo2Y, diametro,diametro), grosorDiagrama)
    pygame.draw.ellipse(ventana, (colorDiagrama), (ventana.get_width()-posi_circulo3X, ventana.get_height()-posi_circulo3Y, diametro,diametro), grosorDiagrama)
    pygame.draw.ellipse(ventana, (colorDiagrama), (ventana.get_width()-posi_circulo4X, ventana.get_height()-posi_circulo4Y, diametro,diametro), grosorDiagrama)
    pygame.draw.ellipse(ventana, (colorDiagrama), (ventana.get_width()-posi_circulo5X, ventana.get_height()-posi_circulo5Y, diametro,diametro), grosorDiagrama)
    #lineas horizontales
    pygame.draw.aaline(ventana,(colorDiagrama),(ventana.get_width()-540,ventana.get_height()-550),(ventana.get_width()-450,ventana.get_height()-550),1)
    pygame.draw.aaline(ventana,(colorDiagrama),(ventana.get_width()-340,ventana.get_height()-550),(ventana.get_width()-250,ventana.get_height()-550),1)
    pygame.draw.aaline(ventana,(colorDiagrama),(ventana.get_width()-415,ventana.get_height()-300),(ventana.get_width()-325,ventana.get_height()-300),1)
    # lineas oblicuas
    pygame.draw.aaline(ventana,(colorDiagrama),(ventana.get_width()-565,ventana.get_height()-500),(ventana.get_width()-475,ventana.get_height()-350),1)
    pygame.draw.aaline(ventana,(colorDiagrama),(ventana.get_width()-225,ventana.get_height()-500),(ventana.get_width()-275,ventana.get_height()-350),1)
    #linea vertical
    pygame.draw.aaline(ventana,(colorDiagrama),(ventana.get_width()-390,ventana.get_height()-490),(ventana.get_width()-380,ventana.get_height()-300),1)
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
    ventana.blit(minum1,(ventana.get_width()-610,ventana.get_height()-575))
    ventana.blit(minum2,(ventana.get_width()-610,ventana.get_height()-545))
    # numero bola 2
    ventana.blit(minum3,(ventana.get_width()-410,ventana.get_height()-575))
    ventana.blit(minum4,(ventana.get_width()-410,ventana.get_height()-545))
      # numero bola 3
    ventana.blit(minum5,(ventana.get_width()-210,ventana.get_height()-575))
    ventana.blit(minum6,(ventana.get_width()-210,ventana.get_height()-545))
    # numero bola 4
    ventana.blit(minum7,(ventana.get_width()-480,ventana.get_height()-315))
    ventana.blit(minum8,(ventana.get_width()-480,ventana.get_height()-290))
     # numero bola 5
    ventana.blit(minum9,(ventana.get_width()-290,ventana.get_height()-315))
    ventana.blit(minum10,(ventana.get_width()-290,ventana.get_height()-290))