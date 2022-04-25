# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 18:44:00 2022

@author: bouti
"""
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
        return "✈️"

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
    
    # def detruire(self, colonne, ligne):
    #     i = ligne
    #     while i>=1:
    #         self.__data[i, colonne] = self.__data[i-1, colonne]
    #         i -= 1
    #     self.__data[0, colonne] = retourner_random(self.__proba_r, self.__proba_b, self.__proba_a, self.__proba_d, self.__proba_e)
        
def retourner_random(proba_r, proba_b, proba_a, proba_d, proba_e):
    if proba_r>0 and proba_b>0 and proba_a>0 and proba_d>0 and proba_e>0 and proba_r+proba_b+proba_a+proba_d+proba_e<1:
        pop = [Roquette(), Bombe(), Avion(), Deflagrateur(), Etoile(), None]
        weight = [proba_r, proba_b, proba_a, proba_d, proba_e, 1-(proba_r+proba_b+proba_a+proba_d+proba_e)]
        rand = rd.choices(pop, weight, k=1)[0]
        if rand == None:
            couleur = rd.choice(["Rouge", "Vert", "Jaune", "Violet", "Bleu"])
            return Classique(couleur)
        else:
            return rand
    
    else:
        raise ValueError("Les probabilités d'apparitions des bonus ne sont pas valides")
