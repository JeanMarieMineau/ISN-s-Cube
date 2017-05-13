#!/usr/bin/env python3
# coding: utf-8

'''
Created on 16 mars 2017

Copyright 2017 Jean-Marie Mineau, Maxime Keller
This file is part of "ISN's Cube".

    "ISN's Cube" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "ISN's Cube" is distributed in the hope that it will be useful and 
    recreative, but WITHOUT ANY WARRANTY; without even the implied 
    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "ISN's Cube".  If not, see <http://www.gnu.org/licenses/>.

@author: <mineau.jean.marie@gmail.com>, Maxime Keller 
'''
import pygame
from operator import itemgetter
from random import choice
from Cube1x1 import Cubie3D
from Action import Action
from CubeGetteur import CubeGetteur
from Commande import Commande
from Solveur import Solver

ROUGE, ORANGE, JAUNE, BLANC, VERT, BLEU = (255,0,0), (255,130,20), (255,255,20), (255,255,255), (0,255,0), (0,0,255)

class Cube(Commande, CubeGetteur, Solver):
    """Objet représentant le rubick's Cube."""
    
    def __init__(self, screen, vide = False):
        """Init. ''vide'' permet d'éviter une réinitialisation de tous le cube."""
        
        Commande.__init__(self, parent = self)
        if not vide:
            #Place les cubies
            lpos = []
            for x in [-4, 0, 4]:
                for y in [-4, 0, 4]:
                    for z in [-4, 0, 4]:
                        lpos.append((x, y, z))
            self.cubies = [Cubie3D(pos) for pos in lpos if pos != (0,0,0)]
            
            self.orientation = [-30,30,0]
            self.screen = screen
            self.setColor()
        
    def creationRefletNonOriente(self):
        """Crée un reflet du cube non orienté."""
        newCube = Cube(None, vide = True)
        newCube.orientation = [0,0,0]
        newCubies = [cubie.copie() for cubie in self.cubies]
        newCube.cubies = newCubies
        newCube.screen = self.screen
        return newCube
        
    def creationReflet(self):
        """Crée un reflet du cube orienté selon l'orientation du cube."""
        newCube = Cube(None, vide = True)
        newCube.orientation = self.orientation
        newCubies = [cubie.rotationX(self.orientation[0]) for cubie in self.cubies]
        newCubies = [cubie.rotationY(self.orientation[1]) for cubie in newCubies]
        newCubies = [cubie.rotationZ(self.orientation[2]) for cubie in newCubies]
        newCube.cubies = newCubies
        newCube.screen = self.screen
        return newCube
        
    def affichage(self):
        """Affiche le cube"""
        
        cubiesZ = [[cubie, cubie.minZ] for cubie in self.cubies]
        
        #self.nbImg = 0
        liste = sorted(cubiesZ, key=itemgetter(1), reverse=True)
        
        for tmp in liste:
            cubie = tmp[0]
            cubie.affichage(self.screen)
            #pygame.display.flip()
            #pygame.display.flip()
            #pygame.image.save(screen,"./img/" + str(self.nbImg) + "Tri2.png")
            #self.nbImg += 1
            #pygame.time.wait(100)            
         
    def setColor(self):
        """Attribut les couleurs aux faces."""
        liste = self.getH()
        for i in liste:
            self.cubies[i].couleurs[0] = ROUGE
            self.cubies[i].couleursResolution.append(ROUGE)
        liste = self.getB()
        for i in liste:
            self.cubies[i].couleurs[1] = ORANGE
            self.cubies[i].couleursResolution.append(ORANGE)
        liste = self.getG()
        for i in liste:
            self.cubies[i].couleurs[2] = JAUNE
            self.cubies[i].couleursResolution.append(JAUNE)
        liste = self.getD()
        for i in liste:
            self.cubies[i].couleurs[3] = BLANC
            self.cubies[i].couleursResolution.append(BLANC)
        liste = self.getAr()
        for i in liste:
            self.cubies[i].couleurs[4] = VERT
            self.cubies[i].couleursResolution.append(VERT)
        liste = self.getAv()
        for i in liste:
            self.cubies[i].couleurs[5] = BLEU
            self.cubies[i].couleursResolution.append(BLEU)
            
    def run(self):
        """Lance l'affichage."""
        self.touches()
        self.action()
        reflet = self.creationReflet()
        reflet.affichage()
        
if __name__ == "__main__":
    
    pygame.init()
          
    angle = 5
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Rubick's Cube")   
    
    cubes = [Cube(screen)]
    
    prendreImage = False
    
    rot = False
    #cubes[0].orientation = [-30,30,0]
    #print(cubes[0].cubies[cubes[0].getCubieByPos((1,1,-1))].getOrientationFace(ROUGE))
    #cubes[0].action.actions.append("H CWI")
    #cubes[0].action.actions.append("H CWI")
    #cubes[0].action.actions.append("B CWI")
    #cubes[0].action.actions.append("B CWI")
    #cubes[0].action.actions.append("D CWI")
    #cubes[0].action.actions.append("D CWI")
    #cubes[0].action.actions.append("G CWI")
    #cubes[0].action.actions.append("G CWI")
    #cubes[0].action.actions.append("AV CWI")
    #cubes[0].action.actions.append("AV CWI")
    #cubes[0].action.actions.append("AR CWI")
    #cubes[0].action.actions.append("AR CWI")
    #cubes[0].action.doAll()
    #cubes[0].action.actions.append("ALEA")
    #cubes[0].resoudre()
    while True:
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        pygame.quit()
        #        sys.exit()
        #    if event.type == pygame.KEYDOWN:
        #        if event.key == pygame.K_SPACE:
        #            if rot:
        #                rot = False
        #            else:
        #                rot = True
        #        if event.key == pygame.K_LEFT:
        #            angle = 5
        #        if event.key == pygame.K_RIGHT:
        #            angle = -5
        screen.fill((255,255,255))
        for cube in cubes:
            cube.run()
        pygame.display.flip()
        #pygame.time.wait(25)
        if rot:
            for cube in cubes:
                orientation = cube.orientation
                cube.orientation = [alpha + angle for alpha in orientation]
        
        if prendreImage:
            pygame.image.save(screen,"./img/pasDeTrie.png")
            prendreImage = False

        