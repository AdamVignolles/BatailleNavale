#encoding: utf-8

import socket
import threading

# gerer la partie resaux du jeu de la bataille naval

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

# method envoyer un message
def send_message(connexion, message):
    connexion.sendall(message.encode("utf-8"))

def ask_for_be_server_client():
    """Asks for be a server or a client 

    la methode demande a l'utilisateur si il veut etre un serveur ou un client

    Returns:
        sock -> [type:socket] : renvoie le socket du serveur ou du client
        joueur -> [type:int] : renvoie le numero du joueur
    """
    if input("server ou client? ") == "server":
        serveur_on = False
        while not serveur_on:
            port = int(input("code serveur: "))
            sock = become_server(port)
            if sock == None:
                print("code deja utiliser")
            else:
                print("en attente de connexion")
                sock, infos_connexion = sock.accept()
                print("connexion accepter")
                serveur_on = True

        print("vous etes le joueur 1")
        joueur = 1
        
        #placer les bateaux
        place_bateau(joueur, sock)

    else:
        connect_with_serv = False
        while not connect_with_serv:
            port = int(input("code serveur: "))
            sock = become_client(port)
            if sock == None:
                print("aucun serveur sur ce code trouver")
            else:
                print("client connecter")
                connect_with_serv = True

        print("vous etes le joueur 2")
        joueur = 2

        #placer les bateaux
        place_bateau(joueur, sock)

    return sock, joueur


# method devenir un serveur
def become_server(port):
    """Create a server socket .

    La  methode creer un socket et le bind a l'adresse

    Args:
        port (type:int) : port du serveur 

    Returns:
        sock -> [type:socket] : renvoie le socket du serveur si il a reussi a creer le socket sinon renvoie None
    """
    try : 
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind le socket
        sock.bind(('127.0.0.1', port))
        # ecouter les connexions
        sock.listen()
        # retourner le socket
        return sock
    except:
        return None

# method devenir un client
def become_client(port):
    """Create a client socket .

    La  methode creer un socket et le connecte au serveur

    Args:
        port (type:int) : port du serveur

    Returns:
        sock -> [type:socket] : renvoie le socket du client si il a reussi a creer le socket sinon renvoie None
    """
    try:
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connecter le socket
        sock.connect(("127.0.0.1", port)) # Port to listen on (non-privileged ports are > 1023) ### netstat -an
        # retourner le socket
        return sock
    except:
        return None

def place_bateau(joueur, sock):
    """Place the ships on the grid .

    La methode place les bateaux sur la grille

    Args:
        joueur (type:int) : numero du joueur
        sock (type:socket) : socket du serveur ou du client
    """
    # attendre que le joueur 1 place ses bateaux
    thread = threading.Thread(target=wait_bateau, args=(sock,))
    thread.start()

    # placer les bateaux
    # place_bateaux()
    grilles[f"joueur{joueur}"]["grille_bateau"] = [""]*100
    grilles[f"joueur{joueur}"]["grille_tir"] = [""]*100

    # envoyer la grille
    send_message(sock, "grille_bateau/joueur2/" + str(grilles[f"joueur{joueur}"]["grille_bateau"]))

    # attendre que les 2 joueurs place leurs bateaux
    bateaux_placer = False
    while not bateaux_placer:
        # placer les bateaux
        if grilles["joueur1"]["grille_bateau"] != [] and grilles["joueur2"]["grille_bateau"] != []:
            bateaux_placer = True
        bateaux_placer = True

def tour(joueur_grille, current_player, joueur):
    """The turn of the player .

    La methode permet de faire le tour du joueur

    Args:
        joueur_grille (type:dict) : grille du joueur
        current_player (type:int) : numero du joueur
        joueur (type:int) : numero du joueur
    """
    # afficher les grilles du joueurs
    if current_player == joueur:
        print(current_player, joueur)
        print(f"tour: Joueur {current_player}")
        print("bateaux:", joueur_grille["grille_bateau"])
        print("tir:",joueur_grille["grille_tir"])
        tir = int(input("case n° tir :"))
        joueur_grille["grille_tir"][int(tir)] = "t"
        print("tir", joueur_grille["grille_tir"])
        return tir

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

def affiche_les_grilles():
    print("grille joueur 1")
    print("bateaux:", grilles["joueur1"]["grille_bateau"])
    print("tir:",grilles["joueur1"]["grille_tir"])
    print("grille joueur 2")
    print("bateaux:", grilles["joueur2"]["grille_bateau"])
    print("tir:",grilles["joueur2"]["grille_tir"])


def boucle_jeu(sock, joueur, current_player):
    """The game loop .

    La methode permet de faire la boucle du jeu

    Args:
        sock (type:socket) : socket du serveur ou du client
        joueur (type:int) : numero du joueur
        current_player (type:int) : numero du joueur
    """
    while True:
        # envoyer le tour
        send_message(sock, "tour/" + str(current_player))
        # attendre le tour
        data = listen_message(sock)
        if data[0] == "tour":
            current_player = int(data[1][0])
        
        # faire le tour
        tir = tour(grilles[f"joueur{current_player}"], current_player, joueur)

        # envoyer la grille tir du joueur 1
        print(tir)
        send_message(sock, f"grille_tir/joueur{current_player}/" + str(tir))

        # recuperer message si besoin
        if current_player != joueur:
            data = listen_message(sock)
            print(data, joueur)
            if data[0] == "grille_tir":
                grilles[data[1]]["grille_tir"][int(data[2])] = "t"

        # afficher les grilles
        affiche_les_grilles()

        #changer de joueur
        current_player = change_current_player(current_player)

        # verifier si la partie est fini
        # if fini:
        #   break

def resaux_game():
    """The game .

    La methode permet de faire le jeu
    """
    # demander si le joueur veut etre serveur ou client
    sock, joueur = ask_for_be_server_client()  
        
    print("les bateaux sont placer")

    # commencer la partie
    print("commencer la partie")

    current_player = 1

    # boucle de jeu
    boucle_jeu(sock, joueur, current_player)

#essai
if __name__ == "__main__":
    grilles = {"joueur1": {"grille_bateau": [""]*100, "grille_tir": [""]*100}, "joueur2": {"grille_bateau": [""]*100, "grille_tir": [""]*100}}

    resaux_game()
