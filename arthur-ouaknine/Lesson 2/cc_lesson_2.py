# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:30:33 2016

@author: arthurouaknine
"""
import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n, int):
        return 'bad argument'
    if not isinstance(string, str):
        return 'bad argument'
    return n*string

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.


def array_front9(nums):
    if len(nums) < 4:
        if 9 in nums:
            return True
    else:
        if 9 in nums[:4]:
            return True
    return False

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1
# (we won't count the end substring).
# prendre les 2 derniers caractères


def last2(string):
    sub = string[-2:]
    cpt = 0
    for i in range(len(string)-2):
        if sub[0] == string[i] and sub[1] == string[i+1]:
            cpt += 1
    return cpt


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.


def length_words(array):
    # obj = map(lambda x: len(x), array) je ne comprends pas comment ça marche
    listnum = []
    for word in array:
        listnum.append(len(word))
    return listnum


# write fizbuzz programm


def fizbuzz():
    for i in range(100):
        if i % 3 == 0 and i % 5 == 0:
            print(str(i) + " fizbuzz")
        elif i % 3 == 0:
            print(str(i) + " fiz")
        elif i % 5 == 0:
            print(str(i) + " buzz")
        else:
            print(str(i))


# Write a function that takes a number and returns a list of its digits.


def number2digits(number):
    newList = []
    for e in str(number):
        newList.append(int(e))
    return newList


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'


def pigLatin(text):
    text = text.lower()
    text = text.split(" ")
    newText = []
    for word in text:
        newWord = word[1:] + word[0] + "ay"
        newText.append(newWord)
    return " ".join(newText).capitalize()


# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]), True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]), False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]), False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2), 'HelHel')
        self.assertEqual(string_times('Toto', 1), 'Toto')
        self.assertEqual(string_times('P', 4), 'PPPP')

    def testLast2(self):
        self.assertEqual(last2('hixxhi'), 1)
        self.assertEqual(last2('xaxxaxaxx'), 1)
        self.assertEqual(last2('axxxaaxx'), 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello', 'toto']), [5, 4])
        self.assertEqual(length_words(['s', 'ss', '59fk', 'flkj3']),
                         [1, 2, 4, 5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849), [8, 8, 4, 9])
        self.assertEqual(number2digits(4985098), [4, 9, 8, 5, 0, 9, 8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox"),
                         "Hetay uickqay rownbay oxfay")

def main():
    unittest.main()

if __name__ == '__main__':
    main()