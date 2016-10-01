import unittest
import types


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if isinstance(n, int) and n > 0:
        word = n * string
    else:
        return 'Bad int : give a positif int'
    return word


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    b = 9

    for i in range(4):
        if nums[i] == b:
            c = True
            break
        else:
            c = False
    return c


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    end = string[-2:]
    a = 0
    for i in range(len(string) - 2):
        if string[i] + string[i + 1] == end:
            a += 1
    return a


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    for i in range(len(array)):
        leng_word_array = list(map(lambda x: len(x), array[:]))
    return leng_word_array


# write fizbuzz programm
def fizbuzz():
    return


# Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    list = []
    number_str = str(number)
    for i in number_str:
        list.append(int(i))
    return list


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'
def pigLatin(text):
    text_spit=text.split()
    words_first =text_spit[0]
    words_first = words_first.lower()
    words_first = words_first[1].upper() + words_first[2:] + words_first[0] + 'ay'
    text_pig =words_first

    for words in text_spit[1:]:
        text_pig=text_pig
        words = words.lower()
        words = words[1:] + words[0] + 'ay'
        keep_words = words
        text_pig = text_pig + ' ' + keep_words
    return text_pig


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
        self.assertEqual(length_words(['s', 'ss', '59fk', 'flkj3']), [1, 2, 4, 5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849), [8, 8, 4, 9])
        self.assertEqual(number2digits(4985098), [4, 9, 8, 5, 0, 9, 8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox"), "Hetay uickqay rownbay oxfay")
        self.assertEqual(pigLatin("Quick the brown fox"), "Uickqay hetay rownbay oxfay")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
