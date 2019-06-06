class Shape(object):
    # constructor
    def __init__(self, color, area, perimeter):
        self._color = color
        self._area = area
        self._perimeter = perimeter

    # getters and setters
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        self._area = area;

    @property
    def perimeter(self):
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter):
        self._perimeter = perimeter

    # to string
    def __str__(self):
        return "Shape type: " + self.__class__.__name__ + ", Color: " + \
               self._color + ", Area: " + str(self._area) + ", Perimeter: " + str(self.perimeter)
