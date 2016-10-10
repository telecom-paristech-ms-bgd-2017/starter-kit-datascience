import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n, int):
        return 'bad argument'
    if not isinstance(string, str):
        return 'bad argument' + string
    if n >= 0:
        return ' '.join([string[:] * n])
    else:
        return "bad argument"


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    print(nums[:max(4, len(nums))])
    return 9 in nums[:min(4, len(nums))]


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    # return string[:-2].count(string[-2:])
    cnt = 0
    idx = 0
    while True:
        idx = string[:-2].find(string[-2:], idx)
        if idx >= 0:
            cnt += 1
            idx += 1
        else:
            break
    return cnt


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    return [len(w) for w in array]


# write fizbuzz programm
# pour multiples de 3, écrire fizz, pour multiples de 5 ecrire buzz, pour multiples de 3 et 5 ecrire fizzbuzz
def fizbuzz():
    result = ''
    for i in range(1, 100):
        if i % 3 == 0 and i % 5 == 0:
            result += 'FizzBuzz'
        elif i % 3 == 0:
            result += 'Fizz'
        elif i % 5 == 0:
            result += 'Buzz'
    print(result)


# Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    if not isinstance(number, int):
        return 'bad argument'
    if number < 0:
        return 'bad argumment'
    return [int(char) for char in str(number)]


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'
def pigLatin(text):
    if not isinstance(text, str):
        return 'bad argument'
    string = ' '.join([word[1:] + word[0].lower() + "ay" for word in text.split(" ")])
    array = string.split(' ')
    array[0] = array[0].capitalize()
    return ' '.join(array)


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

    #
    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox"), "Hetay uickqay rownbay oxfay")


def main():
    unittest.main()
    fizbuzz()


if __name__ == '__main__':
    main()
