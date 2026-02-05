import enum
from os.path import exists
import chars as ch
import sim
import inputParser as inp

title = "SAND SIMULATOR!"
shouldClear = True
paused = False

screenWidth = sim.width
screenHeight = sim.height

screen = [" " * screenWidth] * screenHeight

savePath = "simSave.txt"


def clearScreen():
    global screen
    screen = [" " * screenWidth] * screenHeight


def drawScreen(clear=False):
    # go back to top of screen

    # print((" " * (screenWidth + 3) + "\n") * 2, flush=True)
    if clear:
        print("\033[2J")
        print("\033[F" * 20, end="")
        print("\033[F\033[2K" * (screenHeight), end="")

    print("\n    --==" + title + "==--   ")
    print(ch.tlCorn + (ch.hLine * screenWidth) + ch.trCorn)

    height = 0
    controls = inp.getControls()
    for i in screen:
        i = i[0:screenWidth]
        contLine = ""
        if height < len(controls):
            contLine = " " + controls[height]

        print(ch.vLine + i + ch.vLine + contLine)
        height += 1

    print(ch.blCorn + (ch.hLine * screenWidth) + ch.brCorn)
    # print("x:" + (str)(sim.mouseX) + " y:" + (str)(sim.mouseY))
    # print((" " * (screenWidth + 3) + "\n") * 2, flush=True)

    clearScreen()


def draw(stringArr, drawX: int, drawY: int, target):
    # crop image to not go off left of screen
    if drawX < 0:
        # make a copy so we don't break the original when trimming
        strCopy = [""] * len(stringArr)
        for i in range(len(strCopy)):
            strCopy[i] = stringArr[i][-drawX::]
        drawX = 0
        stringArr = strCopy
    # figure out how to set 1 character of string???
    # for y in range(len(stringArr)):
    #     for x in range(len(stringArr)):
    #         screen[drawY+y][drawX+x] = stringArr[y][x]
    for y in range(len(stringArr)):
        if drawY + y >= len(target) or drawX > screenWidth:
            return
        if drawY + y < 0:
            continue

        line = target[drawY + y]
        target[drawY + y] = (
            line[0:drawX] + stringArr[y] + line[drawX + len(stringArr[y]) : :]
        )


def render():
    # draw(["-="+title+"=-"], 2,0, screen)
    draw(sim.getTextImg(), 0, 0, screen)
    draw([ch.cursor], sim.mouseX, sim.mouseY, screen)
    drawScreen(shouldClear)
    return


def simulate():
    if paused:
        return
    sim.simulate()
    render()


def input(com: str):
    global shouldClear
    global path
    global paused
    global textIn

    if com == "Pause":
        paused = not paused
    elif com == "Save":
        save()
    elif com == "Load":
        load(savePath)

    elif com == "Term Clear":
        shouldClear = not shouldClear
    else:
        sim.input(com)
        render()

def load(file:str):
    if not exists(file):
        return

    contents = open(file).read().split("\n")
    simState = []
    for line in contents:
        l = []
        for char in line:
            l.append(char+"")
        simState.append(l)

    sim.currState = simState

    


def save():
    contents = ""
    for line in sim.currState:
        for ch in line:
            contents += ch
        contents += "\n"

    with open(savePath, "wt")  as file:
        file.write(contents)


