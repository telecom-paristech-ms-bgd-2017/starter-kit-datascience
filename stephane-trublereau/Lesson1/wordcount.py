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
import operator
# +++your code here+++
# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

def dictionnaire(filename):
    input_file = open(filename, 'r')
    dictionnaire = dict()
    for line in input_file:
        words = line.split()
        for word in words :
            word = word.lower()
            if word in dictionnaire :
                dictionnaire[word] = dictionnaire[word] + 1
            else:
                dictionnaire[word] = 1
    input_file.close()  
# retourne list(word/count)          
    return dictionnaire
###
def print_top(filename):
     words = dictionnaire(filename)   
     print ( words )
     words_tries = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
     print(words_tries)
     i=0
     for (word, count) in words_tries:
         if ( i  <  20 ) :
             print (" word : " + word + " nombre : " + str(count))
         else :
             break
         i=i+1
        
### fonction qui retourne la liste de
def print_words(filename):
## récuoération des mots et leurs comptages à partir du fichier nommé filename
## transmis en entrée     
    words = dictionnaire(filename)
## trie sur le nom de la list des mots    
    words_tries = sorted(words.keys())
    
    for word in words_tries :
        print (word + ' , ' + str(words[word]) )
 #  

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
#  if len(sys.argv) != 3:
#    print ('usage: ./wordcount.py {--count | --topcount} file')
#    sys.exit(1)

#  option = sys.argv[1]
  option = '--topcount'
  ##filename = sys.argv[2]
  filename = 'small.txt'
  if option == '--count':
    print_words(filename)
  elif option == '--topcount':
    print_top(filename)
  else:
    print ('unknown option: ' + option)
    sys.exit(1)

if __name__ == '__main__':
  main()
