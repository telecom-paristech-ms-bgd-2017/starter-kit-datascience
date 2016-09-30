import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.
def string_times(string, n):
    return string * n


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    for i, num in enumerate(nums):
        if i == 3:
            return False
        if num == 9:
            return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    res = 0
    last = string[-2:]
    for k in range(len(string[:-2])):
        if last == string[k:k+2]:
            res += 1
    return res


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(words):
    l = []
    for word in words:
        l.append(len(word))
    return l


# write fizbuzz programm
def fizbuzz(n):
    if n % 3 == 0:
        print "Fizz"
    elif n % 5 == 0:
        print "Buzz"
    elif n % 15 == 0:
        print "FizzBuzz"


# Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    return map(int, list(str(number)))


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'
def pigLatin(text):
    pig = ''
    words = text.split()
    for word in words:
        pig += word[1:].lower() + word[0].lower() +'ay' + ' '
    return pig[0].upper() + pig[1:-1]


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


def main():
    unittest.main()
    print last2('hixxhi')


if __name__ == '__main__':
    main()
