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
    # To count the number of same match
    number_of_match = 0

    for w in words:
        # Test length
        if ( len(w) < 2):
            continue
        if(w[0] == w[-1:]):
            number_of_match +=1

    return number_of_match


def match_ends_misunderstood(words):
    # To count the number of same chars
    number_of_match = 0
    # Copy
    search_list = words
    for w in words:
        # Remove s from the list to not match w against w
        search_list.remove(w)
        for s in search_list:
            # Sanity check
            print "Searcing "+w+" in "+s
            if (len(s) < 2 or len(w) < 2):
                continue
            if(s[0] == w[0] and s[-1:] == w[-1:]):
                print 'Cool'
                number_of_match +=1

    return number_of_match

# B. front_x
# Given a list of strings, return a list with the strings
# in sorted order, except group all the strings that begin with 'x' first.
# e.g. ['mix', 'xyz', 'apple', 'xanadu', 'aardvark'] yields
# ['xanadu', 'xyz', 'aardvark', 'apple', 'mix']
# Hint: this can be done by making 2 lists and sorting each of them
# before combining them.
def front_x(words):
    # +++your code here+++
    # By default abc_sorted_list = words will not make a Copy
    # but just provide a reference. You need to slice.
    abc_sorted_list = words[:]
    # In this list we will put x starting words, sorted
    x_sorted_list = []
    # Remove x words from original list
    for w in words:
        if(w[0] == 'x' or w[0] == 'X'):
            # Remove xanadu
            abc_sorted_list.remove(w)
            # Add xanadu
            x_sorted_list.append(w)

    #Sort x words
    x_sorted_list.sort()
    # Sort the list, without x starting words
    abc_sorted_list.sort()

    # Extends the x list with the abc list
    x_sorted_list.extend(abc_sorted_list)

    return x_sorted_list



def last_item(tuple):
    return(tuple[-1])

# C. sort_last
# Given a list of non-empty tuples, return a list sorted in increasing
# order by the last element in each tuple.
# e.g. [(1, 7), (1, 3), (3, 4, 5), (2, 2)] yields
# [(2, 2), (1, 3), (3, 4, 5), (1, 7)]
# Hint: use a custom key= function to extract the last element form each tuple.
def sort_last(tuples):
    # +++your code here+++

    tuples.sort(key=last_item)
    return tuples


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
