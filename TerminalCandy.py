import numpy as np
import random as rd

class Element():
    def __init__(self, grille, ligne, colonne):
        self.__grille = grille
        self.__ligne = ligne
        self.__colonne = colonne
    
    def __repr__(self):
        return "Element"
    
    def read_coordonnees(self):
        return (self.__ligne, self.__colonne)
    
    def write_coordonnees(self, nv_ligne, nv_colonne):
        self.__ligne = nv_ligne
        self.__colonne = nv_colonne

class Classique(Element):
    def __init__(self, couleur, grille, ligne, colonne):
        super().__init__(grille, ligne, colonne)
        couleurs = ["Rouge", "Vert", "Jaune", "Violet", "Bleu"]
        if couleur in couleurs:
            self.__couleur = couleur
        else:
            raise ValueError("Cette couleur n'existe pas")
    
    def __repr__(self):
        if self.__couleur == "Rouge":
            return "🔴"
        elif self.__couleur == "Vert":
            return "🟢"
        elif self.__couleur == "Jaune":
            return "🟡"
        elif self.__couleur == "Violet":
            return "🟣"
        else:
            return "🔵"
            
class Roquette(Element):
    def __init__(self, grille, ligne, colonne):
        super().__init__(grille, ligne, colonne)
    
    def __repr__(self):
        return "🚀"

class Bombe(Element):
    def __init__(self, grille, ligne, colonne):
        super().__init__(grille, ligne, colonne)
    
    def __repr__(self):
        return "💣"
    
class Avion(Element):
    def __init__(self, grille, ligne, colonne):
        super().__init__(grille, ligne, colonne)
    
    def __repr__(self):
        return "✈"

class Deflagrateur(Element):
    def __init__(self, grille, ligne, colonne):
        super().__init__(grille, ligne, colonne)
    
    def __repr__(self):
        return "🔫"

class Etoile(Element):
    def __init__(self, grille, ligne, colonne):
        super().__init__(grille, ligne, colonne)
    
    def __repr__(self):
        return "⭐"

