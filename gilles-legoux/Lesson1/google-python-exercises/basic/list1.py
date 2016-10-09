#!/usr/bin/python -tt
# basic/list1.py

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
    count = 0
    for word in words:
        if len(word) < 2:
            continue
        if word[0] == word[-1]:
            count += 1
    return count


# short but copy list one time
def match_ends_bis(words):
    return len(filter(lambda x: len(x) >= 2 and x[0] == x[-1], words))


# B. front_x
# Given a list of strings, return a list with the strings
# in sorted order, except group all the strings that begin with 'x' first.
# e.g. ['mix', 'xyz', 'apple', 'xanadu', 'aardvark'] yields
# ['xanadu', 'xyz', 'aardvark', 'apple', 'mix']
# Hint: this can be done by making 2 lists and sorting each of them
# before combining them.
def front_x(words):
    xs = []
    nxs = []
    for word in words:
        if len(word) == 0:
            continue
        if word[0] == 'x':
            xs.append(word)
        else:
            nxs.append(word)
    xs.sort()
    nxs.sort()
    return xs + nxs


# short but copy list two times
def front_x_bis(words):
    return sorted(filter(lambda x: len(x) > 0 and x[0] == 'x', words)) \
           + sorted(filter(lambda x: len(x) == 0 or x[0] != 'x', words))


# C. sort_last
# Given a list of non-empty tuples, return a list sorted in increasing
# order by the last element in each tuple.
# e.g. [(1, 7), (1, 3), (3, 4, 5), (2, 2)] yields
# [(2, 2), (1, 3), (3, 4, 5), (1, 7)]
# Hint: use a custom key= function to extract the last element form each tuple.
def sort_last(tuples):
    ts = []
    for k, tuple in enumerate(tuples):
        ts.append((tuple[-1], k))
    ts.sort()
    tts = []
    for k in range(len(ts)):
        tts.append(tuples[ts[k][1]])
    return tts


# with standard library so easy
def sort_last_bis(tuples):
    return sorted(tuples, key=lambda x: x[-1])


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


# Calls the above functions with interesting inputs.
def main():
    for f in [match_ends, match_ends_bis]:
        print f.__name__, ':'
        test(f(['aba', 'xyz', 'aa', 'x', 'bbb']), 3)
        test(f(['', 'x', 'xy', 'xyx', 'xx']), 2)
        test(f(['aaa', 'be', 'abc', 'hello']), 1)

    print
    for f in [front_x, front_x_bis]:
        print f.__name__, ':'
        test(f(['bbb', 'ccc', 'axx', 'xzz', 'xaa']),
         ['xaa', 'xzz', 'axx', 'bbb', 'ccc'])
        test(f(['ccc', 'bbb', 'aaa', 'xcc', 'xaa']),
         ['xaa', 'xcc', 'aaa', 'bbb', 'ccc'])
        test(f(['mix', 'xyz', 'apple', 'xanadu', 'aardvark']),
         ['xanadu', 'xyz', 'aardvark', 'apple', 'mix'])

    print
    for f in [sort_last, sort_last_bis]:
        print f.__name__, ':'
        test(f([(1, 3), (3, 2), (2, 1)]),
             [(2, 1), (3, 2), (1, 3)])
        test(f([(2, 3), (1, 2), (3, 1)]),
             [(3, 1), (1, 2), (2, 3)])
        test(f([(1, 7), (1, 3), (3, 4, 5), (2, 2)]),
             [(2, 2), (1, 3), (3, 4, 5), (1, 7)])


if __name__ == '__main__':
    main()
