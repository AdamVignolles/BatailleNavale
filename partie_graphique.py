#Programé par Lenny Cohen 1G5

import turtle as tt
import BatailleNavale as bn
import resaux
tt.hideturtle()



def blue_screen():       #met le fond de pyton en bleu (permet de simulé la mers)
    tt.reset()
    tt.up()
    tt.goto(1000,1000)
    tt.color("blue")
    tt.speed(0)
    tt.down()
    tt.begin_fill()
    tt.goto(-1000,1000)
    tt.goto(-1000,-1000)
    tt.goto(1000,-1000)
    tt.end_fill()
    tt.up()
    tt.hideturtle()
    tt.color("black")
    

def trace_partie_grille():          #Permet de racourcir le programe grille avec cette fonction
    for i in range (4):
        tt.forward(longueur_case*10)
        tt.left(90)
        tt.forward(longueur_case)
        tt.left(90)
        tt.forward(longueur_case*10)
        tt.right(90)
        tt.forward(longueur_case)
        tt.right(90)
    tt.forward(longueur_case*10)
    tt.left(90)
    tt.forward(longueur_case)
    tt.left(90)
    tt.forward(longueur_case*10)
    
def grille (x,y) :           #Crée une grill de 10X10 100 cases total et on y rentre les cordonné du coin bas  gauche (x,y)
    tt.up()
    tt.speed(0)
    tt.goto(x,y)
    tt.down()
    tt.setheading(0)
    tt.backward(longueur_case*10)
    tt.left(90)
    tt.forward(longueur_case)
    tt.right(90)
    trace_partie_grille()
    tt.backward(longueur_case*10)
    tt.right(90)
    tt.backward(longueur_case*10)
    tt.left(90)
    tt.forward(longueur_case)
    tt.right(90)
    trace_partie_grille()
    tt.hideturtle()
    grille_info(x,y)

def grille_info(x,y):               #Donne des info sur la grille avec les chifre a coé de chaque case
    tt.up()
    tt.speed(0)
    tt.goto(x,y)
    tt.setheading(0)
    tt.backward(longueur_case*10+10)
    tt.left(90)
    for i in range (10):
        tt.forward(longueur_case)
        tt.write(10-i,font=("Verdana",10, "normal"))
    tt.forward(longueur_case)
    tt.right(90)
    for i in range (1,11):
        tt.forward(longueur_case)
        tt.write(i,font=("Verdana",10, "normal"))
    tt.hideturtle()
        

    
 
def croix (x,y,color, tab_x, tab_y) :                               #Crée une croix avec comme millieux les coordonné (x,y) et prend comme autre argument la couleur de la croix
    """ Crée une croix avec comme millieux les coordonné (x,y)int et prend comme autre argument la couleur de la croix en str  """
    if tab_x <0:
        X = -((10-x+3)*longueur_case-abs(tab_x)-longueur_case/2)
        Y = -((y-1)*longueur_case-abs(tab_y)+longueur_case/2)
    else:
        X = -((10-x+1)*longueur_case-abs(tab_x)-longueur_case/2)
        Y = -((y-1)*longueur_case-abs(tab_y)+longueur_case/2)
    tt.up()
    tt.goto(X,Y)
    tt.down()
    tt.setheading(0)
    tt.color(color)
    tt.speed(0)
    tt.right(45)
    for i in range (4): 
        tt.forward(0.7*longueur_case)
        tt.backward(0.7*longueur_case)
        tt.right(90)
    tt.left(45)
    tt.color("black")
    tt.hideturtle()
    
