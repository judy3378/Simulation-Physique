# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:19:13 2023

@author: Juyeon Kim
"""

from vecteur3D import Vecteur3D
import pygame
from pygame.locals import *
from time import time
import datetime
from matplotlib import pylab
from pylab import *
from pylab import plot
import math
from random import random
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

class Particule(object):
    
    def __init__(self, pos0 = Vecteur3D(), vit0=Vecteur3D(), mass = 0, name = 'p1', color = 'blue', fix=False):
        """attribute 'fix' can be used to not adhere to the PFD"""
        self.position = [pos0]
        self.velocity=[vit0]
        self.acc = [Vecteur3D()]
        self.forces = [Vecteur3D()]
        self.mass = mass
        self.name = name
        self.color = color
        self.fix = fix

    def getPosition(self):
        """returns current position"""
        return self.position[-1]
    
    def getSpeed(self):
        """returns current speed"""
        return self.velocity[-1]

    def move (self,step):
        """for a time 'step', resolves the PFD with external forces sum, then calculates acceleration, velocity and position"""
        V = Vecteur3D()
        V = self.getSpeed()
        #acceleration = [force/self.mass for force in self.forces] # external forces sum
        #for i in range(3):
        #    self.velocity[i] += acceleration[i]*step
        #    self.position[i] +=self.velocity[i]*step
        self.velocity += [V+self.acc[-1]* step]
        self.position += [V * step + 0.5*self.acc[-1]*step**2 + self.getPosition()]
        
    def setForce(self, force = Vecteur3D()):
        """adds a force to a list of forces"""
        self.forces.append(force)
        
    def setSpeed(self, speed=Vecteur3D()):
        """disregards PFD and enforces velocity only when 'fix'=True"""
        self.velocity = speed
        
    def setPosition(self, position=Vecteur3D()):
        """disregards PFD and enforces position only when 'fix'=True"""
        self.position = position
        
    def getForces(self):
        """returns the last force applied"""
        return self.forces[-1] 

    def getAcc(self):
        """returns the current acceleration"""
        a = Vecteur3D()
        a = self.getForces() * (1/self.mass)
        self.acc.append(a)
        
        
    # def plot(self):
    #     """plots trajectory"""
    #     X=[]
    #     Y=[]
    #     Z=[]
    #     for p in self.position:
    #         X.append(p.x)
    #         Y.append(p.y)
    #         Z.append(p.z)
    #     return plot(X,Z,color=self.color,label=self.name) #X,Y,

    def plot(self):
        """plots 2D trajectory"""
        X, Y, Z = zip(*[(p.x, p.y, p.z) for p in self.position])
        return plot(X, Y, color=self.color, label=self.name)

    
    
    def plot3d(self):
        """"3d plot"""
        fig = plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        
        X, Y, Z = zip(*[(p.x, p.y, p.z) for p in self.position])
        ax.scatter3D(X,Y,Z,color=self.color, label=self.name)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Trajectory')

        plt.legend()
        plt.show()
    


    def gameDraw(self, screen, scale):
        size = 5
        pos = self.getPosition()
        X, Y, Z = int(scale * pos.x), int(scale * pos.y), int(scale * pos.z)
        
        r, g, b = random(), random(), random()
        rgb = (r, g, b, 1)

        pygame.draw.circle(screen, rgb, (X, Y), size * 2, size)

        vit = self.getSpeed()
        VX, VY = int(scale * vit.x) + X, int(scale * vit.y) + Y

        pygame.draw.line(screen, self.color, (X, Y), (VX, VY))

     
    def __str__(self):
        return f"Particle {self.name}: Position = {self.position}, Velocity = {self.velocity}"

    def __repr__(self):
        return self.__str__()
      
      
class Univers(object) :
    
    def __init__(self, name="la plage", t0=0, step=0.1, dimensions=(1024,768), scale=1, *args):
        self.name = name
        self.temps = [t0]
        self.population = []
        self.step = step
        self.dimensions = dimensions
        self.listForce = []
        self.scale=scale
        
    def addAgent(self, *agents):
        """add one or multiple agents"""
        self.population.extend(agents)
    
    def addSource(self, *generators):
        """add one or multiple sources/forces"""
        self.listForce.extend(generators)
        
    # def sumForce(self, listForce):
    #     totalForce = Vecteur3D()
    #     for f in self.listForce:
    #         totalForce += f
    
    def simule(self):
        """perform a simulation for one step for the entire population"""
        for part in self.population:
            totalForce = Vecteur3D()
            for f in self.listForce:
                totalForce += f.apply(part)
            if part.fix==False:    
                part.setForce(totalForce)
                part.getAcc()
                part.move(self.step)
            else:
                
                part.move(self.step)
            
        self.temps.append(self.temps[-1]+self.step)
    
    
    def simul(self):
        for particle in self.population:
            particle.move(self.step)
        
        self.temps.append(self.temps[-1]+self.step)

    def simuleAll(self, time):
        """perform a smiluation for a duration of 'time'=> multiple simule() steps"""
        #num_steps = int(time/self.step)
        #for _ in range(num_steps):
        #    self.simul()
        #    self.time += self.step
        while self.temps[-1] <time:
            self.simule()

    def plot(self):
        for a in self.population:
            a.plot()
            
    def plot3d(self):
        for a in self.population:
            a.plot3d()
        
    def gameInit(self):
        """ start a real-time simulation with display in a Pygame window.
            set the display fram erate to 60fps."""
    
        pygame.init()
        self.t0 = time.time()
        self.screen = pygame.display.set_mode(self.dimensions)
        self.clock = pygame.time.Clock()
        self.background=(200,200,200)
        self.fps=60
        self.run=True     
        #pygame.display.set_caption(self.name)
        self.gameKeys = pygame.key.get_pressed()
        
    def gameUpdate(self):
        """handles keyboard/mouse input and simulates display for a step"""
        
        now = time.time()-self.t0
        while self.temps[-1] < now:
            self.simule()

        self.screen.fill(self.background)
        
        # display current time
        font_obj = pygame.font.Font('freesansbold.ttf', 24)
        text_surface_obj = font_obj.render(f'{now:.2f}', True, 'red', self.background)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (25, 10)
        self.screen.blit(text_surface_obj, (50,20))

        # display particles        
        for p in self.population:
            p.gameDraw(self.screen,self.scale)
        
        
        pygame.display.update()
        self.clock.tick(self.fps)
        
        # check for window close event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        
        pygame.display.flip
        
        self.gameKeys = pygame.key.get_pressed()
        #update particle forces based on keyboard input or mouse
        

