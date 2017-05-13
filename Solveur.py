#!/usr/bin/env python3
# coding: utf-8
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
Solveur du cube à faire hériter à un Cube.
'''

class Solver:
    """Class pour résoudre le Cube,
    Faire hériter. 
    Résoud un reflet avec des action instantanées 
    (en ajoutant un I a la direction, CWI ou ACWI)"""
    
    def __init__(self):
        pass
    
    def resoudre(self):
        """Méthode principale.
        Pour une question de vitesse, elle résoud un cube virtuel (reflet)
        et retourn la liste d'action à éfectuer sur le modèle d'origine."""
        ####/DEBUG\####
        self.action.doAll()
        ####\DEBUG/####
        resolution = []
        reflet = self.creationRefletNonOriente()
        resolution.extend(self.croixHaute(reflet))
        resolution.extend(self.coinsHaut(reflet))
        resolution.extend(self.arretesMilieu(reflet))
        actions = ["X CW", "X CW"]
        resolution.extend(actions)
        reflet.action.actions.extend([action + "I" for action in actions])
        reflet.action.doAll()
        resolution.extend(self.croixBas(reflet))
        resolution.extend(self.croixBasArrete(reflet))
        resolution.extend(self.coinsBasPos(reflet))
        resolution.extend(self.orientationCoinsBas(reflet))
        ####/DEBUG\####
        #resolution = [i + "I" for i in resolution]
        #self.action.actions.extend(resolution)
        #self.action.doAll()
        #resolution =[]
        ####\DEBUG/####
        print(resolution)
        self.action.actions.extend(resolution)
    
    def croixHaute(self, cube):
        """Résoud la croix du haut."""
        resolution = []
        for i in range(4):
            resolution.extend(self.croixHauteArreteDeFace(cube))
            cube.action.actions.append("Y CWI")
            cube.action.doAll()
            resolution.append("Y CW")
        return resolution
            
    def croixHauteArreteDeFace(self, cube):
        """Place l'arrete de face."""
        resolution = []
        #Positionne l'arrete
        centreAv = cube.getCubieByPos((0,0,-1))
        centreH = cube.getCubieByPos((0,1,0))
        couleurAv = cube.cubies[centreAv].couleursResolution[0]
        couleurH = cube.cubies[centreH].couleursResolution[0]
        couleursArrete = [couleurAv, couleurH]
        arrete = cube.getCubieByColors(couleursArrete)
        posArrete = cube.getPosRelative(arrete)
        ####/DEBUG\####
        #savePos = posArrete
        ####\DEBUG/####
        
        # Le but de cette parti est de placer l'arrete en (1,-1,0), cad face de droite millieu bas.
        if posArrete == (0,1,-1):   #La position finale
            orientation = cube.cubies[arrete].getOrientationFace(couleurH)
            if orientation == (0,1,0): #Vers le Haut
                return resolution
            else:
                actions = ["AV CW", "AV CW", "B ACW"]
                resolution.extend(actions)
                cube.action.actions.extend([action + "I" for action in actions])
                cube.action.doAll()
                
        elif posArrete[1] == 1:     #Le cubie est sur la face du Haut
            if posArrete[0] == -1:
                actions = ["G CW", "G CW"]
            elif posArrete[0] == 0:
                actions = ["AR CW", "AR CW"]
            elif posArrete[0] == 1:
                actions = ["D CW", "D CW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
            
        elif posArrete[1] == 0:         # Le cubie est sur la tranche du Millieu
            if posArrete[0] == -1:      # Cette action place place ce cubie sur la face du Bas, mais pas forcement
                if posArrete[2] == -1:  # à la bonne place
                    actions = ["G ACW", "B CW", "G CW"]
                elif posArrete[2] == 1:
                    actions = ["G CW", "B CW", "G ACW"]
            elif posArrete[0] == 1:
                if posArrete[2] == -1:  
                    actions = ["D ACW", "B CW", "D CW"]
                elif posArrete[2] == 1:
                    actions = ["D CW", "B CW", "D ACW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
            
        #Normalement, arrivé ici, l'arrete est forcement sur la face du bas.
        posArrete = cube.getPosRelative(arrete)
        ####/DEBUG\####
        #if posArrete[1] != -1:
        #    print("error")
        #    print(savePos)
        #nbIter = 0
        ####\DEBUG/####
        while not posArrete == (1,-1,0):
            actions = ["B CW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
            posArrete = cube.getPosRelative(arrete)
            ####/DEBUG\####
            #nbIter += 1
            #if nbIter > 10:
            #    print("Error")
            ####\DEBUG/####
        
        #Maintenant, la face est en (1,-1,0), il reste une formule à appliquer,
        #qu'il faut choisir en fonction de l'orientation du cubie.
        orientation = cube.cubies[arrete].getOrientationFace(couleurH)
        if orientation == (0,-1,0):
            actions = ["B CW", "AV CW", "AV CW"]
        else:
            actions = ["D CW", "AV CW", "D ACW"] 
        resolution.extend(actions)
        cube.action.actions.extend([action + "I" for action in actions])
        cube.action.doAll()
        # Une arrete de finit!
        return resolution
    
    def coinsHaut(self, cube):
        """Résoud les coins de la face du haut."""
        resolution = []
        for i in range(4):
            resolution.extend(self.coinHaut(cube))
            cube.action.actions.append("Y CWI")
            cube.action.doAll()
            resolution.append("Y CW")
        return resolution
    
    def coinHaut(self, cube):
        """Résoud le coin en (1,1,-1), cad face avant, coin haut droit."""
        resolution = []
        #Position du coin
        centreAv = cube.getCubieByPos((0,0,-1))
        centreH = cube.getCubieByPos((0,1,0))
        centreD = cube.getCubieByPos((1,0,0))
        couleurAv = cube.cubies[centreAv].couleursResolution[0]
        couleurH = cube.cubies[centreH].couleursResolution[0]
        couleurD = cube.cubies[centreD].couleursResolution[0]
        couleursCoin = [couleurAv, couleurH, couleurD]
        coin = cube.getCubieByColors(couleursCoin)
        posCoin = cube.getPosRelative(coin)
        ####/DEBUG\####
        #savePos = posArrete
        ####\DEBUG/####
        
        #Si le point est en Haut, le but est de le mettre sur la face du Bas
        actions = None
        if posCoin == (1,1,-1): #Pos final
            orientation = cube.cubies[coin].getOrientationFace(couleurH)
            if orientation == (0,1,0):#Bien placé
                return resolution
            else:
                actions = ["D ACW", "B CW", "D CW"]
        elif posCoin == (1,1,1):
            actions = ["D CW", "B CW", "D ACW"]
        elif posCoin == (-1,1,1):
            actions = ["G CW", "B CW", "G ACW"]
        elif posCoin == (-1,1,-1):
            actions = ["G ACW", "B CW", "G CW"]
        if actions is not None:
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
        
        #Positionne le coin en (1,-1,-1), cad face avant, coin bas droit.
        posCoin = cube.getPosRelative(coin)
        ####/DEBUG\####
        #if posCoin[1] != -1:
        #    print("Error")
        ####\DEBUG/####
        while posCoin != (1,-1,-1):
            actions = ["B CW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
            posCoin = cube.getPosRelative(coin)
        
        #Positionne le coin en (1,1,-1) et l'oriente.
        orientation = cube.cubies[coin].getOrientationFace(couleurH)
        if orientation == (1,0,0):
            actions = ["B ACW", "AV ACW", "B CW", "AV CW"]
        elif orientation == (0,-1,0):
            actions = ["D ACW", "B ACW", "D CW", "B CW", "AV ACW", "B CW", "AV CW"]
        else:
            actions = ["B CW", "D ACW", "B ACW", "D CW"]
        resolution.extend(actions)
        cube.action.actions.extend([action + "I" for action in actions])
        cube.action.doAll()
        return resolution
    
    def arretesMilieu(self, cube):
        """Résoud les arrêtes de la tranche du milieu."""
        resolution = []
        for i in range(4):
            resolution.extend(self.arreteMillieuxDroit(cube))
            cube.action.actions.append("Y CWI")
            cube.action.doAll()
            resolution.append("Y CW")
        return resolution
    
    def arreteMillieuxDroit(self, cube):
        """Résoud l'arrete du milieux droit de la face Avant (1,0,-1)."""
        resolution = []
        #Positionne l'arrete
        centreAv = cube.getCubieByPos((0,0,-1))
        centreD = cube.getCubieByPos((1,0,0))
        couleurAv = cube.cubies[centreAv].couleursResolution[0]
        couleurD = cube.cubies[centreD].couleursResolution[0]
        couleursArrete = [couleurAv, couleurD]
        arrete = cube.getCubieByColors(couleursArrete)
        posArrete = cube.getPosRelative(arrete)
        
        orientation = cube.cubies[arrete].getOrientationFace(couleurAv)
        if posArrete == (1,0,-1) and orientation == (0,0,-1):
            return resolution
        
        elif posArrete[1] == 0:
            #Si l'arrete est sur la tranche du milieu.
            while not posArrete == (1,0,-1):
                #positionne le cube de facon à placer l'arrete en (1,0,-1)
                cube.action.actions.append("Y CWI")
                cube.action.doAll()
                resolution.append("Y CW")
                posArrete = cube.getPosRelative(arrete)
            resolution.extend(self.belgeD(cube))
            
            posCentreAv = cube.getPosRelative(centreAv)
            while not posCentreAv == (0,0,-1):
                #positionne le cube de facon à replacer la face de depart en face.
                cube.action.actions.append("Y CWI")
                cube.action.doAll()
                resolution.append("Y CW")
                posCentreAv = cube.getPosRelative(centreAv)
                
        posArrete = cube.getPosRelative(arrete)
        while not posArrete == (0,-1,-1):
            #Place l'arrete en bas de la face.
            cube.action.actions.append("B CWI")
            cube.action.doAll()
            resolution.append("B CW")
            posArrete = cube.getPosRelative(arrete)
            
        orientation = cube.cubies[arrete].getOrientationFace(couleurAv)
        if orientation == (0,0,-1):
            resolution.extend(self.belgeD(cube))
        else: 
            actions = ["Y CW", "B ACW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
            resolution.extend(self.belgeG(cube))
            cube.action.actions.append("Y ACWI")
            cube.action.doAll()
            resolution.append("Y ACW")
            posArrete = cube.getPosRelative(arrete)
            
        posArrete = cube.getPosRelative(arrete)
        ####/DEBUG\####
        #if posArrete != (1,0,-1):
        #    print("error")
        #    print(resolution)
        ####\DEBUG/####
        
        return resolution

    def belgeD(self, cube):
        """Applique l'algo du Belge à droite."""
        resolution = ["B CW", "D ACW", "B ACW", "D CW", "B ACW", "AV ACW", "B CW", "AV CW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution
    
    def belgeG(self, cube):
        """Applique l'algo du Belge à gauche."""
        resolution = ["B ACW", "G ACW", "B CW", "G CW", "B CW", "AV CW", "B ACW", "AV ACW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution
    
    def croixBas(self, cube):
        """Résoud la croix du bas (pour la resolution, le cube est retourné, 
        donc la croix du bas est en fait en haut)."""
        resolution = []
        posAretes, boolOrientation, nbBienOriente = self.croixBasOrientation(cube)
        iG = posAretes.index((-1,1,0))
        iD = posAretes.index((1,1,0))
        iAv = posAretes.index((0,1,-1))
        iAr = posAretes.index((0,1,1))
        
        if nbBienOriente == 4:
            return resolution
        
        elif nbBienOriente == 0:
            resolution.extend(self.algoCroixBas(cube))
            cube.action.actions.append("Y CWI")
            cube.action.doAll()
            resolution.append("Y CW")
            resolution.extend(self.algoCroixBas(cube))
            resolution.extend(self.algoCroixBas(cube))
            return resolution
        
        elif nbBienOriente == 2:
            aligne = (boolOrientation[iG] and boolOrientation[iD]) or \
                    (boolOrientation[iAr] and boolOrientation[iAv]) 
            if aligne:
                if not (boolOrientation[iAr] and boolOrientation[iAv]):
                    cube.action.actions.append("Y CWI")
                    cube.action.doAll()
                    resolution.append("Y CW")
                resolution.extend(self.algoCroixBas(cube))
                resolution.extend(self.algoCroixBas(cube))
                    
            else:
                while not (boolOrientation[iAr] and boolOrientation[iG]):
                    cube.action.actions.append("Y CWI")
                    cube.action.doAll()
                    resolution.append("Y CW")
                    posAretes, boolOrientation, nbBienOriente = self.croixBasOrientation(cube)
                resolution.extend(self.algoCroixBas(cube))
        
        else: 
            print("Mais commenent quoi comment?")
        return resolution        
    
    def croixBasOrientation(self, cube):
        """Retourne une liste associant position des arretes 
        et une bool indiquant si leur orientation est bonne 
        au pas et le nombre d'orientation correct."""
        #Résoud les orientation
        centreH = cube.getCubieByPos((0,1,0))
        couleurH = cube.cubies[centreH].couleursResolution[0]
        
        retourBoolOrientation = []
        retourPos = [(-1,1,0), (0,1,-1), (1,1,0), (0,1,1)]
        nbOrientationBonnes = 0
        for pos in retourPos:
            cubie = cube.getCubieByPos(pos)
            orientation = cube.cubies[cubie].getOrientationFace(couleurH)
            if orientation == (0,1,0):
                boolOrientation = True
                nbOrientationBonnes += 1
            else: boolOrientation = False
            retourBoolOrientation.append(boolOrientation)
                    
        return retourPos, retourBoolOrientation, nbOrientationBonnes
    
    def algoCroixBas(self, cube):
        """Applique l'algo pour la croix du bas."""
        resolution = ["D ACW", "H ACW", "AV CW", "H CW", "AV ACW", "D CW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution
    
    def croixBasArrete(self, cube):
        """Resolution de la position des arretes de la face du bas."""
        resolution = []
        posAretes, posTheo, nbPosBonnes = self.testCroixBas(cube)
        iG = posAretes.index((-1,1,0))
        iD = posAretes.index((1,1,0))
        iAv = posAretes.index((0,1,-1))
        iAr = posAretes.index((0,1,1))

        if nbPosBonnes == 4:
            return resolution

        while nbPosBonnes == 0:
            cube.action.actions.append("H CWI")
            cube.action.doAll()
            resolution.append("H CW")
            posAretes, posTheo, nbPosBonnes = self.testCroixBas(cube)

        if nbPosBonnes == 4:
            return resolution

        if nbPosBonnes == 2:
            aligne = (posAretes[iG] == posTheo[iG]) and (posAretes[iD] == posTheo[iD]) or \
                    (posAretes[iAv] == posTheo[iAv]) and (posAretes[iAr] == posTheo[iAr])
            if aligne:
                if posAretes[iD] == posTheo[iD]:
                    cube.action.actions.append("H CWI")
                    cube.action.doAll()
                    resolution.append("H CW")
                resolution.extend(self.algoTCW(cube))
                posAretes, posTheo, nbPosBonnes = self.testCroixBas(cube)
                while nbPosBonnes == 0:
                    cube.action.actions.append("H CWI")
                    cube.action.doAll()
                    resolution.append("H CW")
                    posAretes, posTheo, nbPosBonnes = self.testCroixBas(cube)
                    
                if nbPosBonnes == 4:
                    return resolution
                elif nbPosBonnes == 2:
                    print("Mais, cette configuration n'est pas sensé exister!")
                    return resolution
            
            else:
                #nbBoucle = 0
                while nbPosBonnes != 1:
                    cube.action.actions.append("H CWI")
                    cube.action.doAll()
                    resolution.append("H CW")
                    posAretes, posTheo, nbPosBonnes = self.testCroixBas(cube)
                    ####/DEBUG\####
                    #nbBoucle += 1
                    #if nbBoucle > 10:
                    #    print("Trop d'iteration")
                    ####\DEBUG/####

        if nbPosBonnes == 1:
            while posAretes[iG] != posTheo[iG]:
                cube.action.actions.append("Y CWI")
                cube.action.doAll()
                resolution.append("Y CW")
                posAretes, posTheo, nbPosBonnes = self.testCroixBas(cube)
            if posAretes[iAv] == posTheo[iAr]:
                resolution.extend(self.algoTCW(cube))
            elif posAretes[iAr] == posTheo[iAv]:
                resolution.extend(self.algoTACW(cube))       
            else:
                print("wtf")

        return resolution
    
    def algoTACW(self, cube):
        """Algo de resolution en T dans le sens anti horaire, 
        décale les cubies de la face du haut en forme de T
        orienté le bas à droite, le haut à gauche.
        Permet aussi de changer l'orientation des coins combinés à
        algoTCW."""
        resolution = ["D ACW", "H ACW", "D CW", "H ACW", "D ACW", "H ACW", "H ACW", "D CW", "H ACW", "H ACW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution 

    def algoTCW(self, cube):
        """Algo de resolution en T dans le sens horaire, 
        décale les cubies de la face du haut en forme de T
        orienté le bas à droite, le haut à gauche.
        Permet aussi de changer l'orientation des coins combinés à
        algoTACW."""
        resolution = ["D CW", "H CW", "D ACW", "H CW", "D CW", "H CW", "H CW", "D ACW", "H CW", "H CW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution 

    def testCroixBas(self, cube):
        """Test les arrete de la croix bas (donc en haut car le cube est retourné).
        Retourne la position des cubies, la position final des cubies et le nombre
        de cubies à la bonne place."""
        centreH = cube.getCubieByPos((0,1,0))
        couleurH = cube.cubies[centreH].couleursResolution[0]
        
        retourPosTheo = [None, None, None, None]
        nbPosBonnes = 0
        
        retourPos = [(-1,1,0), (0,1,-1), (1,1,0), (0,1,1)]
        couleursFace = []
        for p in retourPos:
            p = (p[0],0,p[2])
            c = cube.getCubieByPos(p)
            couleursFace.append(cube.cubies[c].couleursResolution[0])
        
        for p in retourPos:
            c = cube.getCubieByPos(p)
            couleur = [ i for i in cube.cubies[c].couleursResolution if i != couleurH][0]
            i = couleursFace.index(couleur)
            retourPosTheo[i] = p
            if i == retourPos.index(p):
                nbPosBonnes += 1
        
        return retourPos, retourPosTheo, nbPosBonnes
    
    def coinsBasPos(self, cube):
        """Place les coins du bas (du haut comme le cube est retourné) 
        à leur position."""
        resolution = []
        posCoins, posCoinsTheo, nbPosBonnes = self.testCoinsBas(cube)

        iAvG = posCoins.index((-1,1,-1))
        iAvD = posCoins.index((1,1,-1))
        iArD = posCoins.index((1,1,1))
        iArG = posCoins.index((-1,1,1))
        
        if nbPosBonnes == 0:
            resolution.extend(self.algoTriangleCW(cube))
        posCoins, posCoinsTheo, nbPosBonnes = self.testCoinsBas(cube)
        
        if nbPosBonnes == 4:
            return resolution
        elif nbPosBonnes != 1:
            print("On vous a bien dit que le tournevis n'est pas la solution!")
            return resolution
        
        while posCoins[iAvD] != posCoinsTheo[iAvD]:
            cube.action.actions.append("Y CWI")
            cube.action.doAll()
            resolution.append("Y CW")
            posCoins, posCoinsTheo, nbPosBonnes = self.testCoinsBas(cube)
            
        if posCoins[iArD] == posCoinsTheo[iAvG]:
            resolution.extend(self.algoTriangleCW(cube))
        elif posCoins[iAvG] == posCoinsTheo[iArD]:
            cube.action.actions.append("Y CWI")
            cube.action.doAll()
            resolution.append("Y CW")
            resolution.extend(self.algoTriangleACW(cube))
        else:
            print("PAS DE TOURNEVIS!")
            
        return resolution
    
    def algoTriangleCW(self, cube):
        """Algorithme en triangle dans le sens horaire, sur la face du haut,
        décale les coins dans le sens hoaire, sauf le coin avant droit."""
        resolution = ["G CW", "H CW", "D CW", "H ACW", "G ACW", "H CW", "D ACW", "H ACW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution 
    
    def algoTriangleACW(self, cube):
        """Algorithme en triangle dans le sens anti horaire, sur la face du haut,
        décale les coins dans le sens anti hoaire, sauf le coin avant gauche."""
        resolution = ["D CW", "H ACW", "G CW", "H CW", "D ACW", "H ACW", "G ACW", "H CW"]
        cube.action.actions.extend([action + "I" for action in resolution])
        cube.action.doAll()
        return resolution 
    
    def testCoinsBas(self, cube):
        """Test les coins du bas (donc du haut car le cube est retourné).
        Retourne la position des cubies, la position final des cubies et le nombre
        de cubies à la bonne place."""
        retourPosTheo = [None, None, None, None]
        nbPosBonnes = 0
        
        retourPos = [(-1,1,-1), (1,1,-1), (1,1,1), (-1,1,1)]
        couleursCoins = []
        # Creer la liste couleursCoins qui contien la couleur des 
        # cubie qui devraient ce trouver à cette place.
        for p in retourPos:
            couleurs = []
            avancement = 0
            for i in p:
                pos = [0,0,0]
                pos[avancement] = i
                avancement += 1
                c = cube.getCubieByPos(tuple(pos))
                couleurs.append(cube.cubies[c].couleursResolution[0])
            couleursCoins.append(couleurs)
        
        for couleurs in couleursCoins:
            # Met la position théorique du coin dans la liste pos théorique
            # à l'indice correspondant à sa position.
            c = cube.getCubieByColors(couleurs)
            posRelative = cube.getPosRelative(c)
            retourPosTheo[couleursCoins.index(couleurs)] = posRelative
            if posRelative == retourPos[couleursCoins.index(couleurs)]:
                nbPosBonnes += 1
        
        return retourPos, retourPosTheo, nbPosBonnes
    
    def orientationCoinsBas(self, cube):
        """Oriente les coins de la face du bas (qui est en haut 
        car le cube est retourné)."""
        resolution = []
        posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
        
        #Indices des pos
        iAvG = posCoins.index((-1,1,-1))
        iAvD = posCoins.index((1,1,-1))
        iArD = posCoins.index((1,1,1))
        iArG = posCoins.index((-1,1,1))
        
        ####/DEBUG\####
        #print((orientationCoin, nbBonneOrientation))
        ####\DEBUG/####
        
        if nbBonneOrientation == 4:
            return resolution
        
        if nbBonneOrientation == 0:
            while not self.testOrientationCoinsBasHomogene(cube):
                cube.action.actions.append("Y CWI")
                cube.action.doAll()
                resolution.append("Y CW")
            resolution.extend(self.resolutionOrientationCoinsBasHomogene(cube))
            posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
            
        if nbBonneOrientation == 1:
            while not orientationCoin[iAvD] == (0,1,0):
                cube.action.actions.append("Y CWI")
                cube.action.doAll()
                resolution.append("Y CW")
                posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
            resolution.extend(self.algoTCW(cube))
            resolution.extend(self.algoTACW(cube))
            posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
        
        if nbBonneOrientation == 2:
            diagonal = (orientationCoin[iAvD] == (0,1,0) and orientationCoin[iArG] == (0,1,0)) or \
                        (orientationCoin[iArD] == (0,1,0) and orientationCoin[iAvG] == (0,1,0))
                        
            if diagonal:
                while not orientationCoin[iAvD] == (1,0,0):
                    cube.action.actions.append("Y CWI")
                    cube.action.doAll()
                    resolution.append("Y CW")
                    posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
                actions = ["AV CW"]
                resolution.extend(actions)
                cube.action.actions.extend([action + "I" for action in actions])
                cube.action.doAll()
                resolution.extend(self.algoTCW(cube))
                resolution.extend(self.algoTACW(cube))
                actions = ["AV ACW"]
                resolution.extend(actions)
                cube.action.actions.extend([action + "I" for action in actions])
                cube.action.doAll()
                
            else:
                while not self.testOrientationCoinsBasHomogene(cube):
                    cube.action.actions.append("Y CWI")
                    cube.action.doAll()
                    resolution.append("Y CW")
                    posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
                resolution.extend(self.resolutionOrientationCoinsBasHomogene(cube))

        return resolution
            
    def testOrientationCoinsBasHomogene(self, cube):
        """Test si les coins de droite orienté de façon "Homogene", cad 
        orientable par la fonction associer. Utilisé dans le cadre de 
        l'orentation des coin de la face du bas. (en haut parce que le cube 
        est retourné)"""
        posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
        #Indices des pos
        iAvG = posCoins.index((-1,1,-1))
        iArG = posCoins.index((-1,1,1))
        
        facesHautesVersLaDoite = (orientationCoin[iAvG] == (-1,0,0) and orientationCoin[iArG] == (-1,0,0))
        facesHautesVersAvAr = (orientationCoin[iAvG] == (0,0,-1) and orientationCoin[iArG] == (0,0,1))
        
        return (facesHautesVersLaDoite or facesHautesVersAvAr)
    
    def resolutionOrientationCoinsBasHomogene(self, cube):
        """Oriente correctement les coins en (-1,1,-1) et (-1,1,1) si ils sont
        "Homogene". S'utilise dans le cadre de l'orientation des coins du bas.
        (qui sont en haut car on a retournés le cube)"""
        if not self.testOrientationCoinsBasHomogene(cube):
            raise Exception("Les coins ne sont pas Homogènes.")
        resolution = []
        posCoins, orientationCoin, nbBonneOrientation = self.testOrientationCoinsBas(cube)
        
        #Indices des pos
        iAvG = posCoins.index((-1,1,-1))
        iArG = posCoins.index((-1,1,1))
        
        if (orientationCoin[iAvG] == (0,0,-1) and orientationCoin[iArG] == (0,0,1)):
            resolution.extend(self.algoTCW(cube))
            resolution.extend(self.algoTACW(cube))
        elif (orientationCoin[iAvG] == (-1,0,0) and orientationCoin[iArG] == (-1,0,0)):
            actions = ["Z ACW", "Y CW", "Y CW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
            resolution.extend(self.algoTCW(cube))
            resolution.extend(self.algoTACW(cube))
            actions = ["Y CW", "Y CW", "Z CW"]
            resolution.extend(actions)
            cube.action.actions.extend([action + "I" for action in actions])
            cube.action.doAll()
        
        return resolution
        
    def testOrientationCoinsBas(self, cube):
        """Test l'orientation des coins de la face du bas
        (qui eest en haut parce que le cube est retourné.
        Retourn la liste de la position des coins, celle de leur 
        orientation et le nombre de coin bien orientés."""
        retourOrientation = []
        nbBonneOrientation = 0
        
        retourPos = [(-1,1,-1), (1,1,-1), (1,1,1), (-1,1,1)]
        cubieCentreHaut = cube.getCubieByPos((0,1,0))
        couleurH = cube.cubies[cubieCentreHaut].couleursResolution[0]
        
        for pos in retourPos:
            cubie = cube.getCubieByPos(pos)
            orientation = cube.cubies[cubie].getOrientationFace(couleurH)
            retourOrientation.append(orientation)
            if orientation == (0,1,0):
                nbBonneOrientation += 1
                
        return retourPos, retourOrientation, nbBonneOrientation 