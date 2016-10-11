# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:42:10 2016

@author: Stephan
"""

# A. match_ends
def match_ends (l):
    int=0
    for s in l:
        if len(s)>1 and s[0]==s[-1]:
            int+=1
        else:
            int+=0    
    return int
    
# B. front_x
def front_x(l):
    l2=list()
    l3=list()
    for s in l:
        if s[0]=='x':
            l2.insert(0, s)
            l2.sort()
        else :    
            l3.insert(-1, s)
            l3.sort()
    return l2+l3

# C. sort_last
def sort_last(l):
    return sorted(l, key=lambda tup: (tup[-1]) )
    
# Provided simple test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print ('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main(): 
  print ('match_ends')
  # Each line calls donuts, compares its result to the expected for that call.
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


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
