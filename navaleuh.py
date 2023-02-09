def check_win(grilles):
    if grilles["Joueur_1"].count("bat") == 0:
        print("Le joueur 2 a gagné")
        return True
    if grilles["Joueur_2"].count("bat") == 0:
        print("Vous avez gagné")
        return True
    return False



grilles = {"humain": {"grille_bateau": [[""]*10]*10, "grille_tir": [[""]*10]*10 }, "ia": { "grille_bateau": [""]*100, "grille_tir": [""]*100}}