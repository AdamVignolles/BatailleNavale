import turtle

#methode pour recuperer la position de la souris
def get_position_mouse():
    return turtle.onscreenclick(lambda x, y: print((x, y)))

get_position_mouse()
turtle.mainloop()


