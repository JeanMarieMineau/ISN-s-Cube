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

@author: <mineau.jean.marie@gmail.com>
programme réalisé sur une base du programme dévellopé par Leonel Machava <leonelmachava@gmail.com>
 http://codeNtronix.com 
'''
from random import choice
        
class Action:
    """Object qui permet de tourner les faces."""
    
    def __init__(self, parent):
        """parent est le cube qui utilise l'instance."""
        self.parent = parent
        self.angle = 0          # Angle restant à parcourir
        self.actions = []       # Actions à effectuer
        self.indexs = []        # Indices des cubies à tourner
        self.anglesRotation = []# Angle en x, y, et z à tourner.
        self.listeActionsPossible = ["H CWI", "H ACWI",
                                     "B CWI", "B ACWI",
                                     "D CWI", "D ACWI",
                                     "G CWI", "G ACWI",
                                     "AV CWI", "AV ACWI",
                                     "AR CWI", "AR ACWI"]


    def doAll(self):
        """Execute toutes les actions de la liste."""
        while self.actions:
            self.__call__()
            
    def __call__(self):
        """Méthode principale."""
        if self.angle == 0 and not self.actions:
            #self.actions.append("ALEA")
            return #Si l'action est terminée et qu'il n'y en a pas d'autre, on passe.
        elif self.angle == 0:
            self.initNewAction()
        
        for i in self.indexs:
            self.parent.cubies[i] = self.parent.cubies[i].rotationX(self.anglesRotation[0])
            self.parent.cubies[i] = self.parent.cubies[i].rotationY(self.anglesRotation[1])
            self.parent.cubies[i] = self.parent.cubies[i].rotationZ(self.anglesRotation[2])
        angle = 0
        for i in self.anglesRotation:
            angle += i
        if self.angle < 0:
            print("deadlock")
        self.angle -= abs(angle)
            
    def initNewAction(self, actions = None):
        """Initialise une nouvelle action. Si une action est mise en argument, 
        elle est initialisée, sinon, l'action est prise dans la liste d'action."""
        if actions:
            commande = actions
            actions.split()
        else:
            commande = self.actions.pop(0)
            actions = commande.split()
        if actions[0] == "ALEA":
            self.melange()
            if self.actions:
                actions = self.actions.pop(0).split()
        if actions[0] == "SOLVE":
            self.resoudre()
        elif actions[1] == "CW":
            self.angle = 90
            angle = 10
        elif actions[1] == "ACW":
            self.angle = 90
            angle = -10
        elif actions[1] == "CWI":
            self.angle = 90
            angle = 90
        elif actions[1] == "ACWI":
            self.angle = 90
            angle = -90
        else:
            raise ValueError("La valeur " + str(actions[1]) + " est inconnue.")
            
        x, y, z = 0, 0, 0
        if actions[0] == "H":
            y = angle
            self.indexs = self.parent.getH()
        elif actions[0] == "B":
            y = angle
            self.indexs = self.parent.getB()
        elif actions[0] == "G":
            x = angle
            self.indexs = self.parent.getG()
        elif actions[0] == "D":
            x = angle
            self.indexs = self.parent.getD()
        elif actions[0] == "AV":
            z = angle
            self.indexs = self.parent.getAv()
        elif actions[0] == "AR":
            z = angle
            self.indexs = self.parent.getAr()
        elif actions[0] == "X":
            x = angle
            self.indexs = [i for i in range(len(self.parent.cubies))]
        elif actions[0] == "Y":
            y = angle
            self.indexs = [i for i in range(len(self.parent.cubies))]
        elif actions[0] == "Z":
            z = angle
            self.indexs = [i for i in range(len(self.parent.cubies))]
        elif actions[0] != "SOLVE" and actions[0] != "ALEA":
            raise ValueError("La commande " + str(commande) + " est inconnue.")
        self.anglesRotation = [x, y, z]
    
    def melange(self):
        """Met des actions aléatoire dans la liste d'action."""
        liste = []
        while len(liste) < 21:
            liste.append(choice(self.listeActionsPossible))
        self.actions = liste + self.actions
        print(liste)
        
    def resoudre(self):
        """Lance la resolution."""
        self.parent.resoudre()
