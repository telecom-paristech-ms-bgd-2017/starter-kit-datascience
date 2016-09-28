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
    if len(s) < 3:
        return s
    elif 'ing' == s[-3:]:
        return s + 'ly'
    else:
        return s + 'ing'


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
    top_find_bad = False
    top_find_not = False
    newposbad = 0
    newposnot = len(s)
    longchaine = len(s)
    for mot in s.split(" "):
        mottmp = mot.lower()
        if mottmp[0:3] == 'not':
            top_find_not = True
            posnot = s.lower().find('not')
            if posnot <= newposnot:
                newposnot = posnot
        mottmp = mot.lower()
        if mottmp[0:3] == 'bad':
            top_find_bad = True
            posbad = s.lower().find('bad')
            if posbad >= newposbad:
                newposbad = posbad + 3
    if (top_find_bad and top_find_not) and newposnot < newposbad:
        s = s.replace(s[newposnot:newposbad], 'good')
        return s
    else:
        return s


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
    # +++your code here+++
    a_middle = len(a)//int(2)
    b_middle = len(b)//int(2)

    if len(a) % 2 == 1:
        a_middle += 1

    if len(b) % 2 == 1:
        b_middle += 1

    s = a[:a_middle]+b[:b_middle]+a[a_middle:]+b[b_middle:]
    return s


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
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


if __name__ == '__main__':
    main()
