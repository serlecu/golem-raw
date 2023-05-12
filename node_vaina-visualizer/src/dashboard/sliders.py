import pygame

# pygame.init()
# clock = pygame.time.Clock()
ventana = pygame.display.set_mode((0,0), pygame.FULLSCREEN )# full screen
# #ventana = pygame.display.set_mode((800,800))
# pygame.mouse.set_visible(False) # oculta el mouse
# pygame.display.set_caption("RAW-VZ")

def dib_sliders(ventana, 
                values:list,
                pos:tuple[int,int]=(0,0),
                size:tuple[int,int]=(100,100),
                pointSize:int=10,
                vSpacing:int=10 ):
    
    if len(values) < 6:
        for i in range(6-len(values)):
            values.append(0.0)
    ilen = len(values)

    # draw horizontal lines
    for i in range(0,ilen):
        pygame.draw.aaline(ventana,(100,100,100),(pos[0],pos[1]+(vSpacing*i)),(pos[0]+size[0],pos[1]+(vSpacing*i)),1)

    # create a transparent surface
    surface1 = ventana.convert_alpha() # Surface(size) #! OJO era: surface1 = ventana.convert_alpha()
    surface1.fill([0,0,0,0])

    # draw circles on transparent surface
    for i in range(0,ilen):
        pygame.draw.circle(surface1,(255,255,255,128),(pos[0]+(values[i]*size[0]),pos[1]+(vSpacing*i)),pointSize)
        pygame.time.delay(10)

    # draw transparent surface on main surface
    ventana.blit(surface1, (0,0))