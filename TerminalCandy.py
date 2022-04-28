# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#  /$$   /$$  /$$                                              /$$   /$$  /$$ #
# | $$  | $$ |__/                                             | $$  | $$ | $$ #
# | $$  | $$  /$$   /$$$$$$    /$$$$$$   /$$   /$$   /$$$$$$$ | $$  | $$ | $$ #
# | $$$$$$$$ | $$  |____  $$  /$$__  $$ | $$  | $$  /$$_____/ | $$$$$$$$ | $$ #
# | $$__  $$ | $$   /$$$$$$$ | $$  \ $$ | $$  | $$ |  $$$$$$  |_____  $$ |__/ #
# | $$  | $$ | $$  /$$__  $$ | $$  | $$ | $$  | $$  \____  $$       | $$      #
# | $$  | $$ | $$ |  $$$$$$$ | $$$$$$$/ |  $$$$$$/  /$$$$$$$/       | $$  /$$ #
# |__/  |__/ |__/  \_______/ | $$____/   \______/  |_______/        |__/ |__/ #
#                            | $$                                             #
#                            | $$                                             #
#                            |__/                                             #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import random as rd

class Element():
    def __init__(self):
        pass
    
    def __repr__(self):
        return "Element"

class Classique(Element):
    def __init__(self, couleur):
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
    def __init__(self):
        pass
    
    def __repr__(self):
        return "🚀"

class Bombe(Element):
    def __init__(self):
        pass
    
    def __repr__(self):
        return "💣"
    
class Avion(Element):
    def __init__(self):
        pass
    
    def __repr__(self):
        return "✈"

class Deflagrateur(Element):
    def __init__(self):
        pass
    
    def __repr__(self):
        return "🔫"

class Etoile(Element):
    def __init__(self):
        pass
    
    def __repr__(self):
        return "⭐"

class Grille():
    def __init__(self, taille, proba_r, proba_b, proba_a, proba_d, proba_e):
        self.__taille = taille
        self.__proba_r = proba_r
        self.__proba_b = proba_b
        self.__proba_a = proba_a
        self.__proba_d = proba_d
        self.__proba_e = proba_e
        self.__data = np.array([[None for i in range(self.__taille)] for i in range(self.__taille)])
        
        for i in range(self.__taille):
                for j in range(self.__taille):
                    self.__data[i,j] = retourner_random(proba_r, proba_b, proba_a, proba_d, proba_e)
                    
    def data(self):
        return self.__data
    
    def detruire(self, colonne, ligne):
        i = ligne
        while i>=1:
            self.__data[i, colonne] = self.__data[i-1, colonne]
            i += (-1)
        self.__data[0, colonne] = retourner_random(self.__proba_r, self.__proba_b, self.__proba_a, self.__proba_d, self.__proba_e)
    

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
                        L_pattern.append(Pattern(8, (i,j)))
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
                        L_pattern.append(Pattern(9, (i,j)))
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
                        L_pattern.append(Pattern(4, (i,j)))
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
                        L_pattern.append(Pattern(5, (i,j)))
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
                        L_pattern.append(Pattern(6, (i,j)))
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
                        L_pattern.append(Pattern(7, (i,j)))
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
                        L_pattern.append(Pattern(1, (i,j)))
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
                        L_pattern.append(Pattern(2, (i,j)))
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
                        L_pattern.append(Pattern(3, (i,j)))
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
                        L_pattern.append(Pattern(10, (i,j)))
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
                        L_pattern.append(Pattern(11, (i,j)))
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
        
    def __init__(self, pattern_type, loc_boost):
        self.__type = pattern_type
        self.__loc_boost = loc_boost

    def __repr__(self):
        return "Pattern de type {} en {}".format(str(self.__type), str(self.__loc_boost))

def retourner_random(proba_r, proba_b, proba_a, proba_d, proba_e):
    if proba_r>0 and proba_b>0 and proba_a>0 and proba_d>0 and proba_e>0 and proba_r+proba_b+proba_a+proba_d+proba_e<1:
        pop = [Roquette(), Bombe(), Avion(), Deflagrateur(), Etoile(), None]
        weight = [proba_r, proba_b, proba_a, proba_d, proba_e, 1-(proba_r+proba_b+proba_a+proba_d+proba_e)]
        rand = rd.choices(pop, weight, k=1)[0]
        if rand == None:
            couleur = rd.choice(["Rouge", "Vert", "Jaune"])
            return Classique(couleur)
        else:
            return rand
    
    else:
        raise ValueError("Les probabilités d'apparitions des bonus ne sont pas valides")

G = Grille(10, 0.01, 0.01, 0.01, 0.01, 0.01)
