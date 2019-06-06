"""
Elad Eliav Inc.
"""

START = 1
END = 101
NUM = 7


def is_digit_in_num(digit, num):
    """
    function that returns true if the given digit
    """
    while num > 0:
        if digit == num % 10:
            return True
        else:
            num /= 10
    return False


def print_all_with_7(start, end, num):
    """
       prints all the numbers from start to end if they
       are divisible by num or have a num in them
    """
    for x in range(start, end):
        if x % num == 0 or is_digit_in_num(num, x):
            print(x)


def main():
    """
    calls print_all_with with START, END, NUM
    :return:
    """
    print_all_with_7(START, END, NUM)


if __name__ == '__main__':
    main()
