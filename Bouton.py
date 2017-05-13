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

@author: <mineau.jean.marie@gmail.com>

Class pour les boutons. Une classe qui gère l'ensemble des
boutons, et une autre qui est le bouton. 
'''

import pygame

class Boutons:
    """Class gérant la création de boutons et le fait de clique dessus,
    ainsi que l'affichage."""
    
    def __init__(self):
        """Cette class à pour attribut une liste de boutons."""
        
        self.boutons = []
    
    def nouveauBouton(self, pos, image=None, couleur=(255,0,255), 
                      size=(60,60), callback=lambda *args: None, argsCallback=[]):
        """Crée un nouveau bouton."""
        
        bouton = Bouton(pos, self, image=image, couleur=couleur,
                        size=size, callback=callback, argsCallback=argsCallback)
        self.boutons.append(bouton)
        return bouton
    
    def update(self, events):
        """Gère le click sur le bouton."""
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                self.callbackClic(pos)
    
    def callbackClic(self, pos):
        """Methode appellé lors d'un clic."""
        
        for bouton in self.boutons:
            if bouton.rect.collidepoint(*pos):
                bouton.callback(*bouton.argsCallback)
                return

    def display(self, screen):
        """Affiche les Boutons."""
        
        for bouton in self.boutons:
            bouton.display(screen)
    
        
class Bouton:
    """Un Bouton."""
    
    def __init__(self, pos, parent, image=None, couleur=(255,0,255),
                size=(60,60), callback=lambda *args: None, argsCallback=[]):
        """Crée un bouton, si une image est donné, il la charge, sinon, 
        c'est un rectangle de taille size et de couleur couleur qui est affiché."""
        
        self.parent = parent
        self.pos = pos
        if image is not None:
            self.surface = pygame.image.load(image).convert_alpha()
            self.rect = self.surface.get_rect()
        else:
            self.surface = pygame.Surface(size)
            self.surface.fill(couleur)
            self.rect = self.surface.get_rect()
        self.rect = self.rect.move(self.pos)
        self.callback = callback
        self.argsCallback = argsCallback
    
    def suppr(self):
        """Suprime le Bouton."""
        
        self.parent.boutons.remove(self)

    def display(self, screen):
        """Affiche le Bouton."""
        
        screen.blit(self.surface, self.rect)

def callbackTest(a, b, c, d, e, f, g):
    """Test de callback."""
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)

def callback2(*args):
    print("toto")
    

if __name__ == "__main__":
    
    boutons = Boutons()
    
    screen = pygame.display.set_mode((1000, 400))
    clock = pygame.time.Clock()
    
    pos = (50,50)
    bouton = boutons.nouveauBouton(pos, callback=callbackTest, argsCallback=["A",
                                                                            "B",
                                                                            "C",
                                                                            "D",
                                                                            "E",
                                                                            "F",
                                                                            "G"])
    
    pos2 = (50, 200)
    bouton2 = boutons.nouveauBouton(pos2, callback=callback2, argsCallback=["H",
                                                                              "I",
                                                                              "J",
                                                                              "K",
                                                                              "L",
                                                                              "M",
                                                                              "N"])

    while True:
        screen.fill((150, 150, 150))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                quit()
        boutons.update(events)
        boutons.display(screen)
        pygame.display.update()
        clock.tick(30)
        