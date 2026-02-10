from sys import builtin_module_names
from typing import List
import math
import chars
import random

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
    updatedTiles = set()
    stateBuffer = [[currState[y][x] for x in range(0, width)] for y in range(0, height)]

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
    elif currState[y][x] == chars.fishL:
        fishLsim(x, y, stateBuffer)
    elif currState[y][x] == chars.fishR:
        fishRsim(x, y, stateBuffer)
    elif currState[y][x] == chars.grave:
        gravesim(x, y, stateBuffer)
    elif currState[y][x] == chars.ghost:
        ghostSim(x, y, stateBuffer)

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
    emptyOk=True,
):
    # don't go past edge of screen
    if endX < 0 or endX >= width or endY < 0 or endY >= height:
        return False

    # find tile where we're sswapping
    ch = state[endY][endX]

    # if its empty, move
    if emptyOk and ch == chars.empty:
        state[endY][endX] = char
        state[stY][stX] = chars.empty
        return True

    # otherwise, see if it would move out of the way
    simTile(endX, endY, state)

    # check new tile
    ch = state[endY][endX]
    # if it moved, we can go there
    if emptyOk and ch == chars.empty:
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


def getCh(x: int, y: int, state: List[List[str]]):
    if 0 <= x < width and 0 <= y < height:
        # print(f"x:{x} y:{y} in range")
        return state[y][x]
    # print(f"x:{x} y:{y} out of range")
    return chars.wall


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

    # otherwise do a random left/right
    left = random.randrange(0, 2) == 0
    if left:
        if moveTile(x, y, x - 1, y, chars.water, state):
            return

    if moveTile(x, y, x + 1, y, chars.water, state):
        return

    if not left:
        if moveTile(x, y, x + 1, y, chars.water, state):
            return


def sandSim(x: int, y: int, state: List[List[str]]):
    if y < height - 1:
        if swapTile(x, y, x, y + 1, chars.sand, [chars.water], state):
            return
        if swapTile(x, y, x - 1, y + 1, chars.sand, [chars.water], state):
            return
        if swapTile(x, y, x + 1, y + 1, chars.sand, [chars.water], state):
            return


def fishUpDown(x: int, y: int, char: str, state: List[List[str]]):
    # try to move up/down
    if swapTile(x, y, x, y + 1, char, [chars.water], state, False):
        return True
    if swapTile(x, y, x, y - 1, char, [chars.water], state, False):
        return True
    return False


def fishRsim(x: int, y: int, state: List[List[str]]):

    # try to move vertically if there's an edge of water, or touching fish
    if (
        getCh(x + 1, y, state) == chars.empty
        or getCh(x + 1, y, state) in (chars.fishR, chars.fishL)
        or getCh(x - 1, y, state) in (chars.fishL, chars.fishR)
    ):
        if fishUpDown(x, y, chars.fishR, state):
            return

    # swim foreward
    if swapTile(x, y, x + 1, y, chars.fishR, [chars.water], state, False):
        return

    # try to turn
    if getCh(x - 1, y, state) == chars.water:
        state[y][x] = chars.fishL
        return

    if fishUpDown(x, y, chars.fishL, state):
        return
    # there's no water, so its dead :(
    state[y][x] = chars.grave


def fishLsim(x: int, y: int, state: List[List[str]]):

    # try to swin down if there's an edge of water
    if (
        getCh(x - 1, y, state) == chars.empty
        or getCh(x + 1, y, state) in (chars.fishR, chars.fishL)
        or getCh(x - 1, y, state) in (chars.fishL, chars.fishR)
    ):
        if fishUpDown(x, y, chars.fishR, state):
            return
    # swim foreward
    if swapTile(x, y, x - 1, y, chars.fishL, [chars.water], state, False):
        return

    # try to turn
    if getCh(x + 1, y, state) == chars.water:
        state[y][x] = chars.fishR
        return

    # try to move up/down
    if fishUpDown(x, y, chars.fishR, state):
        return
    # there's no water, so its dead :(
    state[y][x] = chars.grave


def gravesim(x: int, y: int, state: List[List[str]]):

    if swapTile(x, y, x, y + 1, chars.grave, [chars.water], state):
        return

    # become ghost id touching 3 graves
    count = -1 # we will end up counting ourselves
    for cy in range(y-1,y+2):
        for cx in range(x-1,x+2):
            if getCh(cx,cy, state) == chars.grave:
                count+=1
    if count>=3:
        state[y][x] = chars.ghost

def ghostSim(x: int, y: int, state: List[List[str]]):
    # dissapear at top of screen
    if y<=0:
        state[y][x] = chars.empty
        return

    # move up
    state[y][x]= state[y-1][x]
    state[y-1][x] = chars.ghost



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
    elif inp == "Fish":
        currState[mouseY][mouseX] = chars.fishL
    else:
        return

    selected = inp
