# encoding: utf-8
import socket
import threading
import GetPseudo
import time

# gerer la partie resaux du jeu de la bataille navale

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
        print(data)


#method pour gerer la connexion et/ou le start d'un serv d'un nouveau joueur
def connect_new_user(pseudo, port=12345):
    
    #on esai de se connecter au serveur si il n'y a pas de reponse on lance un serveur
    try:
        #creation de la socket
        print(1)
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.connect(('localhost', port))
        # on envoi le pseudo du joueur
        connexion.sendall(f"pseudo/{pseudo}".encode("utf-8"))
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
connexion = connect_new_user("Adam")
while True:
    data = connexion.recv(1024)
    data = data.decode("utf-8")
    print(data)

