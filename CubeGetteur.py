#!/usr/bin/env python3
#coding: utf-8
'''
Created on 5 avr. 2017

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

@author: <mineau.jean.marie@gmail.com>
Sert à traiter des cubies.
'''

from operator import itemgetter

class CubeGetteur:
    """Sert à traiter des cubies."""
    
    def __init__(self):
        pass
    
    def getH(self):
        """Récupère les cubie du haut et retourne leur index."""
        cubiesH = []
        for cubie in self.cubies:
            if len(cubiesH) < 9:
                cubiesH.append([self.cubies.index(cubie), cubie.centre.y])
            else:
                cubiesH = sorted(cubiesH,key=itemgetter(1))
                if cubiesH[0][1] < cubie.centre.y:
                    cubiesH = cubiesH[1:]
                    cubiesH.append([self.cubies.index(cubie), cubie.centre.y])
        cubiesH = [item[0] for item in cubiesH]
        return cubiesH
    
    def getB(self):
        """Récupère les cubie du bas et retourne leur index."""
        cubiesH = []
        for cubie in self.cubies:
            if len(cubiesH) < 9:
                cubiesH.append([self.cubies.index(cubie), cubie.centre.y])
            else:
                cubiesH = sorted(cubiesH,key=itemgetter(1), reverse=True)
                if cubiesH[0][1] > cubie.centre.y:
                    cubiesH = cubiesH[1:]
                    cubiesH.append([self.cubies.index(cubie), cubie.centre.y])
        cubiesH = [item[0] for item in cubiesH]
        return cubiesH

    def getD(self):
        """Récupère les cubie de droite et retourne leur index."""
        cubiesD = []
        for cubie in self.cubies:
            if len(cubiesD) < 9:
                cubiesD.append([self.cubies.index(cubie), cubie.centre.x])
            else:
                cubiesD = sorted(cubiesD,key=itemgetter(1))
                if cubiesD[0][1] < cubie.centre.x:
                    cubiesD = cubiesD[1:]
                    cubiesD.append([self.cubies.index(cubie), cubie.centre.x])
        cubiesD = [item[0] for item in cubiesD]
        return cubiesD
    
    def getG(self):
        """Récupère les cubie de Gauche et retourne leur index."""
        cubiesG = []
        for cubie in self.cubies:
            if len(cubiesG) < 9:
                cubiesG.append([self.cubies.index(cubie), cubie.centre.x])
            else:
                cubiesG = sorted(cubiesG,key=itemgetter(1), reverse=True)
                if cubiesG[0][1] > cubie.centre.x:
                    cubiesG = cubiesG[1:]
                    cubiesG.append([self.cubies.index(cubie), cubie.centre.x])
        cubiesG = [item[0] for item in cubiesG]
        return cubiesG
    
    def getAv(self):
        """Récupère les cubie derrière et retourne leur index."""
        cubiesA = []
        for cubie in self.cubies:
            if len(cubiesA) < 9:
                cubiesA.append([self.cubies.index(cubie), cubie.centre.z])
            else:
                cubiesH = sorted(cubiesA,key=itemgetter(1), reverse=True)
                if cubiesH[0][1] > cubie.centre.z:
                    cubiesA = cubiesH[1:]
                    cubiesA.append([self.cubies.index(cubie), cubie.centre.z])
        cubiesA = [item[0] for item in cubiesA]
        return cubiesA

    def getAr(self):
        """Récupère les cubie de derrière et retourne leur index."""
        cubiesA = []
        for cubie in self.cubies:
            if len(cubiesA) < 9:
                cubiesA.append([self.cubies.index(cubie), cubie.centre.z])
            else:
                cubiesA = sorted(cubiesA,key=itemgetter(1))
                if cubiesA[0][1] < cubie.centre.z:
                    cubiesA = cubiesA[1:]
                    cubiesA.append([self.cubies.index(cubie), cubie.centre.z])
        cubiesA = [item[0] for item in cubiesA]
        return cubiesA         
    
    def getCubieByPos(self, pos):
        """Retourne l'indice du Cubie de pos donné. Cette pos est relative au cube,
        elle est donné en x,y,z, l'origine étant le centre du cube, et l'unité
        correspond à 1 cubie."""
        
        if pos[0] == -1:
            potentielsCubies = self.getG()
        elif pos[0] == 1:
            potentielsCubies = self.getD()
        elif pos[0] == 0:
            #Celui est est plus embetant, il n'y a pas de méthode pour les recuperer
            #Donc c'est toutes les valeur sauf celle des deux autre tranchhes.
            indicesFaux = self.getG() + self.getD()
            potentielsCubies = [i for i in range(len(self.cubies)) if i not in indicesFaux]
        else: 
            raise ValueError("Vous devez demander une ordonné de -1, 0 ou 1")
            # Parce que la pep 20 est bien
        
        if pos[1] == -1:
            potentielsCubies = [i for i in potentielsCubies if i in self.getB()]
        elif pos[1] == 1:
            potentielsCubies = [i for i in potentielsCubies if i in self.getH()]
        elif pos[1] == 0:
            indicesFaux = self.getB() + self.getH()
            potentielsCubies = [i for i in potentielsCubies if i not in indicesFaux]
        else: 
            raise ValueError("Vous devez demander une abscice de -1, 0 ou 1")
            #Errors should never pass silently.
            
        if pos[2] == -1:
            potentielsCubies = [i for i in potentielsCubies if i in self.getAv()]
        elif pos[2] == 1:
            potentielsCubies = [i for i in potentielsCubies if i in self.getAr()]
        elif pos[2] == 0:
            indicesFaux = self.getAv() + self.getAr()
            potentielsCubies = [i for i in potentielsCubies if i not in indicesFaux]
        else: 
            raise ValueError("Vous devez demander une profondeur de -1, 0 ou 1")
            #Oui, aujourd'hui j'ai voulu faire propre.
        
        if len(potentielsCubies) > 1:
            raise Exception("Maxime, je sait pas comment t'as fait, mais t'as réussit à trouver \
            Une coordonnée avec plusieurs Cubie!!!")
        elif len(potentielsCubies) == 0:
            raise Exception("Pas de Cubies ici, peut être avez vous demandé l'origine?")
        else:
            return potentielsCubies[0]
    
    def getCubieByColors(self, couleurs):
        """Retourne l'indice du Cubie de couleurs données. Ces couleurs sont 
        une liste donnant les couleurs exact, mais pas obligatoirement dans l'ordre."""
        for cubie in self.cubies:
            if len(couleurs) != len(cubie.couleursResolution):
                continue
            bonCubie = True
            for couleur in couleurs:
                if couleur not in cubie.couleursResolution:
                    bonCubie = False
                    break
            if bonCubie: return self.cubies.index(cubie)
        raise Exception("Pas de cubies correspondanr aux couleurs données.")
        
    def getPosRelative(self, cubie):
        """Retourne la position relative du cubie (don on donne l'indice)."""
        
        if cubie not in range(len(self.cubies)):
            raise ValueError("Vous devez rentrer un indice de l'argument 'cubies'.")
        
        if cubie in self.getG():
            x = -1
        elif cubie in self.getD():
            x = 1
        else:
            x = 0
            
        if cubie in self.getB():
            y = -1
        elif cubie in self.getH():
            y = 1
        else :
            y = 0
            
        if cubie in self.getAv():
            z = -1
        elif cubie in self.getAr():
            z = 1
        else:
            z = 0
        
        return x, y, z