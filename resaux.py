# Programmé par Adam Vignolles

import socket
import threading
import partie_graphique as pg
import random

# gerer la partie resaux du jeu de la bataille naval


def ask_for_be_server_client():
    """Asks for be a server or a client 

    la methode demande a l'utilisateur si il veut etre un serveur ou un client

    Returns:
        sock -> [type:socket] : renvoie le socket du serveur ou du client
        joueur -> [type:int] : renvoie le numero du joueur
    """
    pg.menu_selection("Server ou client ?", 'server', 'client')
    pg.get_position_mouse('position_menu', 'server')

# method devenir un serveur
def become_server(port):
    """Create a server socket .

    La  methode creer un socket et le bind a l'adresse

    Args:
        port (type:int) : port du serveur 

    """
    global sock
    # creer un socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind le socket
    sock.bind(('127.0.0.1', port))
    # ecouter les connexions
    sock.listen()
    pg.attente_joueur()
    # accepter les connexions
    sock, infos_connexion = sock.accept()
    # place les bateaux
    joueur = 1
    place_bateau(joueur, sock)


# method devenir un client
def become_client(port):
    """Create a client socket .

    La  methode creer un socket et le connecte au serveur

    Args:
        port (type:int) : port du serveur

    """
    global sock
    # creer un socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connecter le socket
    sock.connect(("127.0.0.1", port)) # Port to listen on (non-privileged ports are > 1023) ### netstat -an
    # place les bateaux
    joueur = 2
    place_bateau(joueur, sock)

# method envoyer un message
def send_message(connexion, message):
    connexion.sendall(message.encode("utf-8"))

# method ecouter les messages
def listen_message(connexion):
    """Receive a message from the server .

    La methode recoit un message du serveur et le decode en utf-8 puis le split en fonction du caractere "/"

    Args:
        connexion (type:socket): socket du serveur

    Returns:
        data -> [type:list] : renvoie la liste du message decode
    """
    data = connexion.recv(1024)
    data = data.decode("utf-8")
    data = data.split("/")
    return data

# method wait bateau
def wait_bateau(connexion):
    """Wait for the ships to be placed .

    La methode attend que le joueur 1 place ses bateaux

    Args:
        connexion (type:socket): socket du serveur
    """
    while True:
        data = connexion.recv(1024)
        data = data.decode("utf-8")
        data = data.split("/")
        if data[0] == "grille_bateau":
            # transformer chain data 2 en liste
            data[2] = data[2].replace("[", "")
            data[2] = data[2].replace("]", "")
            data[2] = data[2].replace("'", "")
            data[2] = data[2].replace(" ", "")
            l = []
            for i in data[2].split(","):
                l.append(i)
            grilles[data[1]]["grille_bateau"] = l
            break

def genere_grille_bateau(joueur):
    """Generate the grid of the ships .

    La methode genere la grille des bateaux

    Args:
        joueur (type:int): numero du joueur

    Returns:
        grille_bateau -> [type:list] : renvoie la grille des bateaux
    """
    global grilles
    bateaux = [2, 3, 4, 5]
    grille_bateau = grilles[f'joueur{joueur}']['grille_bateau']
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

def place_bateau(joueur, sock):
    """Place the ships .

    La methode place les bateaux du joueur

    Args:
        joueur (type:int): numero du joueur
        sock (type:socket): socket du serveur
    """

    thread = threading.Thread(target=wait_bateau, args=(sock,))
    thread.start()

    genere_grille_bateau(joueur)

    # envoyer la grille
    send_message(sock, f"grille_bateau/joueur{joueur}/" + str(grilles[f"joueur{joueur}"]["grille_bateau"]))
   
    # attendre que les 2 joueurs place leurs bateaux
    bateaux_placer = False
    while not bateaux_placer:
        # placer les bateaux
        for i in grilles["joueur1"]["grille_bateau"]:
            if i != "":
                for j in grilles["joueur2"]["grille_bateau"]:
                    if j != "":
                        bateaux_placer = True
                        break
                break

    # lancer la boucle de jeu 
    boucle_de_jeu(joueur)  

