import turtle

def get_position_case(x, y):
    # On récupère la position de la case
    x = int((x - POSE_X_TABLEAU) // TAILLE_CASE)
    y = int((y - POSE_Y_TABLEAU) // TAILLE_CASE)
    return x, y

#methode pour recuperer la position de la souris
def get_position_mouse():
    pos = turtle.onscreenclick(lambda x, y: print((x, y)))
    if pos != None:
        return get_position_case(pos[0], pos[1])
    




click = get_position_mouse()
POSE_Y_TABLEAU = 0
POSE_X_TABLEAU = 0
TAILLE_CASE = 50
print(click)
turtle.mainloop()