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

from __future__ import print_function

import operator
import string
import sys


def print_words(filename):
    sort_options = {'key': operator.itemgetter(0)}
    print_dico(sorted(file_dict(filename).items(), **sort_options))

def print_top(filename):
    sort_options = {'key': operator.itemgetter(1), 'reverse': True}
    print_dico(sorted(file_dict(filename).items(), **sort_options)[:20])

# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

## Utility functions:
def helperfct(filename):
    i = 0
    line_update_without_symbol_and_space = []
    file_content_in_str_without_symbol = []
    file_content = open(filename, 'r')

    for line in file_content:
        translator = string.maketrans(string.punctuation + '§', ' ' * len(string.punctuation + '§'))
        line_update_without_symbol_and_space = line.translate(translator).lower().split()
        file_content_in_str_without_symbol += line_update_without_symbol_and_space

    words_with_count = dict()
    for i in range(len(file_content_in_str_without_symbol)):
        words_with_count[file_content_in_str_without_symbol[i]] = file_content_in_str_without_symbol.count(
            file_content_in_str_without_symbol[i])

    for key in sorted(words_with_count):
        print(key, words_with_count[key])


        # print(words_with_count)#vue du dictionnaire en {key:dict(key),..,..}
    # print(words_with_count.items())#vue du dictionnaire en liste de tuple

    # print(words_with_count.keys())#print only dictionary keys
    # print("=========sorted by words which is 0 index=============")
    # print(OrderedDict(sorted(words_with_count.items(), key=lambda t: t[0])))
    # print("=========sorted by count which is 1 index=============")
    # print( OrderedDict(sorted(words_with_count.items(), key=lambda t: t[1],reverse = True)))
    # print("=========sorted by length of word =============")
    # print(OrderedDict(sorted(words_with_count.items(), key=lambda t: len(t[0]))))

    return sorted(words_with_count.items(), key=lambda t: t[1], reverse=True)




# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 3:
        print ('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print ('unknown option: ' + option)
        sys.exit(1)

if __name__ == '__main__':
    main()
