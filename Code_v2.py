# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:31:17 2022
@author: bouti
"""

import numpy as np
import random as rd
import xml.etree.ElementTree as ET

class Grille:
    def __init__(self, path):
        arbreXML = ET.parse(path)
        tronc = arbreXML.getroot()

        nom = tronc.attrib['titre']
        self._couleurs = tronc.attrib['couleurs']
        self._nb_colonnes = int(tronc.attrib['nb_colonnes'])
        self._nb_lignes = int(tronc.attrib['nb_lignes'])

        self._cellules = np.array([[None for j in range(self._nb_colonnes)] for i in range(self._nb_lignes)])

        for i in tronc[0]:
            ligne = int(i.attrib['ligne'])
            colonne = int(i.attrib['colonne'])
            
            try:
                gel = int(i.attrib['niveau_gel'])
            except:
                gel = None
            
            try:
                ortn = i.attrib['orientation']
            except:
                ortn = None
                
            try:
                flux = i.attrib['flux']
            except:
                flux = None            
            
            typ = i.tag

            if typ=='Cellule_Vide':
                cell = CellVide(self, (ligne, colonne), ortn, flux)
                
            else:
                
                cont = i.attrib['contenu']
                if cont in self._couleurs:
                    elem = EltClassique(cont, self, (ligne, colonne))

                elif cont in ['etoile','Etoile']:
                    elem = Etoile(self, (ligne, colonne))
                    
                elif cont in ['avion', 'Avion']:
                    elem = Avion(self, (ligne,colonne))

                elif cont in ['bombe', 'Bombe']:
                    elem = Bombe(self, (ligne, colonne))

                elif cont in ['deflagrateur','Deflagrateur']:
                    elem = Deflagrateur(self, (ligne, colonne))

                elif 'Roquette' in cont:
                    if 'Horizontale' in cont:
                        elem = Roquette('h', self, (ligne, colonne))
                    else:
                        elem = Roquette('v', self, (ligne, colonne))
                    
                else:
                    raise ValueError(("L'élément à la ligne {} et à la colonne {} n'existe pas.").format(ligne, colonne))

                if typ=='Cellule':
                    cell = CellNormale(self, (ligne, colonne), ortn, flux, elem)

                else:
                    cell = CellGelee(self, (ligne, colonne), ortn, flux, elem, gel)

            self._cellules[ligne, colonne] = cell

    def __str__(self):
        return str(np.array([[str(self._cellules[i,j]) for j in range(self._nb_colonnes)] for i in range(self._nb_lignes)]))
    
    def __getitem__(self, coor):
        return str(self._cellules[coor[0], coor[1]])

    def __setitem__(self, coor, nouvelle_valeur):
        self._cellules[coor] = nouvelle_valeur

    def patterns(self):
        M = self._cellules
        n = np.shape(M)[0]
        p = np.shape(M)[1]
        L_pattern = []
        cell = []
        
        # TYPE 8 - XXDXX Ligne
        for i in range(n):
            for j in range(2,p-2):
                cond = not((i,j-2) in cell or (i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i,j+2) in cell)
                if cond:
                    L = [M[i,j+k-2] for k in range(5)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(8, self, (i, j), L[1]))
                        cell.append((i,j-2))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i,j+2))
        
        # TYPE 9 - XXDXX Colonne - NFP
        for i in range(2,n-2):
            for j in range(p):
                cond = not((i-2,j) in cell or (i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i+2,j) in cell)
                if cond:
                    L = [M[i+k-2,j] for k in range(5)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(9, self, (i, j), L[1]))
                        cell.append((i-2,j))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i+2,j)) 
        
        # TYPE 4 - T - F
        for i in range(0,n-2):
            for j in range(1,p-1):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i+1,j) in cell or (i+2,j) in cell)
                if cond:
                    L = [M[i,j-1], M[i,j], M[i,j+1], M[i+1,j], M[i+2,j]]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(4, self, (i, j), L[1]))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i+1,j))
                        cell.append((i+2,j))
                    
        # TYPE 5 - T+90° - F
        for i in range(1,n-1):
            for j in range(0,p-2):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i,j+1) in cell or (i,j+2) in cell)
                if cond:
                    L = [M[i-1,j], M[i,j], M[i+1,j], M[i,j+1], M[i,j+2]]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(5, self, (i, j), L[1]))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i,j+1))
                        cell.append((i,j+2))

        # TYPE 6 - T+180° - F
        for i in range(2,n):
            for j in range(1,p-1):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i-1,j) in cell or (i-2,j) in cell)
                if cond:
                    L = [M[i,j-1], M[i,j], M[i,j+1], M[i-2,j], M[i-1,j]]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(6, self, (i, j), L[1]))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i-1,j))
                        cell.append((i-2,j))
        
        # TYPE 7 - T+270° - F
        for i in range(1,n-1):
            for j in range(2,p):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i,j-1) in cell or (i,j-2) in cell)
                if cond:
                    L = [M[i-1,j], M[i,j], M[i+1,j], M[i,j-2], M[i,j-1]]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(7, self, (i, j), L[1]))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i,j-1))
                        cell.append((i,j-2))
                
        # TYPE 1 - XRXX Ligne
        for i in range(n):
            for j in range(1,p-2):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i,j+2) in cell)
                if cond:
                    L = [M[i,j+k-1] for k in range(4)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(1, self, (i, j), L[1]))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i,j+2))
        
        # TYPE 2 - XRXX Colonne
        for i in range(1,n-2):
            for j in range(p):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i+2,j) in cell)
                if cond:
                    L = [M[i+k-1,j] for k in range(4)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(2, self, (i, j), L[1]))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i+2,j))
        
        # TYPE 3 - Carré 2x2
        for i in range(n-1):
            for j in range(p-1):
                cond = not((i,j) in cell or (i+1,j) in cell or (i,j+1) in cell or (i+1,j+1) in cell)
                if cond:
                    L = [M[i+k,j+l] for k in range(2) for l in range(2)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1])  or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(3, self, (i, j), L[1]))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i,j+1))
                        cell.append((i+1,j+1))
                            
        # TYPE 10 - Match-3 Ligne
        for i in range(n):
            for j in range(1,p-1):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell)
                if cond:
                    L = [M[i,j+k-1] for k in range(3)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(10, self, (i, j), L[1]))
                        cell.append((i,j))
                        cell.append((i,j-1))
                        cell.append((i,j+1))
                        
        
        # TYPE 11 - Match-3 Colonne
        for i in range(1,n-1):
            for j in range(p):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell)
                if cond:
                    L = [M[i+k-1,j] for k in range(3)]
                    c = True
                    for e in L:
                        if str(e) != str(L[1]) or isinstance(e, CellVide):
                            c = False
                    if c:
                        L_pattern.append(Pattern(11, self, (i, j), L[1]))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))


        return L_pattern

    def casser_patterns(self):
        L_pattern = self.patterns()
        for i in L_pattern:
            i.activer()
    
    def map_flux(self):
        M = np.zeros((self._nb_lignes, self._nb_colonnes), dtype=str)
        for i in range(self._nb_lignes):
            for j in range(self._nb_colonnes):
                if self._cellules[i,j]._flux == 'Source':
                    M[i,j] = '●'
                elif self._cellules[i,j]._ortn == 'Haut':
                    M[i,j] = '↑'
                elif self._cellules[i,j]._ortn == 'Bas':
                    M[i,j] = '↓'
                elif self._cellules[i,j]._ortn == 'Gauche':
                    M[i,j] = '←'
                elif self._cellules[i,j]._ortn == 'Droit':
                    M[i,j] = '→'
                elif self._cellules[i,j]._flux == 'Puits':
                    M[i,j] = '○'
                else:
                    M[i,j] = ' '
        return M

class Cellule:
    def __init__(self, grille, coor, ortn, flux):
        self._grille = grille
        self._coor = coor
        self._ortn = ortn
        self._flux = flux

    def remplissage_cellule(self):
        if isinstance(self, CellNormale) or isinstance(self, CellGelee):
            if self._flux == 'Source':
                L = self._grille._couleurs
                coul = rd.choice(L)
                elem = EltClassique(coul, self._grille, self._coor)
                

class CellVide(Cellule):
    def __init__(self, grille, coor, ortn, flux):
        super().__init__(grille, coor, ortn, flux)

    def __str__(self):
        return '  '

class CellNormale(Cellule):
    def __init__(self, grille, coor, ortn, flux, element):
        super().__init__(grille, coor, ortn, flux)
        self._element = element

    def __str__(self): 
        return repr(self._element)

    def detruire(self):
        self._element = None

    def remplacer(self, nouvel_element):
        self._element = nouvel_element

class CellGelee(Cellule):
    def __init__(self, grille, coor, ortn, flux, element, niveau_gel):
        super().__init__(grille, coor, ortn, flux)
        self._element = element
        self._niveau_gel = niveau_gel

    def __str__(self):
        return repr(self._element)

    def detruire(self):
        self._element = None

    def remplacer(self, nouvel_element):
        self._element = nouvel_element

class Element:
    def __init__(self, grille, coor):
        self._grille = grille
        self._coor = coor

class EltClassique(Element):
    def __init__(self, couleur, grille, coor):
        super().__init__(grille, coor)
        self._couleur = couleur

    def __repr__(self):
        if self._couleur in ['vert', 'green']:
            return "💚"
        elif self._couleur in ['jaune', 'yellow']:
            return "💛"
        elif self._couleur in ['rouge', 'red']:
            return "🧡"
        elif self._couleur in ['bleu', 'blue']:
            return "💙"
        elif self._couleur in ['rose', 'magenta']:
            return "💜"
        else:
            return " "

class Bonus(Element):
    def __init__(self, grille, coor):
        super().__init__(grille, coor)

class Etoile(Element):
    def __init__(self, grille, coor):
        super().__init__(grille, coor)

    def __repr__(self):
        return "⭐"

class Avion(Bonus):
    def __init__(self, grille, coor):
        super().__init__(grille, coor)

    def __repr__(self):
        return "✈"

    def activer(self, coor_obj):
        self._grille._cellules[coor_obj[0], coor_obj[1]].detruire()
        self._grille._cellules[self._coor[0], self._coor[1]].detruire()
        if self._coor[0]>=1:
            self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
        if self._coor[0]<=self._grille._nb_lignes-1:
            self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
        if self._coor[1]>=1:
            self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
        if self._coor[1]<=self._grille._nb_colonnes-1:
            self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
        
 class Bombe(Bonus):
    def __init__(self, grille, coor):
        super().__init__(grille, coor)

    def __repr__(self):
        return "💣"

    def activer(self):
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    print('Ca marche')
                    self._grille._cellules[self._coor[0]+i, self._coor[1]+j].detruire()
                except:
                    pass
        try:
            self._grille._cellules[self._coor[0]-2, self._coor[1]].detruire()
        except:
            pass
        try:
            self._grille._cellules[self._coor[0]+2, self._coor[1]].detruire()
        except:
            pass
        try:
            self._grille._cellules[self._coor[0], self._coor[1]-2].detruire()
        except:
            pass
        try:
            self._grille._cellules[self._coor[0], self._coor[1]+2].detruire()
        except:
            pass

class Deflagrateur(Bonus):
    def __init__(self, grille, coor):
        super().__init__(grille, coor)

    def __repr__(self):
        return "🔫"

    def activer(self, elt_type):
        for i in range(self._grille._nb_lignes):
            for j in range(self._grille._nb_colonnes):
                try:
                    if self._grille._cellules[i,j]._element._couleur == elt_type:
                        print('Ca marche ?')
                        self._grille._cellules[i,j].detruire()
                except:
                    print('Ca marche pas')

class Roquette(Bonus):
    def __init__(self, direction, grille, coor):
        super().__init__(grille, coor)
        self._direction = direction

    def __repr__(self):
        return "🚀"

    def activer(self):
        if self._direction == 'h':
            ligne = self._coor[0]
            nb_colonnes = self._grille._nb_colonnes

            for i in range(nb_colonnes):
                print('Ca marche')
                self._grille._cellules[ligne, i].detruire()
                
        elif self._direction == 'v':
            colonne = self._coor[1]
            nb_lignes = self._grille._nb_lignes

            for i in range(nb_lignes):
                print('Ca marche')
                self._grille._cellules[i, colonne].detruire()

class Pattern:
    # TYPES DE PATTERNS: (triés par force)
        # Type 8: XXDXX Ligne
        # Type 9: XXDXX Colonne
        # Type 4: T
        # Type 5: T+90°
        # Type 6: T+180°
        # Type 7: T+270°
        # Type 1: XRXX Ligne
        # Type 2: XRXX Colonne
        # Type 3: Carré 2x2
        # Type 10: Match-3 Ligne
        # Type 11: Match-3 Colonne
        
    def __init__(self, typ, grille, coor, element):
        self._grille = grille
        self._el = element
        self._coor = coor
        self._type = typ
        
    def __repr__(self):
        return "Pattern de type {} ({}) en {}".format(str(self._type), str(self._el), str(self._coor))

    def activer(self):
        if isinstance(self._grille._cellules[self._coor[0], self._coor[1]]._element, EltClassique):
            if self._type == 1:
                self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+2].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Roquette('verticale'))
                
            if self._type == 2:
                self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+2, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Roquette('horizontale'))
            
            if self._type == 3:
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Avion())
            
            if self._type == 4:
                self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+2, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Bombe())
    
            if self._type == 5:
                self._grille._cellules[self._coor[0], self._coor[1]] = Bombe()
                self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+2].detruire()
            
            if self._type == 6:
                self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]-2, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]-2].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Bombe())
            
            if self._type == 7:
                self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]-2].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Bombe())
            
            if self._type == 8:
                self._grille._cellules[self._coor[0], self._coor[1]-2].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+2].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Deflagrateur())
    
            if self._type == 9:
                self._grille._cellules[self._coor[0]-2, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+2, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].remplacer(Deflagrateur())
            
            if self._type == 10:
                self._grille._cellules[self._coor[0], self._coor[1]-1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]+1].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].detruire()
            
            if self._type == 11:
                self._grille._cellules[self._coor[0]-1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0]+1, self._coor[1]].detruire()
                self._grille._cellules[self._coor[0], self._coor[1]].detruire()
        
        else:
            pass # Ne rien faire si le pattern est composé de bonus ou d'étoiles
            
lien1 = "C:/Users/Elève/Downloads/Niveau1 - Reconnaissance de bonus.xml"
lien1_1 = "C:/Users/Elève/Downloads/Niveau1.1 - Activation des bonus.xml"
lien2 = "C:/Users/Elève/Downloads/Niveau2 - Introduction des cellules gelees.xml"
lien3 = "C:/Users/Elève/Downloads/Niveau3 - Introduction des cellules vides.xml"
lien4 = "C:/Users/Elève/Downloads/Niveau4 V1.3 - Carte non convexe + introduction des étoiles.xml"
lien5 = "C:/Users/Elève/Downloads/NIveau5 V1.2 - Flux complexe.xml"
lien6 = "C:/Users/Elève/Downloads/NIveau6 V1.2 - Flux complexe et téléportation.xml"
