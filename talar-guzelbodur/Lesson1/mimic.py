#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/


import random
import sys


def mimic_dict(filename):
    """Returns mimic dict mapping each word to list of words which follow it."""
    # +++your code here+++
    previous_word = ''
    word_mimics = {previous_word:[]}
    file = open(filename, 'rU')  # opens the file
    for line in file:  # iterates over the lines of the file
        # iterates over the words of the line, converted to lower case
        for word in line.lower().split():
            # append word to previous word's list
            word_mimics[previous_word] = [word] if not previous_word in word_mimics else (word_mimics[previous_word] + [word])
            previous_word = word
    file.close()  # closes file
    return word_mimics


def print_mimic(mimic_dict, word):
    """Given mimic dict and start word, prints 200 random words."""
    # +++your code here+++
    text = [word] # initialize the generated text with the the initial word
    for i in range(200):
        # randomly select the next word from the list associated with the previous word  
        word = random.choice(mimic_dict[word]) if word in mimic_dict else ''
        # append the new word to the text
        text.append(word)
    # print the text
    print(' '.join(text))


# Provided main(), calls mimic_dict() and mimic()
def main():
    if len(sys.argv) != 2:
        print('usage: ./mimic.py file-to-read')
        sys.exit(1)

    dico = mimic_dict(sys.argv[1])
    print_mimic(dico, '')


if __name__ == '__main__':
    main()
