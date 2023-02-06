#encoding: utf-8

import socket
import threading
import json
from Adam_V_Parte_3_v1 import *
from IA_GAME_v1 import *

#ajout de la gestion de mode de jeu, avec ia ou en resaux

def game_mode():
    """Ask for the game mode

    La methode demande le mode de jeu

    Returns:
        mode -> [type:str] : renvoie le mode de jeu
    """
    mode = input("mode de jeu? ")
    if mode == "ia":
        ia_game()
    elif mode == "resaux":
        resaux_game()
    else:
        print("mode de jeu invalide")
        game_mode()
        
if __name__ == "__main__":
    game_mode()
