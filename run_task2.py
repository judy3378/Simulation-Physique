
import pygame
from vecteur3D import *
from Particule import *
from random import random
import numpy as np
from matplotlib import pylab
from pylab import legend, show
from math import pi
import sys

# Task 2: Simulate particle(s) under gravity and visocity forces
# and generate particle when [Space] pressed

def main():
    # sim title
    title  = "Generate particles"

    # Initialisation Pygame
    pygame.init()

    clock = pygame.time.Clock()
 
    scale=10
    scene_width = 100
    scene_height = 70
    #screen = pygame.display.set_mode((scene_width*scale, scene_height*scale))
    pygame.display.set_caption(title)

    # Create the Universe
    plage = Univers(step=0.01, dimensions=(scene_width*10,scene_height*10), scale=scale)

    # Create two particles for testing
    #p1 = Particule(pos0=Vecteur3D(scene_width/2,scene_height/2,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 1', color = 'green')
    #p2 = Particule(pos0=Vecteur3D(25,6,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 2', color= 'blue')
    #plage.addAgent(p1, p2)
    # Creating random particles
    for _ in range(3):
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

    plage.addSource(Viscosity(0.5))
    plage.addSource(Gravity(Vecteur3D(0,9.8,0)))

    # Initialize Pygame for visualization (optional)
    plage.gameInit()

    print ('--------------------------------')
    print ('Usage:')
    print('Press (space) to generate one particle.')
    print ('Press (q) to quit simulation. \nand see figure of trajectories.')
    print ('--------------------------------')


    gamestage=0

    while plage.run:
        clock.tick(60)
        pygame.display.flip()
        plage.gameUpdate()
        count = 2
        
        if plage.gameKeys[K_SPACE]:
            count+=1
            name = 'Particle'+str(count)
            x = random() * scene_width
            y = random() * scene_height
            z = random()*pi*2
            position = Vecteur3D(x, y, z)
            particle = Particule(name=name, pos0=position, mass=1)
            plage.addAgent(particle)
            
            # if gamestage == 0:
            #     gamestage +=1
            #     particle = Particule(pos0=Vecteur3D(random()*scene_width, random()*scene_height, random()*pi*2), mass=1)
            #     plage.addAgent(particle)
            # elif gamestage ==1:
            #     gamestage ==0
        elif plage.gameKeys[K_q]:
            plage.run = False
        elif plage.gameKeys[K_ESCAPE]:
            plage.run = False
        
        
    pygame.quit()

    print(plage.temps)
    print ('--------------------------------')
    print(particle.position)
    print ('--------------------------------')
    print(len(plage.temps), len(particle.velocity))
    X, Y, Z = zip(*[(p.x, p.y, p.z) for p in particle.velocity])

    plt.figure(1)
    plt.plot(plage.temps, Y)
    plt.xlabel('Time (ms)')
    plt.ylabel('Position (y)')
    plt.title('Position (y) vs. Time')
    plt.show()
    plage.plot()
    legend()
    show()
    sys.exit(0)

if __name__ == '__main__':
    main()
