from shp_container import *


def main():
    """
    Tests out some shapecontainer functions
    """
    my_cont = ShapeContainer()
    my_cont.generate(100)
    print "Total area: " + str(my_cont.sum_area())
    print "Total perimeter: " + str(my_cont.sum_perimeter())
    print "Colors: " + str(my_cont.count_color())


if __name__ == "__main__":
    main()
