from sys import builtin_module_names
from typing import List
import chars

width = 20
height = 8

mouseX = int(width / 2)
mouseY = int(height / 2)

currState = [[" " for i in range(0, width)] for y in range(0, height)]
updatedTiles = set()

currState[0][0] = chars.sand
currState[0][2] = chars.sand
currState[1][2] = chars.sand
currState[2][2] = chars.sand
currState[3][2] = chars.sand
currState[0][3] = chars.sand


def getTextImg():
    res = []
    for y in currState:
        line = ""
        for x in y:
            line += x
        res.append(line)

    return res


def simulate():
    global currState
    global updatedTiles
    stateBuffer = [[currState[y][x] for x in range(0, width)] for y in range(0, height)]
    updatedTiles = set()

    for y in range(0, height):
        for x in range(0, width):
            simTile(x, y, stateBuffer)

    currState = stateBuffer


def simTile(x: int, y: int, stateBuffer: List[List[str]]):
    updateStr = "x" + str(x) + "y" + str(y)
    if updateStr in updatedTiles:
        return

    if currState[y][x] == chars.sand:
        sandSim(x, y, stateBuffer)

    updatedTiles.add(updateStr)
    return


def moveTile(
    sx: int,
    sy: int,
    endX: int,
    endY: int,
    char: str,
    state: List[List[str]],
    replacechar=chars.empty,
):
    if endX < 0 or endX > width or endY < 0 or endY > height:
        return False

    if state[endY][endX] == chars.empty:
        state[endY][endX] = char
        state[sy][sx] = replacechar
        return True

    simTile(endX, endY, state)

    if state[endY][endX] == chars.empty:
        state[endY][endX] = char
        state[sy][sx] = replacechar
        return True
    return False


def sandSim(x: int, y: int, state: List[List[str]]):
    if y < height - 1:

        if moveTile(x, y, x, y + 1, chars.sand, state):
            return
        if moveTile(x, y, x - 1, y + 1, chars.sand, state):
            return
        if moveTile(x, y, x + 1, y + 1, chars.sand, state):
            return


def input(inp: str):
    global mouseY
    global mouseX
    global currState

    if inp == "u":
        mouseY = max(0, mouseY - 1)
    elif inp == "d":
        mouseY = min(height - 1, mouseY + 1)
    elif inp == "l":
        mouseX = max(0, mouseX - 1)
    elif inp == "r":
        mouseX = min(width - 1, mouseX + 1)
    elif inp == "sand":
        currState[mouseY][mouseX] = chars.sand
