# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:36:31 2023

@author: Juyeon Kim
"""

from vecteur3D import *
from Particule import *
from pylab import legend, show

from random import random 

plage = Univers(step=0.01)

p1 = Particule(pos0=Vecteur3D(20,30,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 1', color = 'green')

p2 =  Particule(pos0=Vecteur3D(30,40,0), vit0 = Vecteur3D(0,0,0), mass = 1, name = 'ball 2', color= 'blue')

force1 =Vecteur3D(5,0)
#force2 = Vecteur3D(10,20)
g = Gravity(Vecteur3D(0,-9.8,0))
visc = Viscosity(0.9)

l0 =( p1.getPosition() * p2.getPosition() ).mod()
ressort = dampingSpring(p1,p2, k =0.1, c = 0.5 , l0 = l0)

plage.addAgent(p1)
plage.addAgent(p2)

#plage.addSource(g)
plage.addSource(visc)
#plage.addSource(ressort)
#plage.addForce(force2)
#plage.addForce(Gravity(Vecteur3D(0,10)))


plage.gameInit()

while plage.run:

    plage.gameUpdate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plage.run = False

plage.plot()
legend()
show()

pygame.quit()
