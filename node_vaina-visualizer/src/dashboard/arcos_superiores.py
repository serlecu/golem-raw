import pygame

def dib_arcos_sup(ventana, values:list, pos:tuple[int,int], size:tuple[int,int], spacer:int=125):
    posx = pos[0]
    posy = pos[1] + size[1]*0.5
    font = pygame.font.SysFont("Arial", 16)
    pointSize = 6

    # linea horizontal
    pygame.draw.aaline(ventana,(100,100,100),(pos[0],posy),(pos[0]+size[0],posy),1)

    # marcadores de magnitud
    textValue1 = font.render(str("0"),True,(100,100,100))
    textValue2 = font.render(str("n"),True,(100,100,100))
    ventana.blit( textValue1, (pos[0]-5, posy - 40))
    ventana.blit( textValue2, (pos[0]+size[0]-5, posy - 40))

    if len(values) > 1:
        values.append(values[0]+values[1]/2)

    # arcos
    for i in range(len(values)):
        value = int(values[i]/255 * (size[0]/2-(spacer*i)))
        #circulos
        pygame.draw.circle(ventana, (100,100,100), (posx+value ,posy), value, 2, False, False, False, True) # hacer cosa con true y false
        pygame.draw.circle(ventana, (100,100,100), (posx+value ,posy), value, 2, False, False, True, False) #
        #linea pequenyas
        pygame.draw.aaline(ventana, (255,255,255), (posx,posy-10), (posx,posy+10), 2)
        #circulos finale arcos
        pygame.draw.ellipse(ventana, (255,255,255), (int(posx+value*2-pointSize*0.5) ,int(posy-pointSize*0.5), pointSize, pointSize )) #
        # valor
        textValue1 = font.render(str(values[i]),True,(100,100,100))
        ventana.blit( textValue1, (posx+value*2-pointSize*0.5, posy-30))
        posx += spacer
    
    


    
    