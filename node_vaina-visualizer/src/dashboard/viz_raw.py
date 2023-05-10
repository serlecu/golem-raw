import pygame, sys
from pygame.locals import *
from pygame import Surface
import random
# import math
# import noise
# import forma_movi
# import forma_movi as fm
from .forma_movi import dibujoForma
# import diagrama_datos as dd
from .diagrama_datos import dib_diagrama
# import barras as bb
from .barras import dib_barras
# import numeros as nm
from .numeros import dib_numero
# import imagen_estruc as ie
from .imagen_estruc import dib_imag_estructura
# import particulas as pt
from .particulas import dib_particulas
# import linechart as lc
from .linechart import dib_lineapuntos
# import circulos_rotos as cr
from .circulos_rotos import dib_circulorotos

# TODO: 
# - importar noise si de verdad hace falta
# - importar forma_movi si de verdad hace falta
# - arreglar coordenadas


pygame.init()
clock = pygame.time.Clock()
ventana = pygame.display.set_mode((0,0), pygame.FULLSCREEN )# full screen
#ventana = pygame.display.set_mode((800,800))
pygame.mouse.set_visible(False) # oculta el mouse
pygame.display.set_caption("RAW-VZ")

colorFondo = (0,0,0)

def eventTeclado():
    # evento que cierra la ventana cuando presionas ESC
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit() 
# fin del evento


def lineasCirculo(v, values:list, pos:tuple[int,int]=(0,0), size:tuple[int,int]=(100,100), pointSize:int=10 ):
    # if v == None:
    #     v = ventana
    ilen = len(values)
    vertSpacing = size[1] / ilen

    # draw horizontal lines
    for i in range(0,ilen):
        pygame.draw.aaline(v,(255,255,255),(pos[0],pos[1]+(vertSpacing*i)),(pos[0]+size[0],pos[1]+(vertSpacing*i)),1)

    # create a transparent surface
    surface1 = v.convert_alpha() # Surface(size) #! OJO era: surface1 = v.convert_alpha()
    surface1.fill([0,0,0,0])

    # draw circles on transparent surface
    for i in range(0,ilen):
        pygame.draw.circle(surface1,(255,255,255,128),(values[i],pos[1]+(vertSpacing*i)),pointSize)
        pygame.time.delay(10)

    # draw transparent surface on main surface
    v.blit(surface1, (0,0))



    # # === ORIGINAL === #
    # pygame.draw.aaline(v,(255,255,255),(100,500),(500,500),1)
    # pygame.draw.aaline(v,(255,255,255),(100,550),(500,550),1)
    # pygame.draw.aaline(v,(255,255,255),(100,600),(500,600),1)
    # pygame.draw.aaline(v,(255,255,255),(100,650),(500,650),1)
    # pygame.draw.aaline(v,(255,255,255),(100,700),(500,700),1)
    # #circulos en alpha

    # surface1 = v.convert_alpha()
    # surface1.fill([0,0,0,0])
    # valorSensor= random.randint(100,500)
    # pygame.draw.circle(surface1,(255,255,255,128),(valorSensor,500),6)
    # pygame.time.delay(10)
    # valorSensor= random.randint(100,500)
    # pygame.draw.circle(surface1,(255,255,255,128),(valorSensor,550),6)
    # pygame.time.delay(10)
    # valorSensor= random.randint(100,500)
    # pygame.draw.circle(surface1,(255,255,255,128),(valorSensor,600),6)
    # pygame.time.delay(10)
    # valorSensor= random.randint(100,500)
    # pygame.draw.circle(surface1,(255,255,255,128),(valorSensor,650),6)
    # pygame.time.delay(10)
    # valorSensor= random.randint(100,500)
    # pygame.draw.circle(surface1,(255,255,255,128),(valorSensor,700),6)
    # pygame.time.delay(10)    
    # v.blit(surface1, (0,0))

    
# # bucle principal
# while True:
#     ventana.fill(colorFondo)
#     eventTeclado()
#     lineasCirculo()
#     # dibujoForma(ventana,fm.id, fm.upSp, fm.dr) # en forma_movi
#     dib_diagrama(ventana)
#     dib_barras(ventana)
#     dib_numero(ventana)
#     dib_imag_estructura(ventana)
#     dib_particulas(ventana)
#     dib_lineapuntos(ventana)
#     dib_circulorotos(ventana)
   
   
  
#     pygame.display.flip()
#     clock.tick(15)
    
    
#     #pygame.time.delay(10)
#     pygame.display.update()
    
    
 
    