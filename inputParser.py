import chars
import sim

mode = "norm"

commands = {
    "norm": {
        "e": "Edit Mode",
        "b": "Brush Mode",
        "s": "Sys Mode",
        "p": "Pause",
    },
    "brush": {
        "s": "Stream",
        "p": "Place",
        "e": "Edit Mode",
        "esc": "Norm Mode",
    },
    "sys": {
        "q": "Quit",
        "s": "Save",
        "l": "Load",
        "r": "Reset",
        "k": "Sim spd+",
        "j": "Sim spd-",
        "c": "Term Clear",
        "esc": "Norm Mode",
    },
    "edit": {
        " ": "Block",
        "w": "Water",
        "s": "Sand",
        "f": "Fish",
        "d": "Delete",
        "h": "left",
        "l": "right",
        "k": "up",
        "j": "down",
        "b": "Brush Mode",
        "esc": "Norm Mode",
    },
}


def parseInput(inChar: str):
    global mode
    if inChar in commands[mode]:
        comm = commands[mode][inChar]
        if comm == "Stream" or comm == "Place":
            mode = "edit"

        if comm == "Edit Mode":
            mode = "edit"
        elif comm == "Sys Mode":
            mode = "sys"
        elif comm == "Norm Mode":
            mode = "norm"
        elif comm == "Brush Mode":
            mode = "brush"
        else:
            return comm

    return "Draw"


def getControls():
    img = ["--== " + mode.upper() + " MODE ==--"]
    if mode == "brush":
        img.append("Brush: " + sim.brushType)

    if mode == "edit":
        img.append("Brush: " + sim.brushType)
        img.append(chars.cursor + " | Cursor | hjkl/Arrows")
        img.append(chars.empty + " | Empty  | d")
        img.append(chars.wall + " | Wall   | Space")
        img.append(chars.sand + " | Sand   | s")
        img.append(chars.water + " | Water  | w")
        img.append(chars.fishL + " | Fish   | f")
        img.append("  | Brush  | b")
        img.append("  | Norm   | esc")
    else:
        for k, desc in commands[mode].items():
            img.append(f"{k:3}| {desc}")
    return img
