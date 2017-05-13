'''
Created on 9 mars 2017

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

Programme inspiré d'un programme dévellopé par Leonel Machava <leonelmachava@gmail.com>
 http://codeNtronix.com 
'''

import sys, math, pygame
from operator import itemgetter

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotationX(self, angle):
        """ Fait pivoter le point autour de l'axe X d'une valeur donnée en degrés. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina #Formules d'addition de trigo.
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotationY(self, angle):
        """ Fait pivoter le point autour de l'axe Y d'une valeur donnée en degrés. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina #Formules d'addition de trigo.
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotationZ(self, angle):
        """ Fait pivoter le point autour de l'axe Z d'une valeur donnée en degrés. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina #Formules d'addition de trigo.
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def projection(self, largeur_ecran, hauteur_ecran, zoom, distance):
        """ Transforme ce point 3D en point 2D (avec la profondeur conservé). """
        factor = zoom / (distance + self.z)
        x = self.x * factor + largeur_ecran / 2
        y = -self.y * factor + hauteur_ecran / 2
        return Point3D(x, y, self.z)
    
    def __eq__(self, point):
        """opérateur d'égalité."""
        x = abs(self.x - point.x) < 0.01
        y = abs(self.y - point.y) < 0.01
        z = abs(self.z - point.z) < 0.01
        return x and y and z

    def dans(self, points):
        """Test si un point est dans une liste de points avec une impressition."""
        for point in points:
        
            x = False
            y = False
            z = False
        
            if abs(self.x - point.x) < 0.01:
                x = True
            if abs(self.y - point.y) < 0.01:
                y = True
            if abs(self.z - point.z) < 0.01:
                z = True
            
            if x and y and z:
                return True

        return False
    
    def copie(self):
        """Retourne  une copie de l'objet."""
        return Point3D(self.x, self.y, self.z)

