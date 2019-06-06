"""
Elad Eliav Inc.
"""


def printBusinessCard():
    """receives name, school and class then prints it out like a business card"""
    name = input("What is your name?")
    school = input("What school are you in?")
    schoolClass = input("What class are you in?")
    print("*" * 100)
    print("Name: {}".format(name))
    print("School: {}".format_map(school))
    print("Class: {}".format(schoolClass))
    print("*" * 100)


def main():
    """prints business card"""
    printBusinessCard()


if __name__ == '__main__':
    main()
