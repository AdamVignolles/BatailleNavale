# Programmé par Adam Vignolles 1G5

#Jeu de la bataille naval
import partie_graphique as pg
from Adam_V_Parte_3_v1 import *
from IA_GAME_v1 import *
import turtle as tt

def choix_do(choix):
    print(choix)
    if choix != "":
        if choix == "menu 1":
            ia_game()
        elif choix == "menu 2":
            resaux_game()


def game_mode():
    """Ask for the game mode

    La methode demande le mode de jeu

    Returns:
        mode -> [type:str] : renvoie le mode de jeu
    """
    pg.menu_selection("mode de jeu?", 'ia', 'resaux')
    pg.get_position_mouse('position_menu')
        
        
if __name__ == "__main__":
    game_mode()

    tt.mainloop()