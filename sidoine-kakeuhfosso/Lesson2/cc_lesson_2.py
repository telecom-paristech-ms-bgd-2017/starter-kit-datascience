# coding=utf-8
import unittest
import collections
import numpy as np


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n,int):
        return 'bad argument'
    if not isinstance (string, str):
        return 'bad argument'+string
    if n>=0:
        return 'bad argumet' + string
        
    return (n*string)

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):

  if not isinstance(nums, (collections.Sequence,list,tuple, np.ndarray))
        return 'bad argument'

  if nums.dtype != 'int32'
        return 'bad argument'
  for i in range(len(nums)):
    if nums[i]==9:
      test = True
    else:
        test = False
  return test


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
# prendre les 2 derniere lettre d'un mot et parcourir la string pour verifier
# used toto[-2:] ==>last 2 element
# used toto[1:-2]==>from 1st element to item before last one

def last2(string):
  if len(string)< 4:
     return 'string length without the last two character is less than 4, please enter string with length >= 4'

     # recupération des deux derniers charactères du string, puis comptage dans la chaine de caractère

  counter_last_2words = string[:-2].count(str[-2:])

  #sub = string[-2:]#recupération des deux derniers charactères du string, puis comptage dans la chaine de caractère
  #counter_last_2words = str.count(sub, 0, len(str) - 3)
  return counter_last_2words

#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    
    return

#write fizbuzz programm
def fizbuzz():
  return

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
  return

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
  return

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")



def main():
    unittest.main()

if __name__ == '__main__':
    main()
