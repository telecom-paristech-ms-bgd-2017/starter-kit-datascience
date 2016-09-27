#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Wordcount exercise
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

# +++your code here+++
def readfile(filename):
    dict_text = {}
    f = open(filename)
    for line in f.readlines():
        ligne = line.strip()
        for word in ligne.replace('--', " ").split(" "):
            wordl = word.lower()
            wordl = wordl.replace(',', '')   # cette partie pourrait se simplifier avec des regex
            wordl = wordl.replace('(', '')
            wordl = wordl.replace(')', '')
            wordl = wordl.replace('.', '')
            wordl = wordl.replace('!', '')
            wordl = wordl.replace('?', '')
            wordl = wordl.replace(':', '')
            wordl = wordl.replace('\"', '')
            wordl = wordl.replace(';', '')
            wordl = wordl.replace('[', '')
            wordl = wordl.replace(']', '')
            wordl = wordl.replace('*', '')
            if wordl not in dict_text:
                dict_text[wordl] = 0
            dict_text[wordl] += 1
    dict_text.pop('')
    return dict_text


def print_words(filename):

    dico = readfile(filename)
    for k in sorted(dico):
        print(k, dico[k])


def print_top(filename):

    dico = readfile(filename)
    items = [(v, k) for k, v in dico.items()]
    items.sort()
    items.reverse()
    items = [(k, v) for v, k in items]
    for item in items[0:20]:
        print(item[0])



# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():

    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)

if __name__ == '__main__':
    main()