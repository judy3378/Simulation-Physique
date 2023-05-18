# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:36:31 2023

@author: Juyeon Kim
"""

from vecteur3D import *
from Particule import *
from pylab import legend, show
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

from random import random 

plage = Univers(step=0.01)


p1 = Particule(P0=Vecteur3D(50,80,0) , mass = 1, name = 'ball 1', color = 'green',fixe = True)

p2 =  Particule(P0=Vecteur3D(70,70,0), mass = 1, name = 'ball 2', color= 'blue', fixe = False)

p3 = Particule(P0= Vecteur3D(60,40,0), mass = 1, name = 'ball 3', color = 'red', fixe = False)

force1 =forceCst(Vecteur3D(1,0))
g = Gravity(Vecteur3D(0,-9.8,0))
visc = Viscosity(0.9)

l0 =( p1.getPosition() - p2.getPosition()).mod()

ressort = dampingSpring(p1,p2, k =1, c =0, l0 = l0)

plage.addAgent(p1)
plage.addAgent(p2)

#plage.addAgent(p3)

#plage.addForce(force1)
plage.addForce(g)
#plage.addForce(visc)
plage.addForce(ressort)


plage.gameInit(1024,768,background='gray',scale=5)

while plage.run:
    plage.gameUpdate()
    for event in pygame.event.get(): # User does something
        if event.type == pygame.QUIT:# if user cliked close
            plage.run = False # flag to exit looop

#plage.plot()

#fig = plt.figure()
#ax = plt.axes(projection='3d')
#legend()


pygame.quit()
