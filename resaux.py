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
    try : 
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind le socket
        sock.bind(('127.0.0.1', port))
        # ecouter les connexions
        sock.listen()
        #pg.attente("En attente d'un joueur")
        # accepter les connexions
        sock, infos_connexion = sock.accept()
        # place les bateaux
        joueur = 1
        place_bateau(joueur, sock)
    except:
        pass

# method devenir un client
def become_client(port):
    """Create a client socket .

    La  methode creer un socket et le connecte au serveur

    Args:
        port (type:int) : port du serveur

    """
    try:
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connecter le socket
        sock.connect(("127.0.0.1", port)) # Port to listen on (non-privileged ports are > 1023) ### netstat -an
        # place les bateaux
        joueur = 2
        place_bateau(joueur, sock)
    except:
        pass

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
            grilles[data[1]]["grille_bateau"] = data[2]
            break

def genere_grille_bateau(joueur):
    global grilles
    bateaux = [2, 3, 3, 4, 5]
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
    boucle_de_jeu(joueur, sock)  

def boucle_de_jeu(joueur, sock):
    current_player = 1

    while True:
        # envoyer le tour
        send_message(sock, "tour/" + str(current_player))
        # attendre le tour
        data = listen_message(sock)
        if data[0] == "tour":
            current_player = int(data[1][0])

        #faire le tour
        tir =  tour(grilles[f"joueur{current_player}"], current_player, joueur)

def tour(grille, current_player, joueur):

    pg.blue_screen()
    # afficher la grille des tirs
    X_GRILLES_TIR = 0
    Y_GRILLES_TIR = 0
    pg.grille(X_GRILLES_TIR, Y_GRILLES_TIR)
# method resaux_game
def resaux_game(): 
    global grilles
    grilles = {"joueur1": {"grille_bateau": [""]*100, "grille_tir": [""]*100}, "joueur2": {"grille_bateau": [""]*100, "grille_tir": [""]*100}}
    ask_for_be_server_client()
