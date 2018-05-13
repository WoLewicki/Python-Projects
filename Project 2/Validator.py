from re import match


def check_if_can_do_without_palette(dictionary):
    if "Figures" in dictionary:
        figures = dictionary["Figures"]
        for elem in figures:
            if "color" in elem:
                if not match("[a-z]+", elem["color"]) and not match("\(\d{1,3},\d{1,3},\d{1,3}\)", elem["color"]) and \
                        not match("#\d{6}", elem["color"]):
                    return False
                elif match("[a-z]+", elem["color"]):
                    if elem["color"] not in dictionary["Palette"]:
                        return False


def validate_screen(screen):
    if "width" not in screen or "height" not in screen or "bg_color" not in screen or "fg_color" not in screen:
        return False
    if screen["width"] < 1 or screen["height"] < 0:
        return False
    return True


def validate_figure(figure):
    if "type" not in figure:
        return False
    if figure["type"] == "point":
        if "x" not in figure or "y" not in figure:
            return False
        if figure["x"] < 0 or figure["y"] < 0:
            return False
        return True
    elif figure["type"] == "polygon":
        if "points" not in figure:
            return False
        for lista in figure["points"]:
            if len(lista) is not 2:
                return False
            for elem in lista:
                if elem < 0:
                    return False
        return True
    elif figure["type"] == "rectangle":
        if "x" not in figure or "y" not in figure or "width" not in figure or "height" not in figure:
            return False
        if figure["x"] < 0 or figure["y"] < 0 or figure["width"] < 1 or figure["height"] < 0:
            return False
        return True
    elif figure["type"] == "square":
        if "x" not in figure or "y" not in figure or "size" not in figure:
            return False
        if figure["x"] < 0 or figure["y"] < 0 or figure["size"] < 0:
            return False
        return True
    elif figure["type"] == "circle":
        if "x" not in figure or "y" not in figure or "radius" not in figure:
            return False
        if figure["x"] < 0 or figure["y"] < 0 or figure["radius"] < 1:
            return False
        return True
    else:
        return False
