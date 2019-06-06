"""
Elad Eliav Inc.
"""

START = 1
END = 10000

def f(n):
    """
    generates a fibonacci number based on the given n
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return f(n - 1) + f(n - 2)


def sub_fib(startNumber, endNumber):
    """
    generates a fibonacci series from the range given
    """
    n = 0
    cur = f(n)
    while cur <= endNumber:
        if startNumber <= cur:
            print(cur)
        n += 1
        cur = f(n)


def main():
    """
    prints a fibonacci series from 1 to 10000
    """
    sub_fib(START, END)


if __name__ == '__main__':
    main()
