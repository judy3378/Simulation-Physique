
import pygame
from vecteur3D import *
from Particule import *
from random import random
import numpy as np
from pylab import legend, show
from math import pi

# Task 2: Simulate 
scale=10
scene_width = 100
scene_height = 7
# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((scene_width*scale, scene_height*scale))
pygame.display.set_caption("Task2 : Scene of 100m by 70m")
clock = pygame.time.Clock()

# Création d'un Univers
plage = Univers(step=0.01, scale =scale)


# Create two particles for testing
p1 = Particule(pos0=Vecteur3D(scene_width/2,scene_height/2,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 1', color = 'green')

p2 =  Particule(pos0=Vecteur3D(25,6,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 2', color= 'blue')

plage.addAgent(p1, p2)

#plage.addSource(Viscosity(0.5))
plage.addSource(Gravity(Vecteur3D(0,-9.8,0)))

# Initialize Pygame for visualization (optional)
plage.gameInit()


#clock = pygame.time.Clock()
gamestage=0

while plage.run:
    plage.gameUpdate()
    if plage.gameKeys[K_SPACE]:
        print('space pressed')
        if gamestage == 0:
            print('start simulation')
            gamestage +=1
        elif gamestage ==1:
            gamestage ==0
            print('gamestage=0')
    elif plage.gameKeys[K_ESCAPE]:
        plage.run = False
    
   
    
pygame.quit()
plage.plot()
legend()
show()
