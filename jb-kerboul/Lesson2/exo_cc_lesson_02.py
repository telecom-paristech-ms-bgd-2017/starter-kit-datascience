import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    return string*n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.


def array_front9(nums):
    is9 = any([ii == 9 for ii in nums[:min([4, len(nums)])]])
    return is9


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count
# the end substring).
def last2(string):
    count = sum([string[y: y + 2] == string[-2:]
                 for y in range(len(string)-2)])
    return count


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    return [len(ii) for ii in array]
# write fizbuzz programm


def fizbuzz():
    f = lambda x: 'fizz' if x % 3 == 0 else ''
    b = lambda x: 'buzz' if x % 5 == 0 else ''
    n = lambda x: str(x) if x % 5 != 0 and x % 3 != 0 else ''
    test = [f(ii)+b(ii)+n(ii) for ii in range(1, 101)]
    return ' '.join(test)

# Write a function that takes a number and returns a list of its digits.


def number2digits(number):
    nSTr = str(number)
    return [int(ii) for ii in nSTr]

# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'


def pigLatin(text):

    c = (lambda x: x[1:] + x[0]+'ay' if x[0].islower()
         else x[1:].capitalize() + x[0].lower() + 'ay')

    newstr = [c(ii) for ii in text.strip().split()]
    return ' '.join(newstr).rstrip()

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
        self.assertEqual(
            length_words(['s', 'ss', '59fk', 'flkj3']), [1, 2, 4, 5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849), [8, 8, 4, 9])
        self.assertEqual(number2digits(4985098), [4, 9, 8, 5, 0, 9, 8])

    def testPigLatin(self):
        self.assertEqual(
            pigLatin("The quick brown fox"), "Hetay uickqay rownbay oxfay")


def main():
    unittest.main()

if __name__ == '__main__':
    main()
