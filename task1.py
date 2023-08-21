
import pygame
from vecteur3D import *
from Particule import *
from random import random
from pylab import legend, show
from math import pi

# Task 1: Simulate 10 particles in free fall with an attractive force field
# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Scene of 10m by 7m")
clock = pygame.time.Clock()

# Création d'un Univers
plage = Univers(step=0.01, scale =100)

# Paramètres pour les particules
num_particles = 10
scene_width = 10
scene_height = 7

# Création de particules aléatoires
for _ in range(num_particles):
    name = 'Particle'+str(_)
    x = random() * scene_width
    y = random() * scene_height
    z = random()*pi*2#0
    
    r = random()
    g = random()
    b = random()
    rgb = (r,g,b,1)
    
    position = Vecteur3D(x, y, z)
    particle = Particule(pos0=position, name=name, mass=1, color=rgb)
    plage.addAgent(particle)

# Ajout d'un champ de force attractif au centre à z=-5m
center_force = ForceField(Vecteur3D(scene_width/2, scene_height/2, -5), amplitude=5)
plage.addSource(center_force)

plage.addSource(Gravity(Vecteur3D(0, 0, -9.8)))

# Initialize Pygame for visualization (optional)
plage.gameInit()

pygame.display.set_caption("Task1")
#clock = pygame.time.Clock()

while plage.run:
    plage.gameUpdate()
    if plage.gameKeys[K_ESCAPE]:
        plage.run = False

    
    
pygame.quit()
plage.plot()
plage.plot3d()
legend()
show()
