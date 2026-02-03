import time
from threading import Thread

from pynput import keyboard

import game


def on_press(key):
    global game
    inp = ""
    try:
        if key.char == "w":
            inp = "u"
        elif key.char == "s":
            inp = "d"
            print("SSSS")
        elif key.char == "a":
            inp = "l"
        elif key.char == "d":
            inp = "r"
        elif key.char == " ":
            inp = "sand"
        elif key.char == "r":
            inp = "x"
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
            inp = "e"
        elif key == keyboard.Key.space:
            inp = "sand"

    if inp != "":
        time.sleep(0.0001)
        game.input(inp)



listner = keyboard.Listener(on_press=on_press)
listner.start()

simDelay = 0.5
while True:
    game.simulate()
    time.sleep(simDelay)






