#Programé par Lenny Cohen 1G5

import turtle as tt
tt.hideturtle()

"""Valeur mutable importante en pixel et permet de modifier la taille des case du tableau et de toutes les autre fonction graphique du"""
longueur_case = 50



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
    

def get_position_mouse():
    return tt.onscreenclick(lambda x, y: print((x, y)))      #Permet d'obtenir la position de l'endroit ou a clicker l'utilisateur

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
    tt.up()
 
def croix (x,y,color) :                               #Crée une croix avec comme millieux les coordonné (x,y) et prend comme autre argument la couleur de la croix 
    tt.up()
    tt.goto(0,0)
    tt.down()
    tt.setheading(0)
    tt.color(color)
    tt.speed(0)
    tt.right(45)
    for i in range (4): 
        tt.forward(0.7*longueur_case)
        tt.backward(0.7*longueur_case)
        tt.right(90)
    tt.color("black")
    tt.hideturtle()
    
def bateau(x,y,ori,taille) :                        #crée un bateau de "taille"(a entré dans la fonction) cases de longueur et de 1 de largeur ,prend comme coordonné (x,y) le millieux du bateau et ori est égal a l'orientation soit "vertical" ou "horrizontale" et return false si quelque chose d'autre est inseré 
    if ori=="vertical": ori=90
    elif  ori =="horrizontale" : ori=0
    else : return False
    tt.up()
    tt.color("gray")
    tt.speed(0)
    tt.setheading(0)
    tt.goto(x,y)
    tt.left(ori)
    tt.backward(longueur_case/10*3*taille)
    tt.begin_fill()
    tt.right(90)
    tt.down()
    tt.forward(longueur_case/10*3)
    tt.left(90)
    tt.forward(longueur_case/5*3*taille)
    tt.circle(longueur_case/10*3,180)
    tt.forward(longueur_case/5*3*taille)
    tt.left(90)
    tt.forward(longueur_case/10*3)
    tt.end_fill()
    tt.color("black")
    tt.hideturtle()

def get_code():                           #Permet d'obtenir le code pour le port multijoueur

    key = tt.textinput("Entrer le code du serveur(port)", "Code:")
    return key  
    
def menu_selection(name,name1,name2) :
    tt.reset()                            #marque les trois donné inserét dans la fonction avec name (au centre haut ),name1(plus bas a gauche) ,name2(méme hauteur que name1 mais a droite);(sera utilisé pour les menu de selection )
    tt.up()
    tt.goto(-200,100)
    tt.write(name,font=("Verdana",50, "normal"))
    tt.goto(-250,-100)
    tt.write(name1,font=("Verdana",50, "normal"))
    tt.goto(100,-100)
    tt.write(name2,font=("Verdana",50, "normal"))
    tt.hideturtle()  
    
def partie_perdu() :                                       #fonction lorsque que la partie est perdu  , écris "Loose" puis un "retry" sous un fond noir 
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
    
    
def partie_gagnee():                                    #Meme fonction que celuit pour la partie gagné mais marque win puis retry sous un fond jaune 
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
    
    
    
    