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
# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.


def compteur_de_mots(filename):
    # renvoie un dictionnaire avec chaque mot et leur nombre d'occurence
    # on map chaque mot avec son nombre d'apparition dans un DICTIONNAIRE
    compteur = {}
    texte = open(filename, 'r')  # on ouvre le fichier
    for ligne in texte:
        # on va spliter les mots de chaque ligne par espace
        mots = ligne.split()
        for mot in mots:
            # on l'ecrit en minuscule
            mot = mot.lower()
            # si le mot n'est pas dans la liste des mots, on l'ajoute :
            if not mot in compteur:
                compteur[mot] = 1  # Ca l'ajoute a la "liste" compteur
            else:
                compteur[mot] = compteur[mot] + 1
    texte.close()  # fermeture du fichier
    return compteur


def print_words(filename):
    # on affiche la liste des mots et leur compteur a cote, puis passage a la
    # ligne apres chacun
    dictionnairefinal = compteur_de_mots(filename)
    # on trie les mots par ordre croissant
    mots = sorted(dictionnairefinal.keys())
    # on l'affiche comme on le demande :
    for mot in mots:
        print mot, dictionnairefinal[mot]


def get_count(mot):
    # renvoie le nombre d'occurence d'un mot
    return mot[1]


def print_top(filename):
    # affiche les 20 premiers mots avec les occurences les plus fortes
    # on fait le dictionnaire :
    dictionnaire = compteur_de_mots(filename)
    # chaque item du dictionnaire est un couple (mot, compteur)
    # on les trie par compteur par ordre DECROISSANT
    items = sorted(dictionnaire.items(), key=get_count, reverse=True)
    # on affiche les 20 premiers :
    for item in items[:20]:
        print item[0], item[1]

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.


def main():
    if len(sys.argv) != 3:
        print 'usage: ./wordcount.py {--count | --topcount} file'
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
