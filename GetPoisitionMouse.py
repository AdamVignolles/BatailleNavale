import turtle
import partie_graphique as gr

def get_position_case(x, y):
    # On récupère la position de la case
    x = int((x - POSE_X_TABLEAU) // TAILLE_CASE)
    y = int((y - POSE_Y_TABLEAU) // TAILLE_CASE)
    return x, y

#methode pour recuperer la position de la souris
def get_position_mouse():
    pos = turtle.onscreenclick(lambda x, y: print((x, y)))
    if pos != None:
        return (int(abs(float(pos[0]))), int(abs(float(pos[1]))))
    




click = get_position_mouse()
POSE_Y_TABLEAU = 0
POSE_X_TABLEAU = 0
TAILLE_CASE = 50
print(click)
gr.grille(0, 0)
turtle.mainloop()