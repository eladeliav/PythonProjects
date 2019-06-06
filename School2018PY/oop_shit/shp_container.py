from random import randint

from shapes import *


# Wrapper object that holds an array of Shapes
class ShapeContainer(object):
    # const dics for colors, shape types, and num of params required for shapes
    COLORS = {0: "White", 1: "Red", 2: "Green", 3: "Blue", 4: "Yellow", 5: "Brown", 6: "LightBlue",
              7: "DarkBlue",
              8: "Orange", 9: "LightGray", 10: "Gray"}

    RAND_SHAPES = {0: Shape, 1: Rectangle, 2: Square, 3: Circle}
    PARAMS_DICT = {Shape: 2, Rectangle: 2, Square: 1, Circle: 1}

    # constructor
    def __init__(self):
        self.a = []

    # generates random shapes into self.a
    def generate(self, num):
        self.a = []
        for _ in range(num):
            params_lst = []
            current_shape = ShapeContainer.RAND_SHAPES[randint(1, len(ShapeContainer.RAND_SHAPES) - 1)]
            current_color = ShapeContainer.COLORS[randint(0, len(ShapeContainer.COLORS) - 1)]
            num_of_params = ShapeContainer.PARAMS_DICT[current_shape]
            for _ in range(num_of_params):
                params_lst.append(randint(0, 10))
            self.a.append(current_shape(current_color, *params_lst))

    # sums perimeter
    def sum_perimeter(self):
        return sum([x.perimeter for x in self.a])

    # sums areas
    def sum_area(self):
        return sum([x.area for x in self.a])

    # counts different shapes with colors into dict
    def count_color(self):
        count_colors = {}
        for obj in self.a:
            current_color = obj.color
            count_colors[current_color] = count_colors.get(current_color, 0) + 1
        return count_colors
