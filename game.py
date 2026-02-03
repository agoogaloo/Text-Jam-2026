import chars as ch
import sim


title = "SAND!!!"

screenWidth =sim.width
screenHeight =sim.height 

screen = [" " * screenWidth] * screenHeight


def clearScreen():
    global screen
    screen = [" " * screenWidth] * screenHeight


def drawScreen(clear=False):
    # go back to top of screen

    # print((" " * (screenWidth + 3) + "\n") * 2, flush=True)
    if clear:
        print("\033[F" *  3, end="")
        print("\033[F\033[2K" * (screenHeight ), end="")

    print("    --=="+title+"==--   ")
    print(ch.tlCorn + (ch.hLine * screenWidth) + ch.trCorn)
    for i in screen:
        i = i[0:screenWidth]
        print(ch.vLine + i + ch.vLine)
    print(ch.blCorn + (ch.hLine * screenWidth) + ch.brCorn)
    print("* - sand | "+ch.cursor+" - selection")
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
    draw(sim.getTextImg(), 0,0, screen)
    draw([ch.cursor], sim.mouseX, sim.mouseY, screen)
    # drawScreen(True)
    drawScreen(False)
    return


def simulate():
    sim.simulate()
    render()


def input(inp: str):
    if(inp=="q"):
        exit()
    sim.input(inp)

    render()

