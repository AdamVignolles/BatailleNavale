#gzet key pressed with turtle and write it on the screen
import turtle

def get_pseudo():

    key = turtle.textinput("Enrer votre Pseudo", "Pseudo:")
    return key

print(get_pseudo())
turtle.exitonclick()
