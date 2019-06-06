import math

from shp import Shape


# new Rectangle class the extends Shape
class Rectangle(Shape):
    # Constructor
    def __init__(self, color, a=0, b=0):
        super(Rectangle, self).__init__(color, a * b, 2 * a + 2 * b)

    # + operator overloads
    def __add__(self, other):
        if isinstance(other, Rectangle) or isinstance(other, Square):
            new_rect = Rectangle(self.color)
            new_rect.perimeter = self.perimeter + other.perimeter
            new_rect.area = self.area + other.area
            return new_rect
        raise Exception("Can't add object of type " + other.__class__.__name__)

    def __radd__(self, other):
        return self + other


# Square class extends Shape
class Square(Shape):
    # Constructor
    def __init__(self, color, a=0):
        super(Square, self).__init__(color, a ** 2, 4 * a)

    # + overloading
    def __add__(self, other):
        if isinstance(other, Square):
            new_obj = Square
        elif isinstance(other, Rectangle):
            new_obj = Rectangle
        else:
            raise Exception("Can't add object of type " + other.__class__.__name__)

        new_rect = new_obj(self.color)
        new_rect.perimeter = self.perimeter + other.perimeter
        new_rect.area = self.area + other.area
        return new_rect

    def __radd__(self, other):
        return self + other


# Circle class extends Shape
class Circle(Shape):
    # constructor
    def __init__(self, color, radius):
        _area = math.pi * radius ** 2
        _perimeter = math.pi * radius * 2
        super(Circle, self).__init__(color, _area, _perimeter)
