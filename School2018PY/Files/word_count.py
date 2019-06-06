""" This program has been adapted for use by GVAHIM
       - the main revisions regard pep8 compliance and use of constants
Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...

Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.

2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.

Use str.split() (no arguments) to split on all whitespace.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

Optional: define a helper function to avoid code duplication inside
print_words() and print_top().

"""

import sys

REQUIRED_NUM_OF_ARGS = 3
ARG_OPTION = 1
ARG_FILE_NAME = 2


# +++your code here+++
# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.


def words_to_dict(filename):
    """
    A function the reads a given file and makes a dictionary displaying each words frequency.
    The function also returns the total number of words.
    :param filename: the file path
    :return: a tuple of the sorted dictionary of words in the file and their frequency
    and an int with the total number of words
    """
    with open(filename, 'r') as file1:  # opening the given file
        wordDictionary = dict()  # defining a dictionary
        numOfWordsTotal = 0  # int for counting the total number of words
        for line in file1:  # iterating over every line and doing the following:
            # removing punctuation from each line, making lower case, splitting into a list, adding to total number
            # of words, and iterating over the words to add to the dictionary
            #
            line = line.lower()

            words = line.split()
            numOfWordsTotal += len(words)
            for w in words:
                w = remove_punctuation(w)
                if w is not None and w[0].isalpha():  # making sure remove_punctuation returned correctly
                    wordDictionary[w] = wordDictionary.get(w, 0) + 1
        # returning a sorted wordDictionary with a descending order based on the value
        #  also returning numOfWordsTotal
        return sorted(wordDictionary.items(), key=lambda kv: kv[1], reverse=True), numOfWordsTotal


def print_words(filename):
    """
    gets a a sorted dictionay and total numberOfWords from words_to_dict
    and prints out the data
    :param filename: file path
    """
    myDict, numOfWords = words_to_dict(filename)
    print "The file has a total of", numOfWords, "and", len(myDict), "different words"
    for key, value in myDict:
        print key, value

def remove_punctuation(string):
    """
    removes symbols from the ends and the beginnings
    """
    while not string[0].isalpha() and len(string) > 1:
        string = string[1:]
    while not string[-1].isalpha() and len(string) > 1:
        string = string[:-1]
    if string is not '':
        return string
    return None

def print_top(filename):
    """
     gets a a sorted dictionay and total numberOfWords from words_to_dict
    and prints out the data but only the top 20 most recurring words
    :param filename: file path
    """
    myDict, numOfWords = words_to_dict(filename)
    for i in xrange(0, 20):
        print myDict[i][0], myDict[i][1]


# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.


def main():
    """
    receives command line param to run with print_top or print_words and calls the requested function
    """
    if len(sys.argv) != REQUIRED_NUM_OF_ARGS:
        print 'usage: ./wordcount.py {--count | --topcount} file'
        sys.exit(1)

    option = sys.argv[ARG_OPTION]
    filename = sys.argv[ARG_FILE_NAME]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print 'unknown option: ' + option
        sys.exit(1)


if __name__ == '__main__':
    main()