class Grille():
    def __init__(self, taille, probas):
        self.__taille = taille
        self.__probas = probas
        self.__data = np.array([[None for i in range(self.__taille)] for i in range(self.__taille)])
        
        for i in range(self.__taille):
                for j in range(self.__taille):
                    self.__data[i,j] = retourner_random(self.__probas, self, i, j)
                    
    def data(self):
        return self.__data
    
    def detruire(self, ligne, colonne):
        i = ligne
        while i>=1:
            self.__data[i, colonne] = self.__data[i-1, colonne]
            self.__data[i, colonne].write_coordonnees(i, colonne)
            i += (-1)
        self.__data[0, colonne] = retourner_random(self.__probas, self, 0, colonne)

    def remplacer(self, ligne, colonne, nouvel_element):
        self.__data[ligne, colonne] = nouvel_element

    def patterns(self):
        ## PROBLEME ICI !!!
        M = self.__data
        n = np.shape(self.__data)[0]
        L_pattern = []
        cell = []
        
        # TYPE 8 - XXDXX Ligne
        for i in range(n):
            for j in range(2,n-2):
                cond = not((i,j-2) in cell or (i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i,j+2) in cell)
                if cond:
                    L = [M[i,j+k-2] for k in range(5)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(8, slef, i, j))
                        cell.append((i,j-2))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i,j+2))
        
        # TYPE 9 - XXDXX Colonne - NFP
        for i in range(2,n-2):
            for j in range(n):
                cond = not((i-2,j) in cell or (i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i+2,j) in cell)
                if cond:
                    L = [M[i+k-2,j] for k in range(5)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(9, self, i, j))
                        cell.append((i-2,j))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i+2,j))
        
        # TYPE 4 - T - F
        for i in range(0,n-2):
            for j in range(1,n-1):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i+1,j) in cell or (i+2,j) in cell)
                if cond:
                    L = [M[i,j-1], M[i,j], M[i,j+1], M[i+1,j], M[i+2,j]]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(4, self, i, j))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i+1,j))
                        cell.append((i+2,j))
                    
        # TYPE 5 - T+90° - F
        for i in range(1,n-1):
            for j in range(0,n-2):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i,j+1) in cell or (i,j+2) in cell)
                if cond:
                    L = [M[i-1,j], M[i,j], M[i+1,j], M[i,j+1], M[i,j+2]]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(5, self, i, j))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i,j+1))
                        cell.append((i,j+2))

        # TYPE 6 - T+180° - F
        for i in range(2,n):
            for j in range(1,n-1):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i-1,j) in cell or (i-2,j) in cell)
                if cond:
                    L = [M[i,j-1], M[i,j], M[i,j+1], M[i-2,j], M[i-1,j]]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(6, self, i, j))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i-1,j))
                        cell.append((i-2,j))
        
        # TYPE 7 - T+270° - F
        for i in range(1,n-1):
            for j in range(2,n):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i,j-1) in cell or (i,j-2) in cell)
                if cond:
                    L = [M[i-1,j], M[i,j], M[i+1,j], M[i,j-2], M[i,j-1]]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(7, self, i, j))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i,j-1))
                        cell.append((i,j-2))
                
        # TYPE 1 - XRXX Ligne - NFP
        for i in range(n):
            for j in range(1,n-2):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell or (i,j+2) in cell)
                if cond:
                    L = [M[i,j+k-1] for k in range(4)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(1, self, i, j))
                        cell.append((i,j-1))
                        cell.append((i,j))
                        cell.append((i,j+1))
                        cell.append((i,j+2))
        
        # TYPE 2 - XRXX Colonne - NFP
        for i in range(1,n-2):
            for j in range(n):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell or (i+2,j) in cell)
                if cond:
                    L = [M[i+k-1,j] for k in range(4)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(2, self, i, j))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i+2,j))
        
        # TYPE 3 - Carré 2x2 - NFP
        for i in range(n-1):
            for j in range(n-1):
                cond = not((i,j) in cell or (i+1,j) in cell or (i,j+1) in cell or (i+1,j+1) in cell)
                if cond:
                    L = [M[i+k,j+l] for k in range(2) for l in range(2)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(3, self, i, j))
                        cell.append((i,j))
                        cell.append((i+1,j))
                        cell.append((i,j+1))
                        cell.append((i+1,j+1))
                            
        # TYPE 10 - Match-3 Ligne - NFP
        for i in range(n):
            for j in range(1,n-1):
                cond = not((i,j-1) in cell or (i,j) in cell or (i,j+1) in cell)
                if cond:
                    L = [M[i,j+k-1] for k in range(3)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(10, self, i, j))
                        cell.append((i,j))
                        cell.append((i,j-1))
                        cell.append((i,j+1))
                        
        
        # TYPE 11 - Match-3 Colonne - NFP
        for i in range(1,n-1):
            for j in range(n):
                cond = not((i-1,j) in cell or (i,j) in cell or (i+1,j) in cell)
                if cond:
                    L = [M[i+k-1,j] for k in range(3)]
                    c = True
                    for e in L:
                        if repr(e) != repr(L[1]):
                            c = False
                    if c:
                        L_pattern.append(Pattern(11, self, i, j))
                        cell.append((i-1,j))
                        cell.append((i,j))
                        cell.append((i+1,j))


        return L_pattern
                
