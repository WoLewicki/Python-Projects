import json
import Figures
from Painter import Paint
import Validator as valid
import sys


def get_json(json_filename):
    with open(json_filename) as json_file:
        return json.load(json_file)


def main():
    input_file = ""
    output = ""
    arguments = sys.argv
    for index, elem in enumerate(arguments):
        if elem == '-o' or elem == '--output':
            if index < len(arguments) - 1:
                output = arguments[index+1]
            else:
                print("Didn't pass output name after flag.")
                return
        elif input_file == "" and index != 0 and arguments[index-1] != '-o' and arguments[index-1] != '--output':
            input_file = elem
    if input == "":
        print("Didn't pass input name in arguments")
        return
    json_dict = get_json(input_file)  # getting dictionary from json input file
    if not json_dict:
        print("Couldn't get dict from json.")
        return
    if "Screen" not in json_dict:
        print("Didn't pass screen values in json.")
        return
    if not valid.validate_screen(json_dict):
        print("Wrong screen parameters passed")
        return
    palette = {}
    if "Palette" in json_dict:
        palette = json_dict["Palette"]
    else:
        if not valid.check_if_can_do_without_palette(json_dict):
            print("Didn't pass palette and it was needed.")
            return
    screen = json_dict["Screen"]
    default_color = screen["fg_color"]
    figures = json_dict["Figures"]
    drawings = []

    collector = {"point": Figures.Point, "polygon": Figures.Polygon, "rectangle": Figures.Rectangle,
                 "square": Figures.Square, "circle": Figures.Circle}
    for elem in figures:
        if not valid.validate_figure(elem):
            print("Wrong figure semantics.")
            return
        copy = elem.copy()
        del copy["type"]
        if "color" not in copy:
            copy["color"] = default_color
        obj = collector[elem["type"]](copy)
        drawings.append(obj)

    paint_all = Paint(screen, drawings, palette)
    paint_all.draw_all()
    if output is not "":
        paint_all.save(output)


if __name__ == '__main__':
    main()
