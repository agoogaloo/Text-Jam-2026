import chars

mode = "norm"

commands = {
    "norm": {
        "e": "Edit Mode",
        "s": "Sys Mode",
    },
    "sys": {
        "q": "Quit",
        "s": "Save",
        "c": "Term Clear",
        "r": "Reset",
        "k": "Sim spd+",
        "j": "Sim spd-",
        "esc": "Norm Mode",
    },
    "edit": {
        " ": "Block",
        "w": "Water",
        "s": "Sand",
        "d": "Delete",
        "h": "left",
        "l": "right",
        "k": "up",
        "j": "down",
        "esc": "Norm Mode",
    },
}


def parseInput(inChar: str):
    global mode
    if inChar in commands[mode]:
        comm = commands[mode][inChar]
        if comm == "Edit Mode":
            mode = "edit"
        elif comm == "Sys Mode":
            mode = "sys"
        elif comm == "Norm Mode":
            mode = "norm"
        else:
            return comm

    return "Draw"


def getControls():
    img = ["--== " + mode.upper() + " MODE ==--"]
    if mode == "edit":
        img.append(chars.cursor + " | Cursor | hjkl/Arrows")
        img.append(chars.empty + " | Empty  | d")
        img.append(chars.wall + " | Wall   | Space")
        img.append(chars.sand + " | Sand   | s")
        img.append(chars.water + " | Water  | w")
        img.append("  | Norm   | esc")
    else:
        for k, desc in commands[mode].items():
            img.append(f'{k:3}| {desc}')
    return img
