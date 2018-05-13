

class Point:
    """Point type object"""
    def __init__(self, dictionary):
        self.x = dictionary["x"]
        self.y = dictionary["y"]
        self.color = dictionary["color"]

    def __str__(self):
        return [self.x, self.y, self.color]


class Polygon:
    """"Polygon type object"""
    def __init__(self, dictionary):
        self.points = dictionary["points"]
        self.color = dictionary["color"]

    def __str__(self):
        return [self.points, self.color]


class Rectangle:
    """Rectangle type object"""
    def __init__(self, dictionary):
        self.x = dictionary["x"]
        self.y = dictionary["y"]
        self.width = dictionary["width"]
        self.height = dictionary["height"]
        self.color = dictionary["color"]

    def __str__(self):
        return [self.x, self.y, self.width, self.height, self.color]


class Square:
    """Square type object"""
    def __init__(self, dictionary):
        self.x = dictionary["x"]
        self.y = dictionary["y"]
        self.size = dictionary["size"]
        self.color = dictionary["color"]

    def __str__(self):
        return [self.x, self.y, self.size, self.color]


class Circle:
    """Circle type object"""
    def __init__(self, dictionary):
        self.x = dictionary["x"]
        self.y = dictionary["y"]
        self.radius = dictionary["radius"]
        self.color = dictionary["color"]

    def __str__(self):
        return [self.x, self.y, self.radius, self.color]