class Peintre:
    """Objet de tri pour les faces."""
    def __init__(self, LARGEUR_ECRAN = 500, HAUTEUR_ECRAN = 500, ZOOM = 254, DISTANCE = 50, ECART_INTER = 0.01):
        self.LARGEUR_ECRAN = LARGEUR_ECRAN                      # DISTANCE 10
        self.HAUTEUR_ECRAN = HAUTEUR_ECRAN
        self.ZOOM = ZOOM
        self.DISTANCE = DISTANCE
        self.ECART_INTER = ECART_INTER
        self.coin = []
        self.faces = []
    
    def intersection(self, A, B, C, D):
        """Retourne l'intersection des secgments [point1 point2] et [point3 point4] en 2 dimentions"""

        # Segments paralleles
        if A.x == B.x and C.x == D.x: return None
    
        elif (A.x == B.x):
            c = (C.y - D.y)/(C.x - D.x)
            d = C.y - (c*C.x)
            x = A.x
            y = c*x + d
        
        elif (C.x == D.x):
            a = (A.y - B.y)/(A.x - B.x)
            b = A.y - (a*A.x)
            x = C.x
            y = a*x + b
    
        else:
            a = (A.y - B.y)/(A.x - B.x)
            b = A.y - (a*A.x)
            c = (C.y - D.y)/(C.x - D.x)
            d = C.y - (c*C.x)   
                     
            if a == c: 
                return None # Segment parallèles
            elif a == 0:
                y = B.y
                x = (y - d)/c
            elif c == 0:
                y = D.y
                x = (y - b/a)
            else:
                x = (d - b)/(a - c)
                y = a*x + b
    
        pointDansSegment1 =  (min(A.x, B.x) + self.ECART_INTER < x < max(A.x, B.x) - self.ECART_INTER) \
                        and (min(A.y, B.y) + self.ECART_INTER < y < max(A.y, B.y) - self.ECART_INTER)
        pointDansSegment2 =  (min(C.x, D.x) + self.ECART_INTER < x < max(C.x, D.x) - self.ECART_INTER) \
                        and (min(C.y, D.y + self.ECART_INTER) < y < max(C.y, D.y) - self.ECART_INTER)
    
        if pointDansSegment1 and pointDansSegment2:
            return Point3D(x, y, 0)
        else:
            return None
        
    def profondeurIntersection(self, A, B, I):
        """Retourne le point avec sa profondeur"""
    
        x = I.x
        y = I.y
    
        if A.z == B.z:
            z = A.z
            return Point3D(x, y, z)

        a = (A.x - B.x)/(A.z - B.z)
        b = B.x - (a*B.z)
        c = (A.y - B.y)/(A.z - B.z)
        d = B.y - (c*B.z)
    
        # Attention grosse formule!

        denominateur = ((x - self.LARGEUR_ECRAN/2) - a*self.ZOOM)
        if denominateur != 0:
            z = (b*self.ZOOM - (x - self.LARGEUR_ECRAN/2)*self.DISTANCE)/denominateur
            return Point3D(x, y, z)
    
        denominateur = (c*self.ZOOM + y - self.HAUTEUR_ECRAN/2)
        if denominateur != 0:
            z = (-d*self.ZOOM - (y - self.HAUTEUR_ECRAN/2)*self.DISTANCE)/denominateur
            return Point3D(x, y, z)
    
        denominateur = (y - self.HAUTEUR_ECRAN/2 + (c+d)*self.ZOOM)
        if denominateur != 0:
            z = -(y - self.HAUTEUR_ECRAN/2)*self.DISTANCE/denominateur
            return Point3D(x, y, z)
    
        ## Formules qui MARCHENT:
        #z = - (y - HAUTEUR_ECRAN/2)*DISTANCE / (y - HAUTEUR_ECRAN/2 + (c+d)*ZOOM)
        #z = (-d*ZOOM - (y - HAUTEUR_ECRAN/2)*DISTANCE)/(c*ZOOM + y - HAUTEUR_ECRAN/2)
        #z = (b*ZOOM - (x - LARGEUR_ECRAN/2)*DISTANCE)/((x - LARGEUR_ECRAN/2) - a*ZOOM)
    
        ## Formules FAUSSENT z = ((y - HAUTEUR_ECRAN/2)*a/ZOOM + b) / (1- (a/ZOOM)*(y - HAUTEUR_ECRAN/2))
        ##z = ((x - LARGEUR_ECRAN/2)*DISTANCE - b*ZOOM)/(a*ZOOM - x - LARGEUR_ECRAN/2)
        z = 0
        return Point3D(x, y, z)
    
    def tri(self, faces, intersections, segments, points3D, point2D):
        """Trie les faces en fonction des points d'intersection"""
    
        # pointsSegments contient des listes avec en première valeur le point d'intersection
        # en deuxième et troisième les extrèmitès du segment auquel il appartient.
        # Ces listes vont normalement par paire.
        while intersections:
            # Selectionne deux points d'intersections de même position
            intersection1 = intersections[0]
            intersections = intersections[1:]
            segment1 = segments[0]
            segments = segments[1:]
            for intersection2 in intersections:
                if abs(intersection1.x - intersection2.x) < 0.01 and abs(intersection1.y - intersection2.y) < 0.01:
                    segment2 = segments[intersections.index(intersection2)]
                    segments.remove(segment2)
                    intersections.remove(intersection2)
                    break 
            
            # verifie la validite du point
            if intersection1.x - intersection2.x < 0.01 and intersection1.y - intersection2.y < 0.01:

                faces1 = []
                faces2 = []
            
                for face in faces:
                    i = faces.index(face)
                    pointsFaces = [points3D[j] for j in face]
                    if segment1[0].dans(pointsFaces) and \
                    segment1[1].dans(pointsFaces):
                        faces1.append(i)
                    if segment2[0].dans(pointsFaces) and \
                    segment2[1].dans(pointsFaces):
                        faces2.append(i)

                # Nous avons associer deux points d'intersection de profondeur differentes 
                # aux faces qui contiennent le segment
                # Il faut que les faces donc le segment est le plus proche soit avans les 
                # deux autres.
                interTpm = [intersection1, intersection2]
                facesTpm = [faces1, faces2]
                # Le point le plus éloigné en premier, donc les premieres faces a afficher en premier
                if interTpm[0].z > interTpm[1].z:
                    tmp = facesTpm[0]
                    facesTpm[0] = facesTpm[1]
                    facesTpm[1] = tmp
                    # les premieres faces doivent etre avant la limite
                limite = min(facesTpm[0])
                indice1, indice2 = facesTpm[1]
        
                if indice1 > limite and indice2 > limite:
                    faces1Liste = faces[:limite]
                    faces2Liste = faces[limite:]
                    faces1Liste.append(faces[min(indice1, indice2)])
                    faces1Liste.append(faces[max(indice1, indice2)])
                    faces2Liste.remove(faces[indice1])
                    faces2Liste.remove(faces[indice2])
                    faces = faces1Liste + faces2Liste
            
                elif indice1 > limite:
                    faces1Liste = faces[:limite]
                    faces2Liste = faces[limite:]
                    faces1Liste.append(faces[indice1])
                    faces2Liste.remove(faces[indice1])
                    faces = faces1Liste + faces2Liste
        
                elif indice2 > limite:
                    faces1Liste = faces[:limite]
                    faces2Liste = faces[limite:]
                    faces1Liste.append(faces[indice2])
                    faces2Liste.remove(faces[indice2])
                    faces = faces1Liste + faces2Liste
            
        return faces

    def peintre1(self, faces, points2D):
        """Algorithme du peintre traditionnel."""
        moy_z = []
        i = 0
        for f in faces:
            z = (points2D[f[0]].z + points2D[f[1]].z + points2D[f[2]].z + points2D[f[3]].z) / 4.0
            moy_z.append([i,z])
            i = i + 1
        
        nouvellesFaces = []
        # Trie lessurfaces en utlisant l'algorithme du peintre
        # Les faces les plus éloignées sont tracées avant les plus proches.
        for tmp in sorted(moy_z,key=itemgetter(1),reverse=True):
            indiceFace = tmp[0]
            nouvellesFaces.append(faces[indiceFace])

        return nouvellesFaces
    
    def peintre2(self):
        """Retourne une liste de surface clasés selon l'algorythme du peintre, ainsi que leur couleur"""
        
        points3D = self.coins
        points2D = [i.projection(self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN, self.ZOOM, self.DISTANCE) for i in self.coins]
        faces = self.faces
        intersections = []
        segments = []

        for face1 in self.faces:
            #Test l'intersection de tous les point de chaque face
            for face2 in self.faces:
                for j in [-1, 0, 1, 2]: 
                    for i in [-1, 0, 1, 2]:
                        
                        A3D = points3D[face1[j]]
                        B3D = points3D[face1[j+1]]
                        C3D = points3D[face2[i]]
                        D3D = points3D[face2[i+1]]
                        
                        A = points2D[face1[j]]
                        B = points2D[face1[j+1]]
                        C = points2D[face2[i]]
                        D = points2D[face2[i+1]]
                        
                        inter = self.intersection(A, B, C, D)
                        if inter:
                            intersections.append(self.profondeurIntersection(A3D, B3D, inter))
                            segments.append([A3D, B3D])
                            intersections.append(self.profondeurIntersection(C3D, D3D, inter))
                            segments.append([C3D, D3D])
        
        faces = self.peintre1(faces, points2D)
        faces = self.tri(faces, intersections, segments, points3D, points2D)      
        return faces


