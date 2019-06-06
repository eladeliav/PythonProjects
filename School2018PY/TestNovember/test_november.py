"""
Elad Eliav
Test.txt November
"""

INITIALIZED = 0
INCREMENTER = 1
FIRST_ELEMENT = 0
SECOND_ELEMENT = 1
READ_PARAMETER = 'r'
REVERSE_INDEX = -1
WORDS_TO_JUMP = 3
SAFE_NUM_OF_WORDS = 100


def is_substring(string1, string2):
    """
    Checks if a given string is in another given string
    :param string1: string to check if it's in the other
    :param string2: string to check if it includes the other
    :return: True if string in string2, else False
    """
    return string1 in string2


def how_many_substrings(tuple_list):
    """
    Counts how many elements in a list of tuples return True in is_substring()
    :param tuple_list: list of tuples
    :return: number of elements that is_substring() returns True on
    """
    return len(filter(lambda tpl: is_substring(tpl[FIRST_ELEMENT], tpl[SECOND_ELEMENT]), tuple_list))


def substring_first(tuple_list):
    """
    Returns a list of tuples sorted by whether or not is_substring() returns True on a given element
    :param tuple_list: the list of tuples to sort
    :return: a sorted list of tuples according to is_substring()
    """
    return sorted(tuple_list, key=lambda kv: is_substring(kv[FIRST_ELEMENT], kv[SECOND_ELEMENT]), reverse=True)


def is_file_valid(filename):
    """
    Checks if a file exists
    :param filename: file to check
    :return: True if it exists, else False
    """
    try:
        f = open(filename, READ_PARAMETER)
        f.close()
        return True
    except IOError as e:
        print "Couldn't open file\n", e
        return False


def decode_long(filename):
    """
    Decodes and prints a file according to the following conditions:
    1. every word is reversed
    2. 2 nonsense words in between every real word
    :param filename: file to decode
    """
    if not is_file_valid(filename) or not is_it_enough(filename):
        return
    with open(filename, READ_PARAMETER) as f:
        for line in f:
            line = line.split()[::WORDS_TO_JUMP]  # splitting line for each word and only considering every
            # WORDS_TO_JUMP words
            decoded_list = list()
            for w in line:
                decoded_list.append(w[::REVERSE_INDEX])  # adding the reversed word to the decoded_list
            print ' '.join(decoded_list)  # printing all elements in decoded_list with a space in between


def decode(filename):
    """
    Decodes and prints a file according to the following condition:
    Every word is reversed
    :param filename: file to decode
    """
    if not is_file_valid(filename) or not is_it_enough(filename):
        return
    with open(filename, READ_PARAMETER) as f:
        for line in f:
            line = line.split()
            decoded_list = list()
            for w in line:
                decoded_list.append(w[::REVERSE_INDEX])
            print ' '.join(decoded_list)


def is_it_enough(filename):
    """
    Checks if file is 'safe' enough by checking if it has SAFE_NUM_OF_WORDS words at least
    :param filename: file to check
    """
    if not is_file_valid(filename):
        return
    with open(filename, READ_PARAMETER) as f:
        num_of_words = INITIALIZED
        for line in f:
            num_of_words += len(line.split())
        return True if num_of_words > SAFE_NUM_OF_WORDS else False


def main():
    """
    Uses all of the above functions
    """
    a = ('b', 'cyber')
    print 'is', a, 'a substring:', is_substring(a[0], a[1])
    a = ('d', 'cyber')
    print 'is', a, 'a substring:', is_substring(a[0], a[1])
    a = [('c', 'cyber'), ('i', 'team'), ('y', 'rothberg'), ('l', 'hello'), ('t', 'test')]
    print 'There are', how_many_substrings(a), 'elemnts in ', a, 'that are substrings'
    print 'Sorted by substrings:', substring_first(a)
    print '\n***************\nSECRET1 DECODED\n***************\n'
    decode('secret1')
    print '\n***************\nSECRET2 DECODED\n***************\n'
    decode_long('secret2')
    """
    Output: 
    is ('b', 'cyber') a substring: True
    is ('d', 'cyber') a substring: False
    There are 3 elemnts in  [('c', 'cyber'), ('i', 'team'), ('y', 'rothberg'), ('l', 'hello'), ('t', 'test')] that are substrings
    Sorted by substrings: [('c', 'cyber'), ('l', 'hello'), ('t', 'test'), ('i', 'team'), ('y', 'rothberg')]
    
    ***************
    SECRET1 DECODED
    ***************
    
    Hey Jude, don't make it bad
    Take a sad song and make it better
    Remember to let her into your heart
    Then you can start to make it better
    Hey Jude, don't be afraid
    You were made to go out and get her
    The minute you let her under your skin
    Then you begin to make it better
    And anytime you feel the pain, hey Jude, refrain
    Don't carry the world upon your shoulders
    For well you know that it's a fool who plays it cool
    By making his world a little colder
    Nah nah nah nah nah nah nah nah nah
    Hey Jude, don't let me down
    You have found her, now go and get her
    Remember to let her into your heart
    Then you can start to make it better
    So let it out and let it in, hey Jude, begin
    You're waiting for someone to perform with
    And don't...
    
    ***************
    SECRET2 DECODED
    ***************
    
    Hey Jude, don't make it bad
    Take a sad song and make it better
    Remember to let her into your heart
    Then you can start to make it better
    Hey Jude, don't be afraid
    You were made to go out and get her
    The minute you let her under your skin
    Then you begin to make it better
    And anytime you feel the pain, hey Jude, refrain
    Don't carry the world upon your shoulders
    For well you know that it's a fool who plays it cool
    By making his world a little colder
    Nah nah nah nah nah nah nah nah nah
    Hey Jude, don't let me down
    You have found her, now go and get her
    Remember to let her into your heart
    Then you can start to make it better
    So let it out and let it in, hey Jude, begin
    You're waiting for someone to perform with
    And don't...
    """


if __name__ == '__main__':
    main()
