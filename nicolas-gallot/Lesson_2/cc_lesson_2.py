import unittest
import math

# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    try:
        s = str(string)
        nb = int(n)
        if nb >= 0:
            return n*s
        else:
            return n + " should not be < 0"
    except ValueError:
        return str(n) + "is not a valid argument"


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.


def array_front9(nums):
    try:
        l = len(nums)
        m = min(l, 4)
        if 9 in nums[0:m]:
            return True
        else:
            return False
    except ValueError:
        print("Bad argument")
        return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    if(len(string)) > 3:
        last_2 = string[-2:]
        c = 0
        for i in range(0, len(string)-2):
            sub_str = string[i] + string[i+1]
            if sub_str == last_2:
                c += 1
        return c
    else:
        return 0


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.


def length_words(array):
    if len(array) < 1:
        return "Bad argument"
    res = []
    for word in array:
        res.append(len(word))
    return res

#write fizbuzz programm


def fizbuzz():
    for i in range(1, 100):
        if i % 15 == 0:
            print(str(i) + ': fizzbuzz')
        elif i % 3 == 0:
            print(str(i) + ': fizz')
        elif i % 5 == 0:
            print(str(i) + ': buzz')
        else:
            print(str(i))
    return


#Write a function that takes a number and returns a list of its digits.


def number2digits(number):
    res = [int(i) for i in str(number)]
    return res

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'


def pigLatin(text):
    words = str(text).split(' ')
    new_text = ""
    n = 0
    for w in words:
        first_letter = str(w[0]).lower()
        new_word = w[1:] + first_letter + "ay"
        if n == 0:
            new_word = new_word[0].upper() + new_word[1:]
        if n != len(words)-1:
            new_text += new_word + " "
        else:
            new_text += new_word
        n += 1
    return new_text


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
    #unittest.main()
    fizbuzz()

if __name__ == '__main__':
    main()