class Cubie3D(Peintre):
    """Class définissant un cube en 3D"""

    def __init__(self, pos):
        """Définit le cube de centre pos et de coté 2"""
        
        Peintre.__init__(self)
        
        self.centre = Point3D(pos[0], pos[1], pos[2])
                
        self.coins = [
            Point3D(pos[0]-2,pos[1]+2,pos[2]+2),   #    droit    haut    arrière
            Point3D(pos[0]+2,pos[1]+2,pos[2]+2),   #    gauche   haut    arrière
            Point3D(pos[0]-2,pos[1]+2,pos[2]-2),   #    droit    haut    avant
            Point3D(pos[0]+2,pos[1]+2,pos[2]-2),   #    gauche   haut    avant
            Point3D(pos[0]-2,pos[1]-2,pos[2]+2),   #    droit    bas     arrière
            Point3D(pos[0]+2,pos[1]-2,pos[2]+2),   #    gauche   bas     arrière
            Point3D(pos[0]-2,pos[1]-2,pos[2]-2),   #    droit    bas     avant
            Point3D(pos[0]+2,pos[1]-2,pos[2]-2)]   #    gauche   bas     avant
        #Liste des faces, les valeurs sont les indices du point correspondant dans la liste coins.
        self.faces  = [
            (0,1,3,2),  # Haut
            (4,5,7,6),  # Bas
            (0,2,6,4),  # Droite
            (1,3,7,5),  # Gauche
            (0,1,5,4),  # Arrière
            (2,3,7,6)]  # Avant
        #Liste des couleurs, leur indices sont les mêmes que ceux de la faces associer.
        self.couleurs = [
            (0,0,0),  #(255,0,0),      # Haut
            (0,0,0),  #(255,70,0),     # Bas
            (0,0,0),  #(255,255,0),    # Gauche
            (0,0,0),  #(255,255,255),  # Droite
            (0,0,0),  #(0,255,0),      # Arrière
            (0,0,0)]  #(0,0,255)]      # Avant
        
        self.couleursResolution = []
    
    def getMinZ(self):
        """Retourne la profondeur du point le plus proche."""
        z = self.coins[0].z
        for pt in self.coins:
            if pt.z < z:
                z = pt.z
        return z

    minZ = property(fget = getMinZ)

    def rotationX(self, angle):
        """ Fait pivoter le cube autour de l'axe X d'une valeur donnée en degrés. """
        newCoins = []
        for point in self.coins:
            newCoins.append(point.rotationX(angle))
        newCube = self.copie()
        newCube.coins = newCoins
        newCube.centre = self.centre.rotationX(angle)
        return newCube

    def rotationY(self, angle):
        """ Fait pivoter le cube autour de l'axe Y d'une valeur donnée en degrés. """
        newCoins = []
        for point in self.coins:
            newCoins.append(point.rotationY(angle))
        newCube = self.copie()
        newCube.coins = newCoins
        newCube.coins = newCoins
        newCube.centre = self.centre.rotationY(angle)
        return newCube
    
    def rotationZ(self, angle):
        """ Fait pivoter le cube autour de l'axe Z d'une valeur donnée en degrés. """
        newCoins = []
        for point in self.coins:
            newCoins.append(point.rotationZ(angle))
        newCube = self.copie()
        newCube.coins = newCoins
        newCube.centre = self.centre.rotationZ(angle)
        return newCube
    
    def getOrientationFace(self, couleur):
        """Retourn l'orientation de la face de la couleur donnée.
        Elle est donné sous la forme x, y, z, seul l'axe perpendiculaire 
        à la face est différent ce 0, et le signe son de quel côté du cube il ce trouve."""
        indiceFace = self.couleurs.index(couleur)
        pointsFace = [(self.coins[i].x, self.coins[i].y, self.coins[i].z) for i in self.faces[indiceFace]]
        pointsFaceOposee = [(self.coins[i].x, self.coins[i].y, self.coins[i].z) 
                            for i in range(len(self.coins)) if i not in self.faces[indiceFace]]
        
        orientation = [0, 0, 0]
        
        for i in [0, 1, 2]:
            #on compart les coordonnées du premier point des deux faces, pour x, y puis z
            if pointsFace[0][i] > pointsFaceOposee[0][i]: orientation[i] = 1
            elif pointsFace[0][i] < pointsFaceOposee[0][i]: orientation[i] = -1

        for point in pointsFace:
            for i in [0, 1, 2]:
                if abs(point[i] - pointsFace[0][i]) > 0.01:
                #if point[i] != pointsFace[0][i]:
                    orientation[i] = 0
            # pour donner l'axe de la face, 
            #on compart les coordonnées e x,y et z entre les points de la place.
        if orientation == [0, 0, 0]:
            raise Exception("Cette face ne semble pas avoir d'orientation, what?")
        return tuple(orientation)
        

    def affichage(self, screen):
        """Affiche le cube sur l'écran screen en utilisant l'algorithme du peintre"""
        
        t = []
        for coin in self.coins:
            p = coin.projection(self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN, self.ZOOM, self.DISTANCE)
            # Place le point dans une liste de coins transformés
            t.append(p)

        # Trace la surface en utlisant l'algorithme du peintre
        # Les faces les plus éloignées sont tracées avant les plus proches.
        faces = self.peintre2()
        for f in faces[-3:]:
            pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                        (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                        (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                        (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
            
            pygame.draw.polygon(screen,(0,0,0),pointlist, 3) 
            #Pour que les faces caches les traits
            #en arrière, ils faut les affichers après les arrètes
            pygame.draw.polygon(screen,self.couleurs[self.faces.index(f)],pointlist)
            #pygame.display.flip()
            #pygame.time.wait(100)
        
    def copie(self):
        """Retourne une copie de l'objet."""
        newCubie = Cubie3D((0,0,0))
        newCubie.centre = self.centre
        newCubie.coins = self.coins
        newCubie.faces = self.faces
        newCubie.couleurs = self.couleurs
        newCubie.couleursResolution = self.couleursResolution
        return newCubie
        

if __name__ == "__main__":
    
    ###nb_image = 0 #######
    
    pygame.init()
          
    cubes = [Cubie3D((-2,-2,-2))]
    angle = 5
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Rubick's Cube")   
    
    rot = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if rot:
                        rot = False
                    else:
                        rot = True
                if event.key == pygame.K_LEFT:
                    angle = 5
                if event.key == pygame.K_RIGHT:
                    angle = -5
        screen.fill((255,255,255))
        for cube in cubes:
            cube.affichage(screen)
        #if nb_image == 40:
        #    pygame.quit()
        #    sys.exit()
        #pygame.image.save(screen,"./img/" + str(nb_image)+".png")
        #nb_image+=1################################################
        pygame.display.flip()
        pygame.time.wait(100)
        if rot:
            for i, cube in enumerate(cubes):
                cubes[i] = cube.rotationZ(angle)#.rotationY(angle).rotationX(angle)