def boucle_de_jeu(joueur):
    """Boucle de jeu .

    La methode permet de faire le tour des joueurs

    Args:
        joueur (type:int): numero du joueur
    """
    global sock, current_player
    current_player = 1

    pg.blue_screen()
    # afficher les grilles
    affiche_grilles(grilles, joueur)

    while True:
        # envoyer le tour
        send_message(sock, "tour/" + str(current_player))
        # attendre le tour
        data = listen_message(sock)
        if data[0] == "tour":
            current_player = int(data[1][0])

        #faire le tour
        tir = tour(grilles, joueur)
        if tir != None:
            # send message
            send_message(sock, "grille_tir/"+ f"joueur{current_player}/" + str(grilles[f"joueur{current_player}"]["grille_tir"]))


        #recuperer la grille de tir
        if current_player != joueur:
            last_grille_tir = grilles[f"joueur{current_player}"]["grille_tir"].copy()
            data = listen_message(sock)
            if data[0] == "grille_tir":
                # transformer chain data 2 en liste
                data[2] = data[2].replace("[", "")
                data[2] = data[2].replace("]", "")
                data[2] = data[2].replace("'", "")
                data[2] = data[2].replace(" ", "")
                l = []
                for i in data[2].split(","):
                    l.append(i)
                grilles[data[1]]["grille_tir"] = l

            # trouver la case qui a ete tire
            for i in range(0, 100):
                if last_grille_tir[i] != grilles[f"joueur{current_player}"]["grille_tir"][i]:
                    case = i
                    x = (case % 10) +1
                    y = (case // 10) +1
                    # afficher le resultat du tir
                    if grilles[f"joueur{current_player}"]["grille_tir"][i] == "t":
                        pg.croix(x, y, "green", X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
                    elif grilles[f"joueur{current_player}"]["grille_tir"][i] == "m":
                        pg.croix(x, y, "red", X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
                    break




        # changer le joueur courant

        current_player = change_current_player(current_player)

        # verifier si le joueur a gagner
        if check_win(grilles) == "joueur1" or check_win(grilles) == "joueur2":
            send_message(sock, "win/" + check_win(grilles))
            # recuperer le message
            data = listen_message(sock)
            if data[0] == "win":
                if data[1] == f"joueur{joueur}":
                    pg.partie_gagnee()
                else:
                    pg.partie_perdu()
            break




def change_current_player(current_player):
    """Change the current player .

    La methode permet de changer le joueur courant

    Args:
        current_player (type:int) : numero du joueur

    Returns:
        current_player (type:int) : numero du joueur
    """
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1
    return current_player

def verifie_si_toucher(grille, position):
    """Verifie si le joueur a touche un bateau.

    La methode permet de verifier si le joueur a touche un bateau

    Args:
        grille (type:dict) : grille du joueur
        position (type:int) : position du joueur

    Returns:
        True si le joueur a touche un bateau
        False si le joueur n'a pas touche un bateau
    """

    if position != None:
        if grille[position] == "b":
            return True
        else:
            return False 


def affiche_grilles(grilles, joueur):
    """Affiche les grilles de jeu.

    La methode permet d'afficher les grilles de jeu

    Args:
        grilles (type:dict) : dictionnaire des grilles
        joueur (type:int) : numero du joueur

    Returns:
        None
    """
    global current_player
   
    pg.grille(X_GRILLES_TIR, Y_GRILLES_TIR)
    pg.grille(X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
    pg.info_grille()
    if joueur == current_player:
        pg.info_tour("oui")
    else:
        pg.info_tour("non")
    autre_joueur = change_current_player(joueur)

    # afficher la grille des bateauxs
    for i in range(0, 100):            
        if grilles[f"joueur{joueur}"]['grille_bateau'][i] == "b":
            pg.bateau((i%10)+1, (i//10)+1)
        if grilles[f"joueur{autre_joueur}"]["grille_tir"][i] == "t":
            pg.croix((i%10)+1, (i//10)+1, 'red', X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
        if grilles[f"joueur{autre_joueur}"]["grille_tir"][i] == "m":
            pg.croix((i%10)+1, (i//10)+1, 'green', X_GRILLES_BATEAU, Y_GRILLES_BATEAU)
    # afficher la grille des tirs
    for i in range(0, 100):
        if grilles[f"joueur{joueur}"]["grille_tir"][i] == "t":
            pg.croix((i%10)+1, (i//10)+1, 'green', X_GRILLES_TIR, Y_GRILLES_TIR)
        if grilles[f"joueur{joueur}"]["grille_tir"][i] == "m":
            pg.croix((i%10)+1, (i//10)+1,  'red', X_GRILLES_TIR, Y_GRILLES_TIR)
    

def check_win(grilles):
    """Check if a player has won the game

    args:
        grilles (type:dict): contains the grids of the players

    returns:
        str: "joueur1" or "joueur2" if a player has won the game
        False: if no player has won the game
    """
    if grilles["joueur1"]["grille_tir"].count("t") == 14:
        return "joueur1"
    elif grilles["joueur2"]["grille_tir"].count("t") == 14:
        return "joueur2"
    else:
        return False

def tour(grilles, joueur, tir=None):
    """AI is creating summary for tour



    Args:
        grilles ([type:list]): contient les grilles des joueurs
        joueur ([type:int]): numero du joueur
        tir ([type:int], optional): position du tir. Defaults to None.

    Returns:
        [type:list]: contient les grilles des joueurs
    """
    global current_player
    

    #faire le tir
    if joueur == current_player:
        while True:
            tir = pg.get_tir()
            if "," in tir:
                tir = tir.split(",")
                x = int(tir[0]) -1
                y = int(tir[1]) -1
                if x >= 0 or x <= 10 or y >= 0 or y <= 10:
                    tir = x + y * 10
                    break

        if grilles[f"joueur{change_current_player(joueur)}"]["grille_bateau"][tir] == "b":
            grilles[f"joueur{joueur}"]["grille_tir"][tir] = "t"
            # afficher le resultat du tir
            pg.croix((tir%10)+1, (tir//10)+1, 'green', X_GRILLES_TIR, Y_GRILLES_TIR)

        else:
            grilles[f"joueur{joueur}"]["grille_tir"][tir] = "m"

            # afficher le resultat du tir
            pg.croix((tir%10)+1, (tir//10)+1, 'red', X_GRILLES_TIR, Y_GRILLES_TIR)

        return tir
    else:
        return None

    


# method resaux_game
def resaux_game(): 
    """AI is creating summary for resaux_game """
    global grilles, X_GRILLES_BATEAU, Y_GRILLES_BATEAU, X_GRILLES_TIR, Y_GRILLES_TIR
    X_GRILLES_TIR = 500
    Y_GRILLES_TIR = -250
    X_GRILLES_BATEAU = -50
    Y_GRILLES_BATEAU = -250
    grilles = {"joueur1": {"grille_bateau": [""]*100, "grille_tir": [""]*100}, "joueur2": {"grille_bateau": [""]*100, "grille_tir": [""]*100}}
    ask_for_be_server_client()
