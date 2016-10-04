# -*- coding: utf-8 -*-
import unittest
# Mahzad KALANTARI Septembre 2016

# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):

    return string*n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    if len(nums)<4:
       return False
    else:
        if 9 in nums[0:4]:
             return True
        else:
             return False

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    count=0
    for n in range(len(string)-2):
        if string[n:n+2]==string[-2:]:
            count+=1
    return count


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words_1(array):
    list_of_word_number=[]
    for a in array:
        list_of_word_number.append(len(a))
    return list_of_word_number

def length_words(array):
    return [len(x) for x in array]


#write fizbuzz programm
#Écrire un programme qui affiche les nombres de 1 à 199.
#Mais pour les multiples de 3, afficher “Fizz” au lieu du nombre
#et pour les multiples de 5 afficher “Buzz”.
#Pour les nombres multiples de 3 et 5, afficher “FizzBuzz”.


def fizbuzz():
    num_list=[]
    for num in range(0,199):
        if num%3==0  and not num%5==0 :
           num_list.append("Fizz")
        elif num%5==0 and not num%3==0 :
             num_list.append("Buzz")
        elif num%5==0 and num%3==0 :
             num_list.append("FizzBuzz")
        else :
             num_list.append(num)
    print(num_list)
    return num_list


#Write a function that takes a number and returns a list of its digits.
def number2digits_1(number):
    list_of_digit=[]
    for num in str(number):
        list_of_digit.append(int(num))
    return list_of_digit

def number2digits(number):
    return [int(num) for num in str(number)]




#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
# "The quick brown fox") , "Hetay uickqay rownbay oxfay"

def pigLatin(text):
  pig_list=[]
  split_txt= text.split()
  for s in split_txt:
      s = s[1:len(s)]+s[0].lower()+'ay'
      pig_list.append(s)

  pig_text= pig_list[0].capitalize()+' '

  for p in pig_list[1:]:
      pig_text = pig_text + p+' '
  return pig_text.rstrip()

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

    fizbuzz()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
