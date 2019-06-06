"""
Elad Eliav Inc.
"""

START_RANGE = 1
END_RANGE = 41

def my_print():
    """prints numbers from 1 to 40"""
    for x in range(START_RANGE, END_RANGE):
        print(x)


def main():
    """
    calls my_print()
    """
    my_print()


if __name__ == '__main__':
    main()
