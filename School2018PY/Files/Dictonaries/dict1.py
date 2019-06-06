"""
Elad Eliav
Dictionaries Practice
"""

global contacts
contacts = dict()

friend_contact = {"Shira Nevo ": "0549292431", "Yarden Cohen ": "0534205598"}


def add_contact(name, number):
    """
    adding contact to contacts dictionary (name,number)
     """
    name = format_name(name)  # formatting name to be legal
    if name is not None and check_phone(number):
        contacts[name] = number
        return contacts
    else:
        return None


def format_name(name):
    """
    formatting the given name to be like this: Elad Eliav
    """
    formatted_namelist = []
    given_name = name.split()
    for element in given_name:
        if element.isalpha() is False:
            return None  # returning None if there is a char that is a symbol or number
        formatted_namelist.append(element[0].upper() + element[1:].lower())  # making the first letter of each word
        # capital
    formatted_name = " ".join(formatted_namelist)
    return formatted_name


def check_phone(number):
    """
    making sure the given number is only in digits
    """
    if number.isdigit():
        return True
    return False


def find_phone_number(name):
    """
    returns phone number of the given name
    """
    name = format_name(name)
    if name in contacts and name is not None:  # if then name is in the dictionary and is formatted correctly
        return contacts[name]  # return the matching phone number
    else:
        return None


def find_name(number):
    """
    searches for the owner of the given number
    """
    for key, value in contacts.items():
        if value == number:
            return key


def print_by_names():
    """
    prints contacts sorted by key
    """
    print "\nSorted by names:"
    new_contacts = sorted(contacts)
    for i in new_contacts:
        print i + " : " + contacts[i]


def print_by_phone():
    """
    prints contacts sorted by value
    """
    print "\nSorted by numbers"
    contact_values = sorted(contacts.values())
    for i in contact_values:
        for key, value in contacts.items():
            if value == i:
                print key + " : " + i


def connect_dict():
    """ connecting between two contact books"""
    contacts.update(friend_contact)
    print_by_names()


def main():
    for i in range(0, 3):
        name = raw_input("Enter a new contact name")
        number = raw_input("Enter a new contact number")
        add_contact(name, number)

    name = raw_input("enter contact's name to find in the contact book ")
    print find_phone_number(name)

    number = raw_input("enter contact's number to find in the contact book ")
    print find_name(number)

    print_by_names()
    print_by_phone()

    connect_dict()


if __name__ == '__main__':
    main()
