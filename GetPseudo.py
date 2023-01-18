import turtle

def get_pseudo():

    key = turtle.textinput("Entrer le code du serveur(port)", "Code:")
    return key

if __name__ == "__main__":
    print(get_pseudo())
    turtle.exitonclick()
