import time
from threading import Thread

from pynput import keyboard

import game
import inputParser as inpParse


run = True
simDelay = 0.5
def on_press(key):
    global game
    global run
    global simDelay
    inp = ""
    try:
        inp = key.char
    except AttributeError:
        if key == keyboard.Key.up:
            inp = "k"
        elif key == keyboard.Key.down:
            inp = "j"
        elif key == keyboard.Key.left:
            inp = "h"
        elif key == keyboard.Key.right:
            inp = "l"
        elif key == keyboard.Key.esc:
            inp = "esc"
        elif key == keyboard.Key.space:
            inp = " "

    
    inp = inpParse.parseInput(inp)
    print("state:"+inpParse.mode)
    print("Com:"+inp)
    if inp == "Sim spd-":
        simDelay*=1.25;
    elif inp == "Sim spd+":
        simDelay/=1.25;
    elif inp == "Quit":
        run = False
        quit()

    elif inp != "None":
        time.sleep(0.0005)
        game.input(inp)



listner = keyboard.Listener(on_press=on_press)
listner.start()


while run:
    game.simulate()
    time.sleep(simDelay)






