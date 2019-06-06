"""Slicing Exercises
Elad Eliav"""


def analyze_number():
    """
    gets number and analyzes
    """
    num = raw_input("Enter num: ")
    diglist = list(num)
    # Create list of ints for the number
    sum_of_digs = sum([int(r) for r in diglist])

    print("You entered: " + num)
    print("The digits: " + ", ".join(diglist))
    print("The sum: " + str(sum_of_digs))


def main():
    """calls analyze_number()"""
    analyze_number()


if __name__ == '__main__':
    main()
