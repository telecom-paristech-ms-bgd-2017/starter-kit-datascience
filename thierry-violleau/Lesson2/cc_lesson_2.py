import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    #    if not isinstance(n, int):
    #        raise ValueError
    return string * n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.


def array_front9(nums):
    return 9 in nums[0:4]


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count
# the end substring).
def last2(string):
    # return string[:-2].count(string[-2:]) # does not count overlapping substrings
    string, sub_string = string[:-2], string[-2:]
    return sum(1 for i in range(len(string)) if string.startswith(sub_string, i))

# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.


def length_words(array):
    return list(map(lambda e: len(e), array))

# write fizbuzz programm
# The FizzBuzz Challenge: Display numbers from 1 to x, replacing the word
# 'fizz' for multiples of 3, 'buzz' for multiples of 5 and 'fizzbuzz' for
# multiples of both 3 and 5. Th result must be:1 2 fizz 4 buzz fizz 7 8
# fizz buzz 11 fizz 13 14 fizzbuzz 16 ...


def fizbuzz(x=100):
    return list(map(lambda i: 'buzz' if type(i) is int and i % 5 == 0 else i,
                    map(lambda i: 'fizz' if type(i) is int and i % 3 == 0 else i,
                        map(lambda i: 'fizzbuz' if type(i) is int and i % 3 == 0 and i % 5 == 0 else i, range(1, x)))))

# Write a function that takes a number and returns a list of its digits.


def number2digits(number):
    # return [int(c) for c in str(number)]
    return list(map(lambda c: int(c), str(number)))

# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'


def pigLatin(text):
    # return ' '.join(list(map(lambda w: w[1:] + w[0] + 'ay', text.split())))
    conv_case = lambda c1, c2: c2.upper() if c1.isupper() else c2.lower()
    return ' '.join(list(map(lambda w: conv_case(w[0], w[1]) + w[2:] + conv_case(w[1], w[0]) + 'ay', text.split())))

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

    def testFizbuzz(self):
        self.assertTrue(
            fizbuzz(15), [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuz'])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
