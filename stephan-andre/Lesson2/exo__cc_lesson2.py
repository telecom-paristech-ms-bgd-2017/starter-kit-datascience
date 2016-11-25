# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 16:20:21 2016

@author: Stephan
"""
import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if n>=0:   
        s=string*n
    else:
        return "try again"
    return s


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    if len(nums)>=4:
        if 9 in nums[0:3]:
            return True
        else:
            return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    cnt=string.count(string[-2:])
    return cnt-1

#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    array2=[]
    for s in array:
        array2.append(len(s))
    return array2

#write fizbuzz programm
def fizbuzz(num):
    if num%3==0 and num%5==0:
        return 'fizbuzz'        
    elif num%3==0:
        return 'fiz'
    elif num%5==0:
        return 'buzz'
    else:
        return"num non divisible par 3 ou 5"

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    l=list(map(int, str(number)))
    return l

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    l1=str.split(text)
    l2=list()
    for word in l1:
        l2.append(word[1:] + word[0] + 'ay')
        text2=' '.join(l2)
        text3=text2[0].upper()+text2[1:].lower() 
    return text3

def pigLatin_back(text):
    l1=str.split(text)
    l2=list()
    for word in l1:
        l2.append(word[-3] + word[0:-3])
        text2=' '.join(l2)
        text3=text2[0].upper()+text2[1:].lower() 
    return text3




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