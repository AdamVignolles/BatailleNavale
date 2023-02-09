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
    global sock, current_player
    current_player = 1

    while True:
        # envoyer le tour
        print("envoyer tour")
        send_message(sock, "tour/" + str(current_player))
        print("attendre tour")
        # attendre le tour
        data = listen_message(sock)
        if data[0] == "tour":
            current_player = int(data[1][0])
            print(f"Tour du joueur {current_player}")

        #faire le tour
        tir = tour(grilles, joueur)
        if tir != None:
            print(tir, "tir")
            # send message
            send_message(sock, "grille_tir/"+ f"joueur{current_player}/" + str(grilles[f"joueur{current_player}"]["grille_tir"]))


        #recuperer la grille de tir
        if current_player != joueur:
            print("attendre grille_tir")
            data = listen_message(sock)
            print(data, "data tour joue par l'adversaire")
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
                print(grilles[data[1]]["grille_tir"], "tir joue par l'adversaire")



        # changer le joueur courant

        current_player = change_current_player(current_player)
        print(current_player, "current_player")

        # verifier si le joueur a gagner
        if check_win(grilles) == "joueur1":
            send_message(sock, "win/joueur1")
            # recuperer le message
            data = listen_message(sock)
            if data[0] == "win":
                if data[1] == f"joueur{joueur}":
                    pg.partie_gagnee()
                else:
                    pg.partie_perdue()
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
    if position != None:
        if grille[position] == "b":
            return True
        else:
            return False 


def affiche_grilles(grilles, joueur):
    global current_player
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
    autre_joueur = change_current_player(joueur)

    # afficher la grille des bateauxs
    print(grilles[f"joueur{joueur}"]['grille_bateau'], "grille_bateauaaaaa")
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
    if grilles["joueur1"]["grille_bateau"].count("t") == 8:
        return "joueur1 a gagné"
    elif grilles["joueur2"]["grille_bateau"].count("t") == 8:
        return "joueur2 a gagné"
    else:
        return False

def tour(grilles, joueur, tir=None):
    global current_player
    pg.blue_screen()
    # afficher les grilles
    affiche_grilles(grilles, joueur)

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

        print(grilles[f"joueur{change_current_player(joueur)}"]["grille_bateau"], "grille_bateau")
        print(grilles[f"joueur{change_current_player(joueur)}"]["grille_bateau"][tir],"tirrrr")
        if grilles[f"joueur{change_current_player(joueur)}"]["grille_bateau"][tir] == "b":
            grilles[f"joueur{joueur}"]["grille_tir"][tir] = "t"
            print("touche")
        else:
            grilles[f"joueur{joueur}"]["grille_tir"][tir] = "m"
            print("manque")

        return tir
    else:
        print("autre joueur")
        return None

    


# method resaux_game
def resaux_game(): 
    global grilles
    grilles = {"joueur1": {"grille_bateau": [""]*100, "grille_tir": [""]*100}, "joueur2": {"grille_bateau": [""]*100, "grille_tir": [""]*100}}
    ask_for_be_server_client()
