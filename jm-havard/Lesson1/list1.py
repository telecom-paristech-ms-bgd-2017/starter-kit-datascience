#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Basic list exercises
# Fill in the code for the functions below. main() is already set up
# to call the functions with a few different inputs,
# printing 'OK' when each function is correct.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code.
# It's ok if you do not complete all the functions, and there
# are some additional functions to try in list2.py.

# A. match_ends
# Given a list of strings, return the count of the number of
# strings where the string length is 2 or more and the first
# and last chars of the string are the same.
# Note: python does not have a ++ operator, but += works.
def match_ends(words):
  # +++your code here+++
    #print(len(words))
    print(words)
    compteur=0
    for i in range(len(words)):
       #print(len(words[i]))
       
        if ((len(words[i])>=2) and (words[i][0] == words[i][-1])):
            print(words[i])
            compteur+=1
            #print(compteur)

    return compteur


# B. front_x
# Given a list of strings, return a list with the strings
# in sorted order, except group all the strings that begin with 'x' first.
# e.g. ['mix', 'xyz', 'apple', 'xanadu', 'aardvark'] yields
# ['xanadu', 'xyz', 'aardvark', 'apple', 'mix']
# Hint: this can be done by making 2 lists and sorting each of them
# before combining them.

def front_x(words):
  # je cree deux liste une contenant les string commencant par x :res_x et l'autre non
# je trie ces listes sur elles meme et je concatene les deux : result
   res_x=[]
   res_ssx=[]
   for i in range(len(words)):
       test=words[i]
       if test[0] == 'x' : 
           res_x.append(test)
       else:
           res_ssx.append(test)
   res_x=sorted(res_x)  
   res_ssx=sorted(res_ssx)
   result=res_x+res_ssx
   
   return result


# C. sort_last
# Given a list of non-empty tuples, return a list sorted in increasing
# order by the last element in each tuple.
# e.g. [(1, 7), (1, 3), (3, 4, 5), (2, 2)] yields
# [(2, 2), (1, 3), (3, 4, 5), (1, 7)]
# Hint: use a custom key= function to extract the last element form each tuple.
"""
abandon de cette solution
je n arrive pas a recreer le dictionnaire
def sort_last(tuples):
    
  # +++your code here+++
    dico={}
    dico_trie={}
    dico_tri2={}
    print(tuples)
    for i in range(len(tuples)):
        print(tuples[i][-1])
        dico[tuples[i]]=tuples[i][-1]
    print(dico)
    dico_trie=sorted(dico.values()) 
    dico_tri2=list(dico_trie.keys())
 #   dico_trie=sorted(dico.values())   
  #  print(dico_trie)
  #  for j in range(len(dico_trie)):
  #      dico_trie2[j]=dico_trie.keys(j)
  #  print(dico_trie2)
    print(dico_trie)
    return
    
    
"""

def sort_last(tuples):
    return sorted(tuples, key = lambda t: t[-1])

# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print ('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# Calls the above functions with interesting inputs.
def main():
  print ('match_ends')
  test(match_ends(['aba', 'xyz', 'aa', 'x', 'bbb']), 3)
  test(match_ends(['', 'x', 'xy', 'xyx', 'xx']), 2)
  test(match_ends(['aaa', 'be', 'abc', 'hello']), 1)

  print
  print ('front_x')
  test(front_x(['bbb', 'ccc', 'axx', 'xzz', 'xaa']),
       ['xaa', 'xzz', 'axx', 'bbb', 'ccc'])
  test(front_x(['ccc', 'bbb', 'aaa', 'xcc', 'xaa']),
       ['xaa', 'xcc', 'aaa', 'bbb', 'ccc'])
  test(front_x(['mix', 'xyz', 'apple', 'xanadu', 'aardvark']),
       ['xanadu', 'xyz', 'aardvark', 'apple', 'mix'])

       
  print
  print ('sort_last')
  test(sort_last([(1, 3), (3, 2), (2, 1)]),
       [(2, 1), (3, 2), (1, 3)])
  test(sort_last([(2, 3), (1, 2), (3, 1)]),
       [(3, 1), (1, 2), (2, 3)])
  test(sort_last([(1, 7), (1, 3), (3, 4, 5), (2, 2)]),
       [(2, 2), (1, 3), (3, 4, 5), (1, 7)])


if __name__ == '__main__':
  main()
