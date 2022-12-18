import turtle

def get_pseudo():

    key = turtle.textinput("Enrer votre Pseudo", "Pseudo:")
    return key

if __name__ == "__main__":
    print(get_pseudo())
    turtle.exitonclick()
