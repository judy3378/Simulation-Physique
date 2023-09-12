
import pygame
from vecteur3D import *
from Particule import *
from random import random
from pylab import legend, show
from math import pi
import sys

# Task 4: Simulate a pendulum
# Initialisation Pygame
def main():

    # Simulation title
    title = "Pendulum"

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

    # Creating particles
    p1 = Particule(pos0=Vecteur3D(4,4,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 1', color = 'green', glissiere=Vecteur3D(1,0,0))
    p2 =  Particule(pos0=Vecteur3D(3,2,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 2', color= 'blue')
    plage.addAgent(p1)
    plage.addAgent(p2)
    
    

    l0 =( p1.getPosition() - p2.getPosition() ).mod()
    ressort = dampingSpring(p1,p2, k = 100, c = 1, l0 = l0)
    plage.addSource(ressort)

    plage.addSource(Viscosity(0.05))
    
    fconst = ForceConst(Vecteur3D(0,0,0), p1)
    plage.addSource(fconst)
    
    #rod = Rod(p1,p2)
    #plage.addSource(rod)

    # Adding gravity
    plage.addSource(Gravity(Vecteur3D(0, 9.8,0)))

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
        
        if plage.gameKeys[K_RIGHT]:
            fconst.value = Vecteur3D(10,0,0)
        else:
            fconst.value = Vecteur3D()
        
        
        if plage.gameKeys[K_q]:
            plage.run = False
        if plage.gameKeys[K_ESCAPE]:
            plage.run = False

    pygame.quit()
        
    plage.plot()
    legend()
    show()
    sys.exit(0)
    
    
    

if __name__ == '__main__':
    main()
