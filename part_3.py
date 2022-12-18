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

# method gere le serveur
def serveur(connexion):
    while True:
        #recuperer les donnees
        data = connexion.recv(1024)
        data = data.decode("utf-8")

        #envoyer la reponse
        connexion.sendall("Connexion établie".encode("utf-8"))

        #lancer le jeu
        #game(connexion)

def new_user():
    # creer un nouveau utilisateur
    
    # recuperer le nom de l'utilisateur
    name = GetPseudo.get_pseudo()

    #verifier si un serveur est en ligne
    try:
        # creer une connexion
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.connect(('localhost', 12345))
        print("Connexion établie avec le serveur")

        # envoyer joueur en ligne
        threading.Thread(target=send_user_connect, args=(connexion, name)).start()
        

        #recuperer la reponse du serveur
        data = connexion.recv(1024)
        print(data.decode("utf-8"))

        #lancer le jeu
        #game(connexion)

    except:
        # si le serveur n'est pas en ligne on lance un serveur

        # creer une serveur
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.bind(('localhost', 12345))
        serveur.listen(5)
        print("Serveur en ligne")

        # accepter les connexions
        connexion, adresse = serveur.accept()
        print("Connexion établie avec le client")

        





new_user()

