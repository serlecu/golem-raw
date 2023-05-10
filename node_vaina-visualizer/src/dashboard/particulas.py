import pygame, sys, random
 
# a particle is...
# a thing that exists at a location
# typically moves around
# typically changes over time
# and typically disappears after a certain amount of time
# [loc, velocity, timer]
particles = []
 
# Loop ------------------------------------------------------- #
def dib_particulas(ventana):
    colorAxis = (255,255,255)
    mx = random.randint(ventana.get_width()/2+400, ventana.get_width()-200)
    my = random.randint(350, ventana.get_height()/2-100)
    particles.append([[mx, my], [random.randint(0, 10) / 10 - 1, -2], random.randint(2, 5)])
    #horizontal
    pygame.draw.aaline(ventana,(100,100,100),(ventana.get_width()/2+250,ventana.get_height()/2-150),(ventana.get_width()-200,ventana.get_height()/2-150),1)
    #vertical
    pygame.draw.aaline(ventana,(colorAxis),(ventana.get_width()/2+250,ventana.get_height()/2-165),(ventana.get_width()/2+250,ventana.get_height()/2-135),1)
    #pygame.draw.aaline(ventana,(colorAxis),(ventana.get_width()/2+475,ventana.get_height()/2-210),(ventana.get_width()/2+475,ventana.get_height()/2-190),1)
    pygame.draw.aaline(ventana,(colorAxis),(ventana.get_width()/2+465,ventana.get_height()/2-210),(ventana.get_width()/2+485,ventana.get_height()/2-210),1)
    pygame.draw.aaline(ventana,(colorAxis),(ventana.get_width()/2+465,ventana.get_height()/2-100),(ventana.get_width()/2+485,ventana.get_height()/2-100),1)
    pygame.draw.aaline(ventana,(colorAxis),(ventana.get_width()-200,ventana.get_height()/2-165),(ventana.get_width()-200,ventana.get_height()/2-135),1)
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][0] += particle[1][1]
        """particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]"""
        particle[2] -= 0.03
        particle[1][1] += 0.03
        pygame.draw.circle(ventana, (128, 128, 128), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)
  
    


