import pygame
import math
import noise

# pygame.init()

h = [60,60]
id = 18
upSp = 80
dr = 2 * math.pi / id

def dibujoForma(ventana, values:list[float], pos:tuple[int,int], size:int=150, amp:int = 56, stroke:int=1, upSp=80):
    global h
    if len(values) < 2:
        for i in range(0, 2-len(values)):
            values.append(0.0)

    d = 0
    id = 14 #len(values)
    dr = 2 * math.pi / id
    font = pygame.font.SysFont("Arial", 16)
    color = 255
    posx = pos[0] + size + 30
    posy = pos[1] + size + 30

    for k in range(0,len(values)):
        for j in range(0, stroke):
            points = []
            for i in range(0, id+2): #range(0, id+5):
                ind = i%id
                # angle
                a = dr * ind
                # diameter (size[0]=outer, size[1]=inner)
                # d = (size[0] + noise.pnoise1(h/upSp + ind, octaves=4) * size[1]  +  math.cos(ind) * 7) + j # original
                d = (size + noise.pnoise1(h[k]/upSp + ind, octaves=4) * amp*values[k]  +  math.cos(ind) * 7) + j
                # d = (size[0] + noise.pnoise1(h/upSp + ind, octaves=4) * size[1]  +  math.cos(ind) * values[ind]) + j
                # d = (size[0] + (values[ind]/100) * size[1]  +  math.cos(ind) * 7) - j*random.randint(1, 10)
                # position
                x = math.cos(a)*d + pos[0]
                y = math.sin(a)*d + pos[1]
                points.append((x, y))
            # color = int(255/stroke * j)
            pygame.draw.aalines(ventana, (color, color, color), False, points, blend=2) 
            h[k]+=2
        
    
        textRSSI = font.render( f"RSSI_{k}:  {values[k]*-120.0}" ,True,(100,100,100))
        ventana.blit( textRSSI, (posx, posy))
        posy += 24
        color = 128