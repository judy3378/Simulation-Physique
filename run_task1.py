
import pygame
from vecteur3D import *
from Particule import *
from random import random
from pylab import legend, show
from math import pi
import sys

# Task 1: Simulate 10 particles in free fall with an attractive force field
# Initialisation Pygame
def main():

    # Simulation title
    title = "Free fall and force field"

    # initializing pygame
    pygame.init()

    # clock object to ensure 
    clock = pygame.time.Clock()

    # set up screen
    # top left corner is (0,0) top right (1000,0) bottom left (0,700)
    # bottom right (1000,700).
    scene_width = 10
    scene_height = 7
    #screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption(title)

    # Create the Universe
    plage = Univers(step=0.01, dimensions=(scene_width*100,scene_height*100), scale=100)

    # Parameters for the particles
    num_particles = 10

    # Creating random particles
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

    # Adding an attractive field force centered at z=-5m
    center_force = ForceField(Vecteur3D(scene_width/2, scene_height/2, -5), amplitude=5)
    plage.addSource(center_force)

    # Adding gravity
    plage.addSource(Gravity(Vecteur3D(0, 0, -9.8)))

    # Initialize Pygame for visualization (optional)
    plage.gameInit()

    print ('--------------------------------')
    print ('Usage:')
    print ('Press (q) to quit simulation. \nand see figure of trajectories.')
    print ('--------------------------------')


    while plage.run:
        # 30 fps
        clock.tick(30)

        plage.gameUpdate()
        

        if plage.gameKeys[K_q]:
            plage.run = False
        if plage.gameKeys[K_ESCAPE]:
            plage.run = False

        
        
    pygame.quit()
    print(plage.temps)
    print ('--------------------------------')
    print(particle.position)
    print ('--------------------------------')
    print(len(plage.temps), len(particle.position))
    X, Y, Z = zip(*[(p.x, p.y, p.z) for p in particle.velocity])

    plt.figure(1)
    plt.plot(plage.temps, Z)
    plt.xlabel('Time (ms)')
    plt.ylabel('Velociy (z)')
    plt.title('Velocity (z) vs. Time')
    plt.show()

    #plage.plot()
    #plage.plot3d()
    #legend()
    #show()
    sys.exit(0)
    
    
    

if __name__ == '__main__':
    main()
