#encoding: utf-8

import socket
import threading
import json
from Adam_V_Parte_3_v1 import *
from IA_GAME_v1 import *

#ajout de la gestion de mode de jeu, avec ia ou en resaux

def game_mode():
    mode = input("mode de jeu? ")
    if mode == "ia":
        ia_game()
    elif mode == "resaux":
        resaux_game()
    else:
        print("mode de jeu invalide")
        game_mode()

game_mode()