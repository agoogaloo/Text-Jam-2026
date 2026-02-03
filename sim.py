from sys import builtin_module_names
from typing import List
import math
import chars

width = 50
height = 20

brushType = "place"
selected = "Delete"
mouseX = int(width / 2)
mouseY = int(height / 2)

currState = [[" " for i in range(0, width)] for y in range(0, height)]
updatedTiles = set()


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

    if brushType == "stream":
        place(selected)

    for y in range(0, height):
        for x in range(0, width):
            simTile(x, y, stateBuffer)

    currState = stateBuffer


def simTile(x: int, y: int, stateBuffer: List[List[str]]):
    if (x, y) in updatedTiles:
        return

    updatedTiles.add((x, y))

    if currState[y][x] == chars.sand:
        sandSim(x, y, stateBuffer)
    elif currState[y][x] == chars.water:
        waterSim(x, y, stateBuffer)

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
    if endX < 0 or endX >= width or endY < 0 or endY >= height:
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


def swapTile(
    stX: int,
    stY: int,
    endX: int,
    endY: int,
    char: str,
    swapTypes: List[str],
    state: List[List[str]],
):
    # don't go past edge of screen
    if endX < 0 or endX >= width or endY < 0 or endY >= height:
        return False

    # find tile where we're sswapping
    ch = state[endY][endX]

    # if its empty, move
    if ch == chars.empty:
        state[endY][endX] = char
        state[stY][stX] = chars.empty
        return True

    # otherwise, see if it would move out of the way
    simTile(endX, endY, state)

    # check new tile
    ch = state[endY][endX]
    # if it moved, we can go there
    if ch == chars.empty:
        state[endY][endX] = char
        state[stY][stX] = chars.empty
        return True

    # otherwise we can swap
    if ch in swapTypes:
        state[stY][stX] = ch
        state[endY][endX] = char
        updatedTiles.add((endX, endY))
        return True

    # otherwise we can't
    return False


def waterSim(x: int, y: int, state: List[List[str]]):

    # try to fall
    if moveTile(x, y, x, y + 1, chars.water, state):
        return

    canLeft = True
    canRight = True
    dist = 1
    # can fall off any ledge within 3 tiles
    while dist <= 3 and (canLeft or canRight):
        canLeft = canLeft and 0 <= x - dist and state[y][x - dist] == chars.empty
        canRight = canRight and x + dist < width and state[y][x + dist] == chars.empty
        if canLeft and moveTile(x, y, x - dist, y + 1, chars.water, state):
            return

        if canRight and moveTile(x, y, x + dist, y + 1, chars.water, state):
            return

        dist += 1

    # see if it should get pushed by water above
    if y > 0 and state[y - 1][x] == chars.water:
        dist = 1
        canLeft = True
        canRight = True
        while canLeft or canRight:
            if canLeft and moveTile(x, y, x - dist, y, chars.water, state):
                return

            if canRight and moveTile(x, y, x + dist, y, chars.water, state):
                return

            canLeft = canLeft and 0 <= x - dist and state[y][x - dist] == chars.water
            canRight = (
                canRight and x + dist < width and state[y][x + dist] == chars.water
            )
            dist += 1


def sandSim(x: int, y: int, state: List[List[str]]):
    if y < height - 1:
        if swapTile(x, y, x, y + 1, chars.sand, [chars.water], state):
            return
        if swapTile(x, y, x - 1, y + 1, chars.sand, [chars.water], state):
            return
        if swapTile(x, y, x + 1, y + 1, chars.sand, [chars.water], state):
            return


def input(inp: str):
    global mouseY
    global mouseX
    global currState
    global brushType

    if inp == "up":
        mouseY = max(0, mouseY - 1)
    elif inp == "down":
        mouseY = min(height - 1, mouseY + 1)
    elif inp == "left":
        mouseX = max(0, mouseX - 1)
    elif inp == "right":
        mouseX = min(width - 1, mouseX + 1)
    elif inp == "Reset":
        currState = [[" " for i in range(0, width)] for y in range(0, height)]
    elif inp == "Stream":
        brushType = "stream"
    elif inp == "Place":
        brushType = "place"
    else:
        place(inp)


def place(inp: str):
    global selected

    if inp == "Sand":
        currState[mouseY][mouseX] = chars.sand
    elif inp == "Water":
        currState[mouseY][mouseX] = chars.water
    elif inp == "Delete":
        currState[mouseY][mouseX] = chars.empty
    elif inp == "Block":
        currState[mouseY][mouseX] = chars.wall
    else:
        return

    selected = inp
