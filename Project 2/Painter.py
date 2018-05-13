import Figures as F
from PIL import Image, ImageDraw


class Paint:

    def __init__(self, screen, figures, palette):
        self.screen = screen
        self.figures = figures
        self.palette = palette
        self.image = Image.new('RGB', (self.screen["width"], self.screen["height"]),
                               Paint.convert_color(self.palette, self.screen["bg_color"]))

    def draw_all(self):
        for figure in self.figures:
            d = ImageDraw.Draw(self.image)
            self.draw_figure(figure, d)
        self.image.show()

    def draw_figure(self, obj, d):
        if isinstance(obj, F.Point):
            self.draw_point(obj, d)
        elif isinstance(obj, F.Polygon):
            self.draw_polygon(obj, d)
        elif isinstance(obj, F.Rectangle):
            self.draw_rectangle(obj, d)
        elif isinstance(obj, F.Square):
            self.draw_square(obj, d)
        elif isinstance(obj, F.Circle):
            self.draw_circle(obj, d)

    def draw_point(self, obj, d):
        d.point([obj.x, obj.y], self.convert_color(self.palette, obj.color))

    def draw_polygon(self, obj, d):
        points = [tuple(x) for x in obj.points]
        d.polygon(points, self.convert_color(self.palette, obj.color))

    def draw_rectangle(self, obj, d):
        points = [(obj.x - obj.width/2, obj.y + obj.height/2), (obj.x + obj.width/2, obj.y - obj.height/2)]
        d.rectangle(points, self.convert_color(self.palette, obj.color))

    def draw_square(self, obj, d):
        points = [(obj.x - obj.size/2, obj.y + obj.size/2), (obj.x + obj.size/2, obj.y - obj.size/2)]
        d.rectangle(points, self.convert_color(self.palette, obj.color))

    def draw_circle(self, obj, d):
        points = [(obj.x - obj.radius, obj.y + obj.radius), (obj.x + obj.radius, obj.y - obj.radius)]
        d.ellipse(points, self.convert_color(self.palette, obj.color))

    @staticmethod
    def convert_color(palette, color):
        def convert_to_image_input_type(unready):
            if unready == "\(\d{1,3},\d{1,3},\d{1,3}\)":
                unready = unready[1:-1]
                return tuple([int(x) for x in unready.split(",")])
            elif unready == "#\d{6}":
                return tuple([int(unready[1:3], 16), int(unready[3:5], 16), int(unready[5:], 16)])
            else:
                return unready  # it is actually already good color format
        if color in palette:
            return convert_to_image_input_type(palette[color])
        else:
            return convert_to_image_input_type(color)
