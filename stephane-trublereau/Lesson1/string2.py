#!/usr/bin/python2.4 -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic string exercises

# D. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
  # +++your code here+++
    mot = s
    if len(mot) > 3 : 
        if mot[-3:] == 'ing' :
            return s + 'ly'
        else :
            return s + 'ing'
    else :
        return s

# E. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
  # +++your code here+++
  pos_chaine1 = s.find('not')
  pos_chaine2 = s.find('bad')
  if (pos_chaine1 != -1):
      if pos_chaine2 > pos_chaine1 : 
# on remplace 
          pos_chaine2 = pos_chaine2 + 3
          resultat = s[:pos_chaine1] + "good" + s[pos_chaine2:]
          return resultat
      else :
          return s
  else :
     return s   
  return


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
  # +++your code here+++
    front_a = int( len(a) / 2 ) + ( len(a) % 2 )
    back_a = int(len(a) / 2)
 #   print("front a : " + str(front_a))
 #   print("back a : " + str(back_a))
    front_b = int( len(b) / 2 ) + ( len(b) % 2 )
    back_b = int( len(b) / 2 )
 #   print("front b : " + str(front_b))
 #   print("back b : " + str(back_b))
    resultat = a[:front_a] + b[:front_b] + a[-back_a:] + b[-back_b:]        
    return resultat
    
# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  KO '
  print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# main() calls the above functions with interesting inputs,
# using the above test() to check if the result is correct or not.
def main():
  print('verbing')
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print
  print('not_bad')
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

  print
  print('front_back')
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')
  test(front_back('', 'Donut'), 'Donut')

if __name__ == '__main__':
  main()
