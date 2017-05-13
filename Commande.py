#!/usr/bin/env python3
#coding: utf-8

"""
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

@author: Maxime Keller
"""
import pygame
from pygame.locals import *
from ConstanteTouche import *
from Action import Action

#pygame.init()

class Commande:
    """Objet permettant de gérer les touches du clavier"""
    
    def __init__(self, parent):
        self.action = Action(parent)
        self.KANOMI = (K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, TOUCHE_b, TOUCHE_a)
        self.iKonami = 0
    
    def testKonamie(self, event):
        """Fait avancer, ou remet a 0, le konami code."""
        if event.key == self.KANOMI[self.iKonami]:
            self.iKonami += 1
            if event.key == TOUCHE_a:
                event.key = None
        else:
            self.iKonami = 0
        if self.iKonami == 10:
            self.iKonami = 0
            self.action.actions.append("SOLVE")
    
    def touches(self):
        """Les touches sont reliés a un autre programme"""

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                self.testKonamie(event)
                if event.key == TOUCHE_a:
                    self.action.actions.append("ALEA")
                    print("alea")
                elif event.key == TOUCHE_e :
                    self.action.actions.append("H CW")
                elif event.key == TOUCHE_r :
                    self.action.actions.append("B CW")  
                elif event.key == TOUCHE_y :
                    self.action.actions.append("AV CW")
                elif event.key == TOUCHE_u :
                    self.action.actions.append("AR CW")                  
                elif event.key == TOUCHE_o :
                    self.action.actions.append("G CW")
                elif event.key == TOUCHE_p :
                    self.action.actions.append("D CW")     
                elif event.key == TOUCHE_d :
                    self.action.actions.append("H ACW")
                elif event.key == TOUCHE_f :
                    self.action.actions.append("B ACW")                                     
                elif event.key == TOUCHE_h :
                    self.action.actions.append("AV ACW")
                elif event.key == TOUCHE_j :
                    self.action.actions.append("AR ACW")                                     
                elif event.key == TOUCHE_l :
                    self.action.actions.append("G ACW")
                elif event.key == TOUCHE_m :
                    self.action.actions.append("D ACW")
                elif event.key == TOUCHE_z :
                    print("stop")
                #    self.orientation[1] = -45
                #elif event.key == K_RIGHT :
                #    self.orientation[0] = -45
                #    self.orientation[2] = -45
                #elif event.key == K_LEFT :
                #    self.orientation[2] = 135
                #    self.orientation[0] = 135
            #elif event.type == KEYUP:
            #    if event.key == K_UP :
            #        self.orientation[1] = 45
            #    elif event.key == K_RIGHT :
            #        self.orientation[0] = 45
            #        self.orientation[2] = 45
            #    elif event.key == K_LEFT :
            #        self.orientation[2] = 45
            #        self.orientation[0] = 45