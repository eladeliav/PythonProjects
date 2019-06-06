"""
Elad Eliav Inc.
"""

START_RANGE = 1
INCREMENTER = 1
END_RANGE = 41


def my_print():
    """prints number from 1 to 40 using a while loop"""
    x = START_RANGE
    while x < END_RANGE:
        print(x)
        x += INCREMENTER


def main():
    """
    calls my_print()
    """
    my_print()


if __name__ == '__main__':
    main()
