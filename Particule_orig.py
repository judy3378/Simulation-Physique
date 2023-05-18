# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:19:13 2023

@author: Juyeon Kim
"""

from vecteur3D import Vecteur3D
import pygame
from pygame.locals import *
from time import time
import sys, termios, tty


class Particule(object):
    """Classe Particule """
    
    def __init__(self, mass = 0, pos0 = Vecteur3D(), vit0 = Vecteur3D(), name = 'p1', color = 'blue', fixe = False):
        """Constructeur avec des valeurs par defaut : 
            les attributs position et vitesse gardent l'historique
            l'attribut forces pour
            l'attribut fix = True? pour ne pas respecter la PFD"""
        self.position = [pos0]
        self.velocity=[vit0]
        self.acc = [Vecteur3D()]
        self.forces =[ Vecteur3D()]
        self.mass = mass
        self.name = name
        self.color = color
        self.fixe = fixe
        
    def getPosition(self):
        """ retourne la position actuelle """
        return self.position[-1]
    
    def getSpeed(self):
        """ retourne la vitesse actuelle """
        return self.velocity[-1]
    
    def setForce(self, Force = Vecteur3D()):
        self.forces.append(Force)
        
    def getForces(self):
        return self.forces[-1]
    

    
    def getAcc(self):
        a = Vecteur3D()
        a = self.getForces() * (1/self.mass)
        self.acc.append(a)
        
    def setSpeed(self, speed = Vecteur3D()):
        self.velocity.append(speed)
        
    def setPosition(self, p=Vecteur3D()):
        self.position.append(p)
        
        
    def move (self, step):
        """ pour un pas de temps step, resolution de PFD avec somme des forces,
        calcule l'acceleration, la vitesse, la position"""
        if self.fixe == False:
            V = self.getSpeed()
            self.velocity += [V+self.acc[-1]* step]
            self.position += [V * step + 0.5*self.acc[-1]*step**2 + self.getPosition()]
        else:
            V=self.getSpeed()
            self.velocity += [V]
            self.position += [self.getPosition()]
        

    def plot(self):
        from pylab import plot
        X=[]
        Y=[]
        for p in self.position:
            X.append(p.x)
            Y.append(p.y)
    
        return plot(X,Y,color=self.color,label=self.name)
    

    def gameDraw(self,screen,scale):
        
        height = screen.get_height()
        #width, height = screen.get_size()
        
        size= 5
        pos = self.getPosition()
        X = int(scale*pos.x)
        Y = height - int(scale*pos.y)
        
        pygame.draw.circle(screen,self.color,(X,Y),size*2,size)
        
        # check if particle has hit left or right wall
        # if X <= 0:
        #     X = 0
        #     self.velocity[-1].x *= -1
        # elif X >= width:
        #     X = width
        #     self.velocity[-1].x *= -1
            
        # if Y <= 0:
        #     Y = 0
        #     self.velocity[-1].y *= -1
        # elif Y >= height:
        #     Y = height
        #     self.velocity[-1].y *= -1
        
        
        
        
        vit = self.getSpeed()
        VX = int(scale*vit.x) + X
        VY = -int(scale*vit.y) + Y
    
        
        pygame.draw.line(screen,self.color,(X,Y),(VX,VY))
     



      
        
class Univers(object) :
    
    def __init__(self,name="la plage",t0=0, step=0.1,*args):
        self.name = name
        self.temps=[t0]
        self.population=[]
        self.step=step
        self.listForce = []
        
    def addAgent(self,agent):
        self.population.append(agent)
    
    def addForce(self, f):
        self.listForce.append(f)
        
    # def sumForce(self, listForce):
    #     totalForce = Vecteur3D()
    #     for f in self.listForce:
    #         totalForce += f
    
    def get_ch(self):
         fd = sys.stdin.fileno()
         old_settings = termios.tcgetattr(fd)
         try:
             tty.setraw(sys.stdin.fileno())
             ch = sys.stdin.read(3)
         finally:
             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
         return ch
     

    def simule(self):
        for part in self.population:
            totalForce = Vecteur3D()
            for f in self.listForce:
                totalForce += f.apply(part)
            
            # char=self.get_ch()

            # if char=="s":
                        
            # #if keyboard.is_pressed("s"):
            #     part.fixe=True
            #     print("s pressed")

            if part.fixe == False:
                
                part.setForce(totalForce)
                part.getAcc()
                part.move(self.step)
            
            else :
                part.setSpeed(Vecteur3D(2,0,0))

                part.move(self.step)


                
            
            
            #if part.right >= 1024 or part.right <=0:
            #    part.getSpeed
            
        self.temps.append(self.temps[-1]+self.step)
    
    
    def plot(self):
        for a in self.population:
            a.plot()
            
        
    def gameInit(self,W,H,fps=60,background=(0,0,0),scale=1000):
        """ creer le fenetre """
        
        pygame.init()
        self.t0= time()
        
        self.W = W
        self.H = H
        
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.background=background
        self.fps=fps
        self.scale=scale
        self.run=True
                
        pygame.display.set_caption(self.name)
        self.gameKeys = pygame.key.get_pressed()
        
    def gameUpdate(self):
        
        
        now = time()-self.t0
        
        while self.temps[-1] < now:
            self.simule()


        self.screen.fill(self.background)
        
        # Affiche le temps à la fenêtre
        font_obj = pygame.font.Font('freesansbold.ttf', 24)
        text_surface_obj = font_obj.render(str(now)[:6], True, 'red', self.background)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (25, 10)
        self.screen.blit(text_surface_obj, (50,20))

        # Affiche chaque particule de la population        
        for p in self.population:
            p.gameDraw(self.screen,self.scale)
            
        # Envoie à l'écran
        pygame.display.update()
        
        # On est bon jusqu'à la prochaine 
        self.clock.tick(self.fps)
        
        # Est-ce que qq1 a fermé la fenêtre ?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        
        # Quelles touches ont été appuyées depuis le dernier affichage
        self.gameKeys = pygame.key.get_pressed()
        
        
class Gravity():
    def __init__(self, dir = Vecteur3D()):
        self.dir = dir
        
    def apply(self, p):
        return self.dir * p.mass

class Viscosity():
    def __init__(self, coef = 0):
        self.coef = coef
    
    def apply(self, p):
        return self.coef * (-p.getSpeed())
    
class forceCst():
    def __init__(self, norme = Vecteur3D()):
        self.force = norme
           
    def apply(self, p):
        return self.force

class dampingSpring():
    def __init__(self,  p0, p1, k=0, c=0, l0=0):
        self.k = k #raideur
        self.c = c #ammortissement
        self.l0 = l0 #distance initiale
        self.p0 = p0
        self.p1 = p1
        
    def apply(self, p):
        if p is self.p0:
            dist = self.p1.getPosition() - p.getPosition() #position de la masse
            vit = (self.p1.getSpeed() - p.getSpeed()) ** dist #
        
        elif p is self.p1:
            dist = self.p0.getPosition() - p.getPosition() #position de la masse
            vit = (self.p0.getSpeed() - p.getSpeed()) ** dist
            
        else:
            return Vecteur3D()
        
        Fr = (dist.mod() - self.l0) * self.k #force de rappel
        Fv = self.c * vit #force de viscosite
        Fnormalise = (Fr+Fv)*dist.norm()
    
        force =((dist.mod() - self.l0) * self.k + self.c * vit ) * dist.norm() #renvoie un vecteur normalisé
        
        return force
        
        