def bateau(x,y) :                        #crée un bateau de "taille"(a entré dans la fonction) cases de longueur et de 1 de largeur ,prend comme coordonné (x,y) le millieux du bateau et ori est égal a l'orientation soit "vertical" ou "horrizontale" et return false si quelque chose d'autre est inseré 
    """#crée un bateau de "taille"(a entré dans la fonction) cases de longueur et de 1 de largeur ,prend comme coordonné (x,y)int le millieux du bateau et ori est égal a l'orientation soit "vertical" ou "horrizontale" en str et return false si quelque chose d'autre est inseré """
    #aller a la coordonné (x,y)
    tt.up()
    tt.goto(-((10-x+1+1)*longueur_case-abs(POSE_X_TABLEAU)),(10-y+1)*longueur_case-abs(POSE_Y_TABLEAU))
    tt.down()
    tt.speed(0)
    # couleur grise
    tt.color("grey")
    #faire un carré de la taille de la case en son centre
    tt.begin_fill()
    tt.right(90)
    for i in range (4):
        tt.forward(longueur_case)
        tt.right(90)
    tt.left(90)
    tt.end_fill()
    tt.up()
    tt.color("black")

def get_code():                           #Permet d'obtenir le code pour le port multijoueur
    """#Permet d'obtenir le code pour le port multijoueur en int """
    key = tt.textinput("Entrer le code du serveur(port)", "Code:")
    return key  
    
def menu_selection(name,name1,name2) :
    """#marque les trois donné inserét dans la fonction avec name (au centre haut )str,name1(plus bas a gauche)str ,name2(méme hauteur que name1 mais a droite)str;(sera utilisé pour les menu de selection )"""
    tt.reset()                            #marque les trois donné inserét dans la fonction avec name (au centre haut ),name1(plus bas a gauche) ,name2(méme hauteur que name1 mais a droite);(sera utilisé pour les menu de selection )
    tt.up()
    tt.goto(-200,100)
    tt.write(name,font=("Verdana",50, "normal"))
    tt.goto(-250,-100)
    tt.write(name1,font=("Verdana",50, "normal"))
    tt.goto(100,-100)
    tt.write(name2,font=("Verdana",50, "normal"))
    tt.hideturtle() 

         

    
def partie_perdu() :
    """#fonction lorsque que la partie est perdu  , écris "Loose" puis un "retry" sous un fond noir"""                            #fonction lorsque que la partie est perdu  , écris "Loose" puis un "retry" sous un fond noir 
    tt.reset()
    tt.up()
    tt.goto(-300,0)
    tt.write("Loose",font=("Verdana",150, "normal"))
    tt.goto(-1000,800)
    tt.setheading(0)
    tt.width(30)
    tt.down()
    tt.speed(16)
    for i in range (25):
        tt.forward(2000)
        tt.right(90)
        tt.forward(30)
        tt.right(90)
        tt.forward(2000)
        tt.left(90)
        tt.forward(30)
        tt.left(90)
    tt.up()
    tt.color("white")
    tt.goto(-200,0)
    tt.write("Retry?",font=("Verdana",100, "normal"))
    tt.hideturtle()
    tt.done()
    
    
def partie_gagnee():
    """#fonction lorsque que la partie est gagnee  , écris "WIN" puis un "retry" sous un fond jaune"""                             #Meme fonction que celuit pour la partie gagné mais marque win puis retry sous un fond jaune 
    tt.reset()
    tt.up()
    tt.goto(-200,0)
    tt.write("WIN",font=("Verdana",150, "normal"))
    tt.goto(-1000,800)
    tt.setheading(0)
    tt.width(30)
    tt.down()
    tt.color("yellow")
    tt.speed(16)
    for i in range (25):
        tt.forward(2000)
        tt.right(90)
        tt.forward(30)
        tt.right(90)
        tt.forward(2000)
        tt.left(90)
        tt.forward(30)
        tt.left(90)
    tt.up()
    tt.color("white")
    tt.goto(-200,0)
    tt.write("Retry?",font=("Verdana",100, "normal"))
    tt.hideturtle()
    tt.done()

