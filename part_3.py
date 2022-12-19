# encoding: utf-8
import socket
import threading
import GetPseudo
import time
import json

#########s convert str '{joueur1:{grille:[0, 0, 0,0 ], bateaux:[]}, joueur2:{grille:[], bateaux:[]}}' to dict
dico = json.loads('{"joueur1":{"grille":[0,0,0,0], "bateaux":[]}, "joueur2":{"grille":[], "bateaux":[]}}')

# gerer la partie resaux du jeu de la bataille naval

#method get lsite des joueur en ligne
def get_liste_joueur():
    return liste_joueur

# method check_joueur_online
def check_joueur_online():
    
    # supprimer les joueur qui sont plus en ligne depuis plus de 60 secondes
    for i in liste_joueur:
        if int(liste_joueur[i] - time.time()) > 60:
            del liste_joueur[i]

    return liste_joueur


#method pour envoyer toutes les minuttes que le joueur est toujours en ligne
def send_user_connect(connexion, name):
    while True:
        connexion.sendall(f"player_online/{name}".encode("utf-8"))
        time.sleep(60)

#method pour ecouter les messages du serveur
def listen_server(connexion):
    while True:
        data = connexion.recv(1024)
        data = data.decode("utf-8")
        # thread le get liste joueur
        data = data.split("/")
        if data[0] == "player_online":
            liste_joueur[data[1]] = time.time()
        return data


#method pour gerer la connexion et/ou le start d'un serv d'un nouveau joueur
def connect_new_user(pseudo, port=12345):
    
    #on esai de se connecter au serveur si il n'y a pas de reponse on lance un serveur
    try:
        #creation de la socket
        print(1)
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.connect(('localhost', port))
        # thread et on envoi le pseudo du joueur
        threading.Thread(target=send_user_connect(connexion, pseudo)).start()
        print(2)
    except:
        print(3)
        #creation de la socket
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.bind(('localhost', port))
        connexion.listen(5)
        connexion, infos_connexion = connexion.accept()
        # on envoi le pseudo du joueur
        connexion.sendall(f"pseudo/{pseudo}".encode("utf-8"))
        print(4)       

    return connexion

# essai 
liste_joueur = {}
pseudo = "Adam"
connexion = connect_new_user(pseudo)
threading.Thread(target=listen_server(connexion)).start()
threading.Thread(target=send_user_connect(connexion, pseudo)).start()
while True:
    print(get_liste_joueur())
    time.sleep(1)

