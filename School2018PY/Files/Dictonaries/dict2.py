# -*- coding: utf-8 -*-
contacts = dict()


def add_contact(name, phonenum):
    """adds name and phone number to contacts"""
    global contacts
    if not phonecheck(phonenum):
        return
    if not namecheck(name):
        name = name.title()
    contacts[name] = phonenum


def phonecheck(phonenum):
    """checks if phone number is made out of digits"""
    return phonenum.isdigit()


def namecheck(name):
    """checks if name's first letter is uppercase letter, and the rest are lowercase"""
    return name is name.title()


def find_phone_number(name):
    return contacts[name]


def name_sort(contacts):
    print sorted(contacts.items())


def find_name(phonenum):
    reversed_contacts = {}
    for key,value in contacts.items():
        reversed_contacts.update({value:key})
    return reversed_contacts[phonenum]


def phone_sort(contacts):
    reversed_contacts = {}
    for key,value in contacts.items():
        reversed_contacts.update({value:key})
    print sorted(reversed_contacts)


def main():
    add_contact("Dan", "15423345")
    add_contact("alon", "25236342")
    add_contact("Nadav", "35235462")
    print contacts.items()
    name_contacts()



if __name__ == '__main__':
    main()
