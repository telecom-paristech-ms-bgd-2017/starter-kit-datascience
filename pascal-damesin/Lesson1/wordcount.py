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

def dict_words(filename):       #buid up a dictionary of the words of the filename
    f = open(filename,'r')      #load filename to f ready for reading
    dictword = {}               #build up a dictionary
    for line in f:              #look for every line of the file f
        word = line.split()     #split the line in words
        for w in word:          #look for every word of each line
            w = w.lower()       #replace each word by its lowercase version
            if w in dictword:   #check if the word already is in the dictionary
                dictword[w] = dictword[w] + 1#increments the value of this word
            else:
                dictword[w] = 1    #if 1st time, set value 1
    f.close()
    return dictword             #return a dictionary of key/value

def print_words(filename):      #print the dictionary of words from the filename
    dictword = dict_words(filename) #build up the dictionary
    word = sorted(dictword.keys())  #sort the dictionary by the key word
    for w in word:                  #look for every key/value of the dictionary
        print(w, ' ' ,dictword[w])  #print a key value pair
        print                       #return to next line

def print_top(filename):
    dictword = dict_words(filename) #build up the dictionary
    items = sorted(dictword.items(),key=get_count, reverse=True)#sort the dictionnary reversely by value
    for i in items[:20]:            #look for the 1st 20 items
        print(i[0], ' ' , i[1])     #print the key value pair
        print

def get_count(thetuple):    #return the value of the tuple
    return thetuple[1]
#
###

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