class Pattern():
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
        
    def __init__(self, pattern_type, grille, ligne, colonne):
        self.__type = pattern_type
        self.__grille = grille
        self.__ligne = ligne
        self.__colonne = colonne

    def __repr__(self):
        return "Pattern de type {} en {}".format(str(self.__type), str((self.__ligne, self.__colonne)))
    
    def activer(self):
        if self.__type == 1:
            for i in range(4):
                self.__grille.detruire(self.__ligne+2, self.__colonne)
            self.__grille.remplacer(self.__ligne, self.__colonne, Roquette(self.__grille, self.__ligne, self.__colonne))
        
        if self.__type == 2:
            for i in range(-1,3):
                self._grille.detruire(self.__ligne, self.__colonne+i)
            self.__grille.remplacer(self.__ligne, self.__colonne, Roquette(self.__ligne, self.__colonne))
        
        if self.__type == 3:
            for i in range(2):
                for j in range(2):
                    self.__grille.detruire(self.__ligne+1, self.__colonne+j)
            self.__grille.remplacer(self.__ligne, self.__colonne, Avion(self.__grille, self.__ligne, self.__colonne))            
        
        if self.__type == 4:
            for i in range(3):
                self.__grille.detruire(self.__ligne+2, self.__colonne)
            self.__grille.detruire(self.__ligne, self.__colonne-1)
            self.__grille.detruire(self.__ligne, self.__colonne+1)
            self.__grille.remplacer(self.__ligne, self.__colonne, Bombe(self.__grille, self.__ligne, self.__colonne))
        
        if self.__type == 5:
            for i in range(3):
                self.__grille.detruire(self.__ligne+1, self.__colonne)
            self.__grille.detruire(self.__ligne, self.__colonne+1)
            self.__grille.detruire(self.__ligne, self.__colonne+2)
            self.__grille.remplacer(self.__ligne, self.__colonne, Bombe(self.__grille, self.__ligne, self.__colonne))
        
        if self.__type == 6:
            for i in range(3):
                self.__grille.detruire(self.__ligne, self.__colonne)
            self.__grille.detruire(self.__ligne, self.__colonne-1)
            self.__grille.detruire(self.__ligne, self.__colonne+1)
            self.__grille.remplacer(self.__ligne, self.__colonne, Bombe(self.__grille, self.__ligne, self.__colonne))
        
        if self.__type == 7:
            for i in range(3):
                self.__grille.detruire(self.__ligne+1, self.__colonne)
            self.__grille.detruire(self.__ligne, self.__colonne+1)
            self.__grille.detruire(self.__ligne, self.__colonne+2)
            self.__grille.remplacer(self.__ligne, self.__colonne, Bombe(self.__grille, self.__ligne, self.__colonne))
        
        if self.__type == 8:
            for i in range(5):
                self.__grille.detruire(self.__ligne+2, self.__colonne)
            self.__grille.remplacer(self.__ligne, self.__colonne, Deflagrateur(self.__grille, self.__ligne, self.__colonne))
        
        if self.__type == 9:
            for i in range(-2,3):
                self._grille.detruire(self.__ligne, self.__colonne+i)
            self.__grille.remplacer(self.__ligne, self.__colonne, Deflagrateur(self.__ligne, self.__colonne))
            
        
        if self.__type == 10:
            pass
        
        if self.__type == 11:
            pass

def retourner_random(probas, grille, ligne, colonne):
    if probas[0]>0 and probas[1]>0 and probas[2]>0 and probas[3]>0 and probas[4]>0 and probas[0]+probas[1]+probas[2]+probas[3]+probas[4]<1:
        pop = [Roquette(grille, ligne, colonne), Bombe(grille, ligne, colonne), Avion(grille, ligne, colonne), Deflagrateur(grille, ligne, colonne), Etoile(grille, ligne, colonne), None]
        weight = [probas[0],probas[1],probas[2],probas[3],probas[4], 1-(probas[0]+probas[1]+probas[2]+probas[3]+probas[4])]
        rand = rd.choices(pop, weight, k=1)[0]
        if rand == None:
            couleur = rd.choice(["Rouge", "Vert", "Jaune", "Bleu", "Violet"])
            return Classique(couleur, grille, ligne, colonne)
        else:
            return rand
    
    else:
        raise ValueError("Les probabilités d'apparitions des bonus ne sont pas valides")

probas = [0.01, 0.01, 0.01, 0.01, 0.01]
G = Grille(10, probas)
