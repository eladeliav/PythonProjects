"""
SHIRA NEVO
YUD ALEF 2
DICTIONARIES EXCERCISE 1
"""
FIRST_CHAR = 0
SECOND_CHAR = 1

contacts = dict()
friend_contact = {"Shira Nevo ": "0549292431", "Yarden Cohen ": "0534205598"}


def add_contact(name, number):
    """ adding a contact by his name and his number """
    name = check_name(name)
    if name is not None and check_phone(number):
        contacts[name] = number
        return contacts
    else:
        return None


def check_name(name):
    """ checking if the given name is only letters and
    the first letter from each word is capital while the others
    arr low"""
    legal_lst = []
    name_lst = name.split()
    for w in name_lst:
        if w.isalpha() is False:
            return None
        legal_lst.append(w[0].upper() + w[1:].lower())
    legal_name = " ".join(legal_lst)
    return legal_name


def check_phone(number):
    """ checking if the number contains only digits"""
    if number.isdigit():
        return True
    return False


def find_phone_number(name):
    """ finds the phone number of the contact by his name"""
    name = check_name(name)
    if name in contacts and name is not None:
        return contacts[name]
    else:
        return None


def find_name(number):
    """ finds the name of the contact by his number"""
    for key, value in contacts.items():
        if value == number:
            return key


def print_by_names(contacts):
    """ prints the sorted contact book by the names """
    new_contacts = sorted(contacts)
    for i in new_contacts:
        print i + " : " + contacts[i]


def print_by_phone(contacts):
    """ prints the sorted contact book by the numbers """
    new_contacts = sorted(contacts.values())
    for i in new_contacts:
        for key, value in contacts.items():
            if value == i:
                print key + " : " + i


def connect_dict(dictionary, contacts):
    """ connecting between two contact books"""
    friend_contact.update(contacts)
    print_by_names(friend_contact)


def main():
    name = raw_input("enter contact's name")
    number = raw_input("enter contact's phone number ")
    add_contact(name, number)

    name = raw_input("enter contact's name")
    number = raw_input("enter contact's phone number ")
    add_contact(name, number)
    """
    name = raw_input("enter contact's name")
    number = raw_input("enter contact's phone number ")
    add_contact(name, number) """

    name = raw_input("enter contact's name to find in the contact book ")
    print find_phone_number(name)

    number = raw_input("enter contact's number to find in the contact book ")
    print find_name(number)

    print_by_names(contacts)
    print_by_phone(contacts)

    connect_dict(friend_contact, contacts)


if __name__ == '__main__':
    main()

