# Programmé par Adam Vignolles

import socket
import threading
import json
import random
import partie_graphique as pg

def genere_grille_bateau(grilles, joueur):
    """Genere la grille de bateau

    La methode genere la grille de bateau

    Args:
        grilles (type:dict) : grilles du jeu
        joueur (type:str) : joueur courant

    Returns:
        grille_bateau (type:list) : grille de bateau
    """
    bateaux = [2, 3, 4, 5]
    grille_bateau = grilles[joueur]['grille_bateau']
    for j in bateaux:
        sens = random.randint(0, 1)
        if sens == 0:
            # horizontal
            position = random.randint(0, 99)
            #verifier si il y a deja un bateau a cette position en verifiant si tout les cases sont vide
            while "b" in grille_bateau[position:position + j] and position % 10 + j <= 10 and position + j * 10 <= 99:
                position = random.randint(0, 99)
            
            #verifier si le bateau ne sort pas de la grille
            if position % 10 + j <= 10:
                for k in range(0, j):
                    grille_bateau[position + k] = "b"
            # si le bateau sort de la grille, on le place a l'envers
            else:
                for k in range(0, j):
                    grille_bateau[position - k] = "b"
        else:
            # vertical
            position = random.randint(0, 99)
            #verifier si il y a deja un bateau a cette position en verifiant si tout les cases sont vide
            while "b" in grille_bateau[position:position + j] and position % 10 + j <= 10 and position + j * 10 <= 99:
                position = random.randint(0, 99)
            # verifier si le bateau ne sort pas de la grille
            if position + j * 10 <= 99:
                for k in range(0, j):
                    grille_bateau[position + k * 10] = "b"
            # si le bateau sort de la grille, on le place a l'envers
            else:
                for k in range(0, j):
                    grille_bateau[position - k * 10] = "b"
    return grille_bateau

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

def affiche_grilles(grilles, joueur, current_player):
    """Afficher les grilles

    La methode permet d'afficher les grilles

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles
        joueur (type:str) : joueur courant

    Returns:
        None
    """
    X_GRILLES_TIR = 500
    Y_GRILLES_TIR = -250
    X_GRILLES_BATEAU = -50
    Y_GRILLES_BATEAU = -250
    pg.grille(X_GRILLES_TIR, Y_GRILLES_TIR)
    pg.grille(X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
    pg.info_grille()
    if joueur == current_player:
        pg.info_tour("oui")
    else:
        pg.info_tour("non")
    
    # afficher la grille des bateauxs
    for i in range(0, 100):            
        if grilles["humain"]['grille_bateau'][i] == "b":
            pg.bateau((i%10)+1, (i//10)+1)
        if grilles["ia"]["grille_tir"][i] == "t":
            pg.croix((i%10)+1, (i//10)+1, 'green', X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
        if grilles["ia"]["grille_tir"][i] == "m":
            pg.croix((i%10)+1, (i//10)+1, 'red', X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
    # afficher la grille des tirs
    for i in range(0, 100):
        if grilles["humain"]["grille_tir"][i] == "t":
            pg.croix((i%10)+1, (i//10)+1, 'green', X_GRILLES_TIR, Y_GRILLES_TIR)
        if grilles["humain"]["grille_tir"][i] == "m":
            pg.croix((i%10)+1, (i//10)+1,  'red', X_GRILLES_TIR, Y_GRILLES_TIR)

def check_win(grilles, joueur):
    """Verifie si le joueur a gagne

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles de bateaux et de tir
        joueur (type:str) : joueur courant

    Returns:
        (type:bool) : True si le joueur a gagne, False sinon
    """
    if grilles[joueur]["grille_bateau"].count("t") == 14:
        return True
    else:
        return False

def tour(grilles, current_player):
    """Tour de jeu

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles de bateaux et de tir
        current_player (type:str) : joueur courant
    """
    pg.blue_screen()

    affiche_grilles(grilles, current_player, current_player)
    # tour du joueur courant
    if current_player == "humain":
        # tour du joueur
        while True:
            tir = pg.get_tir()
            if "," in tir:
                tir = tir.split(",")
                x = int(tir[0]) -1
                y = int(tir[1]) -1
                if x >= 0 or x <= 10 or y >= 0 or y <= 10:
                    tir = x + y * 10
                    break
        return tir
    else:
        # tour de l'ia
        x = random.randint(0, 10) - 1
        y = random.randint(0, 10) - 1
        tir = x + y * 10
        return tir

def boucle_jeu(grilles, current_player):
    """Boucle de jeu

    Args:
        grilles (type:dict) : dictionnaire contenant les grilles de bateaux et de tir
        current_player (type:str) : joueur courant
    """
    while True:
        # faire le tour
        tir = tour(grilles, current_player)

        # modifie grille et si touche
        if grilles[change_current_player(current_player)]["grille_bateau"][tir] == "b":
            grilles[current_player]["grille_bateau"][tir] = "t"
            grilles[current_player]["grille_tir"][tir] = "t"
        else:
            grilles[current_player]["grille_tir"][tir] = "m"

        # check si le joueur a gagne
        if check_win(grilles, current_player):
            break

        # change le joueur courant
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
    grilles["ia"]["grille_bateau"] = genere_grille_bateau(grilles, "ia")

    # placer les bateaux du joueur
    grilles["humain"]["grille_bateau"] = genere_grille_bateau(grilles, "humain")

    # boucle de jeu
    boucle_jeu(grilles, current_player)
