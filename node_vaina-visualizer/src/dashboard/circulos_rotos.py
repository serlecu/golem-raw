import pygame
from pygame.locals import *
# import math
# import noise
import random

pygame.init()

def dib_circulorotos(ventana):
    colorCircle = (255,255,255)
    colorNumeros = (255,255,255)
    parteCirculo1 = random.choice([True, False])
    parteCirculo2 = random.choice([True, False])
    parteCirculo3 = random.choice([True, False])
    parteCirculo4 = random.choice([True, False])
    apareceCirculo1 = random.randrange(-1,2)
    apareceCirculo2 = random.randrange(-1,2)
    apareceCirculo3 = random.randrange(-1,2)
    apareceCirculo4 = random.randrange(-1,2)

     #numeros
    miFuente = pygame.font.SysFont("Arial", 11)
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
    valorA = str(apareceCirculo1)
    valorB = str(apareceCirculo2)
    valorC = str(apareceCirculo3)
    valorD = str(apareceCirculo4)
    valorA = miFuente.render(valorA,1,(colorNumeros))
    valorB = miFuente.render(valorB,1,(colorNumeros))
    valorC = miFuente.render(valorC,1,(colorNumeros))
    valorD = miFuente.render(valorD,1,(colorNumeros))
    ventana.blit(valorA,(ventana.get_width()/2-265, ventana.get_height()/2+280))
    ventana.blit(valorB,(ventana.get_width()/2-245, ventana.get_height()/2+280))
    ventana.blit(valorC,(ventana.get_width()/2-265, ventana.get_height()/2+305))
    ventana.blit(valorD,(ventana.get_width()/2-245, ventana.get_height()/2+305))

    #linea horizontal
    pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2-250,ventana.get_height()/2+300),(ventana.get_width()/2+150,ventana.get_height()/2+300),1)
    #circulos
    apareceCirculo1 = random.randrange(-1,2)
    parteCirculo1 = random.choice([True, False])
    parteCirculo2 = random.choice([True, False])
    parteCirculo3 = random.choice([True, False])
    parteCirculo4 = random.choice([True, False])

    pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2-250, ventana.get_height()/2+300), 30, apareceCirculo1, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
    pygame.time.delay(15)
    apareceCirculo2 = random.randrange(-1,2)
    parteCirculo1 = random.choice([True, False])
    parteCirculo2 = random.choice([True, False])
    parteCirculo3 = random.choice([True, False])
    parteCirculo4 = random.choice([True, False])

    pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2-125, ventana.get_height()/2+300), 30, apareceCirculo2, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
    pygame.time.delay(15)
    apareceCirculo3 = random.randrange(-1,2)
    parteCirculo1 = random.choice([True, False])
    parteCirculo2 = random.choice([True, False])
    parteCirculo3 = random.choice([True, False])
    parteCirculo4 = random.choice([True, False])

    pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2, ventana.get_height()/2+300), 30, apareceCirculo3, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
    pygame.time.delay(15)
    apareceCirculo4 = random.randrange(-1,2)
    parteCirculo1 = random.choice([True, False])
    parteCirculo2 = random.choice([True, False])
    parteCirculo3 = random.choice([True, False])
    parteCirculo4 = random.choice([True, False])
    pygame.draw.circle(ventana, colorCircle, (ventana.get_width()/2+125, ventana.get_height()/2+300), 30, apareceCirculo4, parteCirculo1, parteCirculo2, parteCirculo3, parteCirculo4)
   
    
