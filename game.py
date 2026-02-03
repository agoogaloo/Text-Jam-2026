import chars as ch
import sim

title = "SAND SIMULATOR!"

screenWidth = sim.width
screenHeight = sim.height

screen = [" " * screenWidth] * screenHeight

controls = [
    "--==Controls==--",
    ch.cursor + " | Cursor | hjkl/Arrows",
    ch.empty + " | Empty  | d",
    ch.wall + " | Wall   | Space",
    ch.sand + " | Sand   | s",
    ch.water + " | Water  | w",
    "  | Quit   | Esc/^C",
]


def clearScreen():
    global screen
    screen = [" " * screenWidth] * screenHeight


def drawScreen(clear=False):
    # go back to top of screen

    # print((" " * (screenWidth + 3) + "\n") * 2, flush=True)
    if clear:
        print("\033[1J")

        # print("\033[F" * 6, end="")
        # print("\033[F\033[2K" * (screenHeight), end="")

    print("\n\n    --==" + title + "==--   ")
    print(ch.tlCorn + (ch.hLine * screenWidth) + ch.trCorn)

    height = 0
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
    drawScreen(True)
    # drawScreen(False)
    return


def simulate():
    sim.simulate()
    render()


def input(inp: str):
    if inp == "exit":
        quit()
    sim.input(inp)

    render()
