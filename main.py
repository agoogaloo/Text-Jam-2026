import time
from threading import Thread

from pynput import keyboard

import game


run = True
def on_press(key):
    global game
    global run
    inp = ""
    try:
        if key.char == "k":
            inp = "u"
        elif key.char == "j":
            inp = "d"
            print("SSSS")
        elif key.char == "h":
            inp = "l"
        elif key.char == "l":
            inp = "r"
        elif key.char == "w":
            inp = "water"
        elif key.char == "s":
            inp = "sand"
        elif key.char == "d":
            inp = "delete"
    except AttributeError:
        if key == keyboard.Key.up:
            inp = "u"
        elif key == keyboard.Key.down:
            inp = "d"
        elif key == keyboard.Key.left:
            inp = "l"
        elif key == keyboard.Key.right:
            inp = "r"
        elif key == keyboard.Key.esc:
            inp = "exit"
            run = False
            exit()
        elif key == keyboard.Key.space:
            inp = "wall"

    if inp != "":
        time.sleep(0.0001)
        game.input(inp)



listner = keyboard.Listener(on_press=on_press)
listner.start()

simDelay = 0.5

while run:
    game.simulate()
    time.sleep(simDelay)






