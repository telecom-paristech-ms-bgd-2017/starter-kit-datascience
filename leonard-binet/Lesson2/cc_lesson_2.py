# pour python 3
import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n, int):
        return "Mauvais argument"
    if not isinstance(string, str):
        return "Mauvais string"
    if n >= 0:
        return string * n
    else:
        return "Mauvais nombre"

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.


def array_front9(nums):
    result = False
    for num in nums[:min(len(nums), 4)]:
        if int(num) == 9:
            result = True
    return result


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end
# substring).


def last2(string):
    count = 0
    if len(string) <= 3:
        return 0
    pattern = string[-2:]
    for i in range(len(string) - 4):
        if string[i:i+2] == pattern:
            count += 1
    return count


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.


def length_words(array):
    return list(map(lambda x: len(x), array))


# write fizbuzz programm
def fizbuzz():
    # Écrire un programme qui affiche les nombres de 1 à 199. Mais pour les
    # multiples de 3, afficher “Fizz” au lieu du nombre et pour les multiples
    # de 5 afficher “Buzz”. Pour les nombres multiples de 3 et 5, afficher
    # “FizzBuzz”.
    for i in range(200):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

# Write a function that takes a number and returns a list of its digits.


def number2digits(number):
    result = list(str(number))
    result = list(map(lambda x: int(x), result))
    return result


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'


def pigLatin(text):
    mots = text.split(" ")
    result = mots[0][1:]+mots[0][0]+'ay'
    for mot in mots[1:]:
        result = " ".join((result, mot[1:]+mot[0]+'ay'))
    result = result[0].upper()+result[1:].lower()
    return result


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

    def testFizzBuzz(self):
        self.assertEqual(fizbuzz(), None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
