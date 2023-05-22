import pygame

# pygame.init()


def dib_barras(ventana, 
               values:list[int], # [0-100] will turn into [0-1]
               pos:tuple[int,int], 
               maxWidth:int,
               stroke:int=60,
               spacing:int=10 ):
   
   if len(values) < 6:
      for i in range(6-len(values)):
            values.append(0)
   ilen = len(values)
   xpos = pos[0]
   ypos = pos[1]
   
   for i in range(0,ilen):
      pygame.draw.aaline(ventana,(100,100,100),(pos[0],ypos + stroke + spacing),(pos[0],ypos + 2*stroke + spacing),1)
      # draw bars
      rect = pygame.Rect(pos[0], ypos + stroke + spacing, values[i]/255 * maxWidth, stroke)
      pygame.draw.rect(ventana, (255,255,255), rect, 0)

      # draw numbers
      font = pygame.font.SysFont("Arial", 24)
      textValue = font.render( str(values[i]),True,(100,100,100) )
      ventana.blit( textValue, (xpos, pos[1]) ) #ilen * (stroke+spacing)) )

      xpos += (maxWidth / (ilen+1))
      ypos += stroke + spacing
    