def get_position_menu(x, y, type_menu):
    """methode pour recuperer la position de la souris
    x: int : position de la souris
    y: int : position de la souris
    type_menu: str : "menu 1" ou "menu 2"

    """
    global POS_X_MENU_1, POS_Y_MENU_1, POS_X_MENU_2, POS_Y_MENU_2, LONGUEUR_MENU, HAUTEUR_MENU
    if x < POS_X_MENU_1 and x > POS_X_MENU_1 - LONGUEUR_MENU and y > POS_Y_MENU_1 and y < POS_Y_MENU_1 + HAUTEUR_MENU:
        bn.choix_do("menu 1", type_menu)
    elif x > POS_X_MENU_2 and x < POS_X_MENU_2 + LONGUEUR_MENU and y > POS_Y_MENU_2 and y < POS_Y_MENU_2 + HAUTEUR_MENU:
        bn.choix_do("menu 2", type_menu)


#methode pour recuperer la position de la souris
def get_position_mouse(afterscreenclik, type_of_click=None, grilles=None, joueur=None):
    """#methode pour recuperer la position de la souris
    args:
        afterscreenclik: str : description de ce que l'on veut faire après le click
        type_of_click: str : type de click (menu, grille)
        grilles: list : liste des grilles
        joueur: str : nom du joueur

    return:
        None

    """
    
    if afterscreenclik == "position_menu":
        tt.onscreenclick(lambda x, y: get_position_menu(x,y, type_of_click))
    else:
        tt.onscreenclick(lambda x, y: print(x, y))

def attente_joueur():
    tt.up()
    tt.reset()
    tt.goto(-350,0)
    tt.write("En atente d'un joueur",font=("Verdana",50, "normal"))

def info_grille():          #Fonction qui marque en bas des grille a quoi elle correspond "Vos Bateau" et "Vos Tirs"
    """fonction qui marque en bas des grille a quoi elle correspond "Vos Bateau" et "Vos Tirs et ne demende rien """
    tt.up()
    tt.goto(-300,-280)
    tt.write("Vos Bateaux",font=("Verdana",10, "normal"))
    tt.goto(280,-280)
    tt.write("Vos Tirs",font=("Verdana",10, "normal"))
    tt.hideturtle()
    
def joueur_tour(le_tour):   #Fonction qui est utilisé dans celle cidessous pour reduir le code
    tt.up()
    tt.goto(-100,350)
    tt.color("blue")
    tt.speed(0)
    tt.down()
    tt.begin_fill()
    tt.goto(-100,260)
    tt.goto(100,260)
    tt.goto(100,350)
    tt.goto(-100,350)
    tt.end_fill()
    tt.goto(-100,300)
    tt.color("black")
    tt.write(le_tour,font=("Verdana",15, "normal"))
    tt.hideturtle()
    
def info_tour(reponse):    #Fonction qui permet de changer l'affichage du tour entre "c'est a vous et "pas a vous" pour indiqué qui dois jouer
    """Fonction qui permet de changer l'affichage du tour entre "c'est a vous et "pas a vous" pour indiqué qui dois jouer en prenant des str "oui" ou "non" et changer la reponse "oui"="c'est a vous" et "non"="pas a vousde jouer" """
    tt.up()
    if reponse=="oui":
        joueur_tour("C'est votre tour")
    elif reponse=="non":
        joueur_tour("pas a vous de jouer")

def get_tir():
    key = tt.textinput("Entrer la casse choissit", "case:")
    return key

"""Valeur mutable importante en pixel et permet de modifier la taille des case du tableau et de toutes les autre fonction graphique du"""
longueur_case = 50

POS_X_MENU_1 = -160
POS_Y_MENU_1 = -100
POS_X_MENU_2 = 90
POS_Y_MENU_2 = -100
LONGUEUR_MENU = 250
HAUTEUR_MENU = 75

choix = [""]

# grille de batteaux
POSE_Y_TABLEAU = -250
POSE_X_TABLEAU = -50

# grille de tir
POSE_Y_TABLEAU_TIR = -250
POSE_X_TABLEAU_TIR = 500






if __name__ == "__main__":

    grille(POSE_X_TABLEAU, POSE_Y_TABLEAU)

    bateau(5, 10)
    croix((44//10)+1,(44%10)+1, "red", POSE_X_TABLEAU, POSE_Y_TABLEAU)
    tt.mainloop()
    

    