"""
Elad Eliav
"""

END = 5
JUMPS = 1


def print_range(end, jumps):
    """
    prints numbers in range every 0.1
    """
    end_proper = (end * 10) + jumps
    for num in (x / 10.0 for x in xrange(end_proper)):
        if num - int(num) == 0:
            print(int(num))
        else:
            print(num)


def main():
    """calls printRange()"""
    print_range(END, JUMPS)


if __name__ == '__main__':
    main()
