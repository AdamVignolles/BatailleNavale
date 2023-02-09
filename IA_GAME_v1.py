# Programmé par Adam Vignolles

import socket
import threading
import json
import random


#fonction du jeu contre l'ia
def tour(grilles, current_player):
    """Tour of the game

    La methode permet de faire le tour du jeu

    Args:
        grilles (type:dict) : grilles du jeu
        current_player (type:str) : joueur courant

    Returns:
        tir (type:int) : case tirer
    """
    if current_player == "humain":
        print("tour: HUMAIN")
        print("bateaux:", grilles["humain"]["grille_bateau"])
        print("tir:", grilles["humain"]["grille_tir"])
        tir = int(input("case n° tir :"))
        grilles["humain"]["grille_tir"][int(tir)] = "t"
        print("tir", grilles["humain"]["grille_tir"])
        return tir
    else:
        print("tour: IA")
        print("bateaux:", grilles["ia"]["grille_bateau"])
        print("tir:", grilles["ia"]["grille_tir"])
        tir = random.randint(0, 99)
        grilles["ia"]["grille_tir"][int(tir)] = "t"
        print("tir", grilles["ia"]["grille_tir"])
        return tir

def placer_bateaux(grille):
    # paterne de bateau car pas ma partie
    # bateau de 2 cases
    grille[0] = "b"
    grille[1] = "b"
    # bateau de 3 cases
    grille[3] = "b"
    grille[4] = "b"
    grille[5] = "b"
    # bateau de 4 cases
    grille[11] = "b"
    grille[12] = "b"
    grille[13] = "b"
    grille[14] = "b"
    # bateau de 5 cases
    grille[21] = "b"
    grille[22] = "b"
    grille[23] = "b"
    grille[24] = "b"
    grille[25] = "b"
    return grille


def placer_bateaux_ia(grille_bateau_ia):
    """Placer les bateaux de l'ia

    La methode permet de placer les bateaux de l'ia

    Args:
        grille_bateau_ia (type:list) : grille de bateau de l'ia

    Returns:
        grille_bateau_ia (type:list) : grille de bateau de l'ia
    """
    # placer les bateaux de l'ia
    bateaux = [2, 3, 3, 4, 5]
    for j in bateaux:
        sens = random.randint(0, 1)
        if sens == 0:
            # horizontal
            position = random.randint(0, 99)
            #verifier si il y a deja un bateau a cette position en verifiant si tout les cases sont vide
            while "b" in grille_bateau_ia[position:position + j] and position % 10 + j <= 10 and position + j * 10 <= 99:
                position = random.randint(0, 99)
            
            #verifier si le bateau ne sort pas de la grille
            if position % 10 + j <= 10:
                for k in range(0, j):
                    grille_bateau_ia[position + k] = "b"
            # si le bateau sort de la grille, on le place a l'envers
            else:
                for k in range(0, j):
                    grille_bateau_ia[position - k] = "b"
        else:
            # vertical
            position = random.randint(0, 99)
            #verifier si il y a deja un bateau a cette position en verifiant si tout les cases sont vide
            while "b" in grille_bateau_ia[position:position + j] and position % 10 + j <= 10 and position + j * 10 <= 99:
                position = random.randint(0, 99)
            # verifier si le bateau ne sort pas de la grille
            if position + j * 10 <= 99:
                for k in range(0, j):
                    grille_bateau_ia[position + k * 10] = "b"
            # si le bateau sort de la grille, on le place a l'envers
            else:
                for k in range(0, j):
                    grille_bateau_ia[position - k * 10] = "b"
    return grille_bateau_ia


def change_current_player(current_player):
    """Changer de joueur

    La methode permet de changer de joueur

    Args:
        current_player (type:str) : joueur courant

    Returns:
        current_player (type:str) : joueur courant
    """
    # changer de joueur
    if current_player == "humain":
        current_player = "ia"
    else:
        current_player = "humain"
    return current_player

def formater_grille(grille):
    # formater la grille pour l'affichage optimalement
    grille_formatee = ""
    for i in range(0, 10):
        grille_formatee += " ".join(grille[i * 10:i * 10 + 10]) + "\n"
    return grille_formatee

def affiche_les_grilles(grilles):
    print("grille joueur 1")
    print("bateaux:\n", formater_grille(grilles["humain"]["grille_bateau"]))
    print("tir:\n", formater_grille(grilles["humain"]["grille_tir"]))
    print("grille joueur 2")
    print("bateaux:\n", formater_grille(grilles["ia"]["grille_bateau"]))
    print("tir:\n", formater_grille(grilles["ia"]["grille_tir"]))

def check_touche(grilles, current_player, tir):
    """Verifier si le bateau est touché

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles de bateaux et de tir
        current_player (type:str) : joueur courant
        tir (type:int) : position du tir
    """
    current_player = change_current_player(current_player) # pour verifier si le bateau est touché par l'adversaire
    if grilles[current_player]["grille_bateau"][tir] == "b":
        print("bateau touché")
        grilles[current_player]["grille_bateau"][tir] = "t"
    else:
        print("bateau raté")
        grilles[current_player]["grille_bateau"][tir] = "O"

def check_win(grilles):
    """Verifier si le jeu est fini

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles de bateaux et de tir

    Returns:
        bool: True si le jeu est fini, False sinon
    """
    if grilles["humain"]["grille_bateau"].count("b") == 0:
        print("l'IA a gagné")
        return True
    if grilles["ia"]["grille_bateau"].count("b") == 0:
        print("Vous avez gagné")
        return True
    return False


def boucle_jeu(grilles, current_player):
    """Boucle de jeu

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles de bateaux et de tir
        current_player (type:str) : joueur courant
    """

    while True:
        # faire le tour
        tir = tour(grilles, current_player)

        # afficher les grilles
        affiche_les_grilles(grilles)

        # vérifier si le joueur a touché un bateau
        check_touche(grilles, current_player, tir)

        # vérifier si le jeu est fini
        if check_win(grilles):
            break

        # changer de joueur
        current_player = change_current_player(current_player)




def ia_game():
    """Jeu contre l'IA"""
    grilles = {
        "humain": {
            "grille_bateau": [""]*100,
            "grille_tir": [""]*100
        },
        "ia": {
            "grille_bateau": [""]*100,
            "grille_tir": [""]*100
        }
    }
    current_player = "humain"

    # placer les bateaux de l'ia
    grilles["ia"]["grille_bateau"] = placer_bateaux_ia(grilles["ia"]["grille_bateau"])

    # placer les bateaux du joueur
    grilles["humain"]["grille_bateau"] = placer_bateaux(grilles["humain"]["grille_bateau"])

    # boucle de jeu
    boucle_jeu(grilles, current_player)

if __name__ == "__main__":
    ia_game()

