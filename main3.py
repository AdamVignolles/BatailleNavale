#encoding: utf-8

import socket
import threading
import json

# gerer la partie resaux du jeu de la bataille naval

# method wait bateau
def wait_bateau(connexion):
    while True:
        data = connexion.recv(1024)
        data = data.decode("utf-8")
        data = data.split("/")
        if data[0] == "grille_bateau":
            grilles[data[1]]["grille_bateau"] = data[2]
            print(grilles)
            break

# method ecouter les messages
def listen_message(connexion):
    data = connexion.recv(1024)
    data = data.decode("utf-8")
    data = data.split("/")
    return data

# method envoyer un message
def send_message(connexion, message):
    connexion.sendall(message.encode("utf-8"))


# method devenir un serveur
def become_server(port):
    try : 
        # creer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind le socket
        sock.bind(("", port))
        # ecouter les connexions
        sock.listen(5)
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
        sock.connect(("localhost", port))
        # retourner le socket
        return sock
    except:
        return None

def tour(joueur_grille, current_joueur):
    # afficher les grilles du joueurs
    if current_joueur == joueur:
        print(f"tour {current_joueur}")
        print(joueur_grille["grille_bateau"])
        print(joueur_grille["grille_tir"])
        tir = int(input("case n° tir :"))
        joueur_grille["grille_tir"][tir] = "t"
        print(joueur_grille["grille_tir"])

#essai
if __name__ == "__main__":
    grilles = {"joueur1": {"grille_bateau": [""]*100, "grille_tir": [""]*100}, "joueur2": {"grille_bateau": [""]*100, "grille_tir": [""]*100}}

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
        
        
        # attendre que le joueur 2 place ses bateaux
        thread = threading.Thread(target=wait_bateau, args=(sock,))
        thread.start()
        
        # placer les bateaux
        # place_bateaux()
        grilles["joueur1"]["grille_bateau"] = [""]*100
        grilles["joueur1"]["grille_tir"] = [""]*100

        # envoyer la grille
        send_message(sock, "grille_bateau/joueur1/" + str(grilles["joueur1"]["grille_bateau"]))

        # attendre que les 2 joueurs place leurs bateaux
        bateaux_placer = False
        while not bateaux_placer:
            # placer les bateaux
            if grilles["joueur1"]["grille_bateau"] != [] and grilles["joueur2"]["grille_bateau"] != []:
                bateaux_placer = True
            bateaux_placer = True


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

        # attendre que le joueur 1 place ses bateaux
        thread = threading.Thread(target=wait_bateau, args=(sock,))
        thread.start()

        # placer les bateaux
        # place_bateaux()
        grilles["joueur2"]["grille_bateau"] = [""]*100
        grilles["joueur2"]["grille_tir"] = [""]*100

        # envoyer la grille
        send_message(sock, "grille_bateau/joueur2/" + str(grilles["joueur2"]["grille_bateau"]))

        # attendre que les 2 joueurs place leurs bateaux
        bateaux_placer = False
        while not bateaux_placer:
            # placer les bateaux
            if grilles["joueur1"]["grille_bateau"] != [] and grilles["joueur2"]["grille_bateau"] != []:
                bateaux_placer = True
            bateaux_placer = True
        
    print("les bateaux sont placer")
    print(grilles)

    # commencer la partie
    print("commencer la partie")

    # boucle de jeu
    while True:
        tour(grilles["joueur1"], joueur)
        break
        # tour du joueur 1
        # tour_joueur_1()

        # tour du joueur 2
        # tour_joueur_2()

        # verifier si la partie est fini
        # if fini:
        #   break