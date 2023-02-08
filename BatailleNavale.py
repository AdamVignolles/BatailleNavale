# Programmé par Adam Vignolles 1G5

#Jeu de la bataille naval
import partie_graphique as pg
import resaux
from IA_GAME_v1 import *
import turtle as tt

def choix_do(choix, type_choix):
    print(choix)
    if type_choix == "mode_de_jeu":
        if choix != "":
            if choix == "menu 1":
                ia_game()
            elif choix == "menu 2":
                resaux.resaux_game()
    elif type_choix == "server":
        if choix != "":
            if choix == "menu 1":
                port = pg.get_code()
                resaux.become_server(int(port))
            elif choix == "menu 2":
                port = pg.get_code()
                resaux.become_client(int(port))


def game_mode():
    """Ask for the game mode

    La methode demande le mode de jeu

    Returns:
        mode -> [type:str] : renvoie le mode de jeu
    """
    pg.menu_selection("mode de jeu?", 'ia', 'resaux')
    pg.get_position_mouse('position_menu', 'mode_de_jeu')
        
        
if __name__ == "__main__":
    game_mode()

    tt.mainloop()