"""
Elad Eliav Inc.
"""


def calculator(num1, operation, num2):
    """calculates the answer from the given numbers and operation"""
    result = eval("{} {} {}".format(num1, operation, num2))
    # runs in python console num1 opeator num2 with .format and saves the answer in result
    print("{} {} {} = {}".format(num1, operation, num2, result))


def get_numbers():
    """gets two floats and an operation"""
    num1 = float(raw_input("Give me the first number"))
    operation = str(raw_input("What is the operator?"))
    num2 = float(raw_input("Give me the second number"))

    return num1, operation, num2


def main():
    """uses get_numbers() to receive input for num1, operation and num2 then calculate and print the result"""
    num1, operation, num2 = get_numbers()
    calculator(num1, operation, num2)


if __name__ == '__main__':
    main()
