#encoding: utf-8

import socket
import threading
import random

# gerer la partie resaux du jeu de la bataille naval

# method wait bateau
def wait_bateau(connexion):
    while True:
        data = listen_message(connexion)
        if data[0] == "grille_bateau":
            grilles[data[1]]["grille_bateau"] = data[2]
            break

# method ecouter les messages
def listen_message(connexion):
    data = connexion.recv(1024)
    data = data.decode("utf-8")
    data = data.split("/")
    return data

# method envoyer un message
def send_message(connexion, message):
    connexion.send(message.encode("utf-8"))


# method demande choix de serveur ou client
def ask_for_be_server_client():
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
    
    # gerer le placement des bateaux des 2 joueur
    #placer les bateaux
    place_bateau(joueur, sock)

    return sock, joueur


# method devenir un serveur
def become_server(port):
    try : 
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind le socket
        sock.bind(('0.0.0.0', port))
        # ecouter les connexions
        sock.listen()
        # retourner le socket
        return sock
    except:
        return None

# method devenir un client
def become_client(port):
    try:
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connecter le socket
        sock.connect(("127.0.0.1", port)) # Port to listen on (non-privileged ports are > 1023) ### netstat -an
        # retourner le socket
        return sock
    except:
        return None

def place_bateaux_joueur(grille_bateaux):
    # generer une grille de bateau aleatoire
    for j in range(2,6):
        sens = random.randint(0, 1)
        if sens == 0:
            # horizontal
            position = random.randint(0, 99)
            #verifier si il y a deja un bateau a cette position en verifiant si tout les cases sont vide
            while "b" in grille_bateaux[position:position + j] and position % 10 + j <= 10 and position + j * 10 <= 99:
                position = random.randint(0, 99)
            
            #verifier si le bateau ne sort pas de la grille
            if position % 10 + j <= 10:
                for k in range(0, j):
                    grille_bateaux[position + k] = "b"
            # si le bateau sort de la grille, on le place a l'envers
            else:
                for k in range(0, j):
                    grille_bateaux[position - k] = "b"
        else:
            # vertical
            position = random.randint(0, 99)
            #verifier si il y a deja un bateau a cette position en verifiant si tout les cases sont vide
            while "b" in grille_bateaux[position:position + j] and position % 10 + j <= 10 and position + j * 10 <= 99:
                position = random.randint(0, 99)
            # verifier si le bateau ne sort pas de la grille
            if position + j * 10 <= 99:
                for k in range(0, j):
                    grille_bateaux[position + k * 10] = "b"
            # si le bateau sort de la grille, on le place a l'envers
            else:
                for k in range(0, j):
                    grille_bateaux[position - k * 10] = "b"
    return grille_bateaux

def place_bateau(joueur, sock):
    # attendre que le joueur 1 place ses bateaux
    thread = threading.Thread(target=wait_bateau, args=(sock,))
    thread.start()

    # placer les bateaux
    grille_bateaux = grilles[f"joueur{joueur}"]["grille_bateau"]
    grille_bateaux = place_bateaux_joueur(grille_bateaux)

    # envoyer la grille
    send_message(sock, f"grille_bateau/joueur{joueur}/" + str(grille_bateaux))

    # attendre que les 2 joueurs place leurs bateaux
    bateaux_placer = False
    while not bateaux_placer:
        # placer les bateaux
        if grilles["joueur1"]["grille_bateau"].count("b") != 0 and grilles["joueur2"]["grille_bateau"].count("b") != 0:
            bateaux_placer = True
        bateaux_placer = True

def tour(joueur_grille, current_player, joueur):
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

def receive_message(sock):
    # essayer de recevoir le message plusieur fois
    data = None
    while data == None:
        try:
            data = sock.recv(1024).decode("utf-8")
        except:
            data = None
    # retourner le message
    return data.split("/")

def boucle_jeu(sock, joueur, current_player):
    while True:
        # envoyer le tour
        send_message(sock, "tour/" + str(current_player) + "/")

        # essayer de recevoir le tour plusieur fois
        data = receive_message(sock)
        if data[0] == "tour":

            print(data)
            current_player = int(data[1])

        # faire le tour
        if current_player == joueur:
            tir = tour(grilles[f"joueur{current_player}"], current_player, joueur)
            print(tir)
            # envoyer la grille tir du joueur
            send_message(sock, f"grille_tir/joueur{current_player}/{tir}")

            # changer de joueur
            current_player = change_current_player(current_player)

            # verifier si le joueur a touche un bateau
            if grilles[f"joueur{current_player}"]["grille_bateau"][int(tir)] == "b":
                print("touche")
                grilles[f"joueur{current_player}"]["grille_bateau"][int(tir)] = "t"
        
        

        # sinon recuperer les donne du tour de l'autre joueur
        else :
            data = listen_message(sock)
            print(data, joueur)
            if data[0] == "grille_tir":
                grilles[data[1]]["grille_tir"][int(data[2])] = "t"
                #changer de joueur
                current_player = change_current_player(current_player)
                # verifier si le joueur a touche un bateau
                if grilles[f"joueur{current_player}"]["grille_bateau"][int(data[2])] == "b":
                    grilles[f"joueur{current_player}"]["grille_bateau"][int(data[2])] = "t"
                    print("touche")

        # afficher les grilles
        affiche_les_grilles()


        # verifier si la partie est fini
        # if fini:
        #   break

def resaux_game():
    # demander si le joueur veut etre serveur ou client
    sock, joueur = ask_for_be_server_client()  
        
    print("les bateaux sont placer")

    # commencer la partie
    print("commencer la partie")
    current_player = 1

    # lancer la partie/ le jeu
    boucle_jeu(sock, joueur, current_player)

#essai
if __name__ == "__main__":
    grilles = {"joueur1": {"grille_bateau": [""]*100, "grille_tir": [""]*100}, "joueur2": {"grille_bateau": [""]*100, "grille_tir": [""]*100}}
    # demarrer la partie en reseau
    resaux_game()