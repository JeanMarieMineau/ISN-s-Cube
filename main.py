#!/usr/bin/env python3
#coding: utf-8

'''
Created on 5 mai 2017

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
 
 https://www.python.org/ (c'est le language, donc important) 
 Module principale du programme de Rubicks cube.
'''

import this # (c'est important aussi)
import pygame
from Cube import Cube
from InterfaceBoutons import InterfaceBoutons

if __name__ == "__main__":
    
    pygame.init()
          
    surfaceCube = pygame.Surface((500, 500))
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("ISN's Cube")   
    
    cube = Cube(surfaceCube)
    interfaceBoutons = InterfaceBoutons(screen, cube)

    while True:
        surfaceCube.fill((255,255,255))
        screen.fill((255,255,255))
        cube.run()
        screen.blit(surfaceCube, (100,100))
        interfaceBoutons.run()
        pygame.display.flip()
        pygame.time.wait(25)
        
