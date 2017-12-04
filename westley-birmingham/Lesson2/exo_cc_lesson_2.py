import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n, int):
        return 'bad argument'
    if not isinstance(string, str):
        return 'bad argument ' + string
    if n >= 0:
        return n * string


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    for el in nums[:4:]:
        if el == 9:
            return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    i = 0
    j = 0
    while j < len(string[:-2]):
        if string[j] == string[-2:][0] and string[j+1] == string[-2:][1]:
            i += 1
        j += 1
    return i


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    return list(map(lambda x: len(x), array))


#write fizbuzz programm
def fizbuzz():
    number = []
    for el in range(1,100):
        if el % 3 == 0:
            if el % 5 == 0:
                number.append('fizbuzz')
            else:
                number.append('fiz')
        elif el % 5 == 0:
            number.append('buzz')
        else:
            number.append(el)
    return number


#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    num = []
    for el in str(number):
        num.append(int(el))
    return num


#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    newtext = ""
    for el in text.split():
        if len(newtext) == 0:
            newtext += el[1:2].upper() + el[2:].lower() + el[:1].lower() + "ay"
        else:
            newtext += ' '
            newtext += el[1:].lower() + el[:1].lower() + "ay"
    return newtext


# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]), True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]), False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]), False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2), 'HelHel' )
        self.assertEqual(string_times('Toto', 1), 'Toto' )
        self.assertEqual(string_times('P', 4), 'PPPP' )

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
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")


def main():
    unittest.main()

if __name__ == '__main__':
    main()
