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

@author: <mineau.jean.marie@gmail.com>

Interface de boutons fait à la va vite.
"""

import pygame
from Bouton import Boutons

 
def addAction(cube, action):
	"""Ajoute une action à la liste."""

	cube.action.actions.append(action)

CARACTS_BOUTONS = [[(100,30), "img/B1.png", addAction, ["ALEA"]], 
				   [(400,30), "img/B2.png", addAction, ["SOLVE"]], 
				   [(100,600), None, addAction, ["B CW"]],
				   [(500,600), None, addAction, ["B ACW"]],
				   [(200,600), None, addAction, ["AV CW"]],
				   [(400,600), None, addAction, ["AV ACW"]],
				   [(100,150), None, addAction, ["H CW"]],
				   [(500,150), None, addAction, ["H ACW"]],
				   [(200,150), None, addAction, ["AR CW"]],
				   [(400,150), None, addAction, ["AR ACW"]],
				   [(100,350), None, addAction, ["G CW"]],
				   [(100,450), None, addAction, ["G ACW"]],
				   [(500,350), None, addAction, ["D CW"]],
				   [(500,450), None, addAction, ["D ACW"]]]

class InterfaceBoutons:
	"""interface gérant l'ensemble des boutons."""

	def __init__(self, screen, cube, caractsBoutons=None):
		"""caractsBoutons est une liste contenants des listes
		de caracteristiques des boutons, dans l'ordre:
		[position, img, callback, argsCallback]"""

		if caractsBoutons is None:
			caractsBoutons = CARACTS_BOUTONS

		self.screen = screen
		self.cube = cube

		self.boutons = Boutons()

		for caracts in caractsBoutons:
			pos, img, callback, argsCallback = caracts
			# Bon c'est pas propre mais faut bien mettre le Cube
			# quelque part...
			argsCallback = [self.cube] + argsCallback
			self.boutons.nouveauBouton(pos, image=img, callback=callback, 
				argsCallback=argsCallback)

	def run(self):
		"""Affiche et check les envents pour une itération de la
		boucle principale."""

		events = self.cube.events
		self.boutons.update(events)
		self.boutons.display(self.screen)