class ForceConst(object):
    def __init__(self, value = Vecteur3D(), *particles):
        self.value = value
        self.particles = particles
           
    def apply(self, p):
        return self.value
    
class ForceHarmonic(object):
    def __init__(self, value=Vecteur3D(), pulsation =0, *particles):
        self.value = value
        self.pulsation = pulsation
        self.particles = particles
    
    def apply(self, p):
        return self.value * math.cos(self.pulsation*time.time())

class Viscosity(object):
    def __init__(self, coef = 0, *particles):
        self.coef = coef
        self.particles = particles
    
    def apply(self, p):
        return self.coef * (-p.getSpeed())
    
class ForceField(object):
    def __init__(self, pos0=Vecteur3D(), amplitude = Vecteur3D(), *particles):
        self.pos0 = pos0
        self.amplitude = amplitude
        self.particles = particles
    
    def apply(self, p):
        displacement = self.pos0 - p.getPosition()
        return self.amplitude*displacement

class SpringDumper(object):
    def __init__(self, stiffness = 0, dumping=0, length=0, particle1=None, particle2=None):
        self.stiffness=stiffness
        self.dumping=dumping
        self.length=length
        self.particle1=particle1
        self.particle2=particle2
        
    def apply(self,p):
        if p is self.particle1:
            dist = self.particle2.getPosition() - self.particle1.getPosition()
            relative_speed = self.particle2.getSpeed() - p.getSpeed()
        elif p is self.particle2:
            dist = self.particle1.getPosition() - self.particle2.getPosition()
            relative_speed = self.particle1.getSpeed() - p.getSpeed()
        else:
            return Vecteur3D()
        
        spring_force =  (dist.mod() - self.length) * self.stiffness
        damping_force = self.dumping *relative_speed

        
        return (spring_force + damping_force) *dist.norm()

    
class Rod(object):
    def __init__(self, particle1=None, particle2=None):
        self.particle1 = particle1
        self.particle2 = particle2
        self.stiffness = 0
        self.dumping = 0
    
    def apply(self,p):
        return dampingSpring(self.stiffness, self.dumping, 0, self.particle1, self.particle2).apply(p)
    

class PrismJoint(object):
    def __init__(self, axis=Vecteur3D(), particle=None):
        self.axis = axis # direction of the joint
        self.particle = particle
    
    def apply(self, p):
        displacement = p.getPosition() - self.particle.getPosition()
        projected_displacement = displacement - displacement.proj(self.axis)
        return projected_displacement * -self.particle.mass*9.81 #assuming gravity
                
class Gravity(object):
    def __init__(self, dir = Vecteur3D()):
        self.dir = dir
        
    def apply(self, p):
        return self.dir * p.mass




class dampingSpring(object):
    def __init__(self,  p0, p1, k=0, c=0, l0=0):
        self.k = k #raideur
        self.c = c #ammortissement
        self.l0 = l0 #distance initiale
        self.p0 = p0
        self.p1 = p1
        
    def apply(self, p):
        if p is self.p0:
            dist = self.p1.getPosition() - self.p0.getPosition() #position de la masse
            vit = (self.p1.getSpeed() - p.getSpeed()) ** dist #
        
        elif p is self.p1:
            dist = self.p0.getPosition() - self.p1.getPosition() #position de la masse
            vit = (self.p0.getSpeed() - p.getSpeed()) ** dist
            
        else:
            return Vecteur3D()
        
        Fr = (dist.mod() - self.l0) * self.k #force de rappel
        Fv = self.c * vit #force de viscosite
        Fnormalise = (Fr+Fv)*dist.norm()
    
        force =((dist.mod() - self.l0) * self.k + self.c * vit ) * dist.norm() #renvoie un vecteur normalisé
        
        return force
        
        
