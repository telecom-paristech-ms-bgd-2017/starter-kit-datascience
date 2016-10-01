import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    return string * n


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    bol =False
    for i in nums[:3]:
        if (i == 9):
            bol =True
    return bol

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):

    return len([n for n in range(len(string [:-2])) if string.find(string[-2:], n) == n])


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    len_word = []
    for word in array:
        len_word.append(len(word))

    return len_word


# write fizbuzz programm
def fizbuzz(chiffre):
    string = ""
    if chiffre % 3 and not chiffre % 5:
        string = "fiz"
    elif chiffre % 5 and not chiffre % 3:
        string = "buzz"
    elif chiffre % 3 and chiffre % 5:
        string = "fizbuzz"
    return string


# Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    return [int(d) for d in str(number)]


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'
def pigLatin(text):
    list = text.split()
    ret_lis = []
    i =0
    for word in list:
        i = i+1
        if i==1:
           word = word[1:2].upper()+word[2:len(word)]+word[0:1].lower() + "ay"
           ret_lis.append(word)
        else :
            word = word[1:len(word)] + word[0:1].lower() + "ay"
            ret_lis.append(word)
        if i<len(list):
            ret_lis.append(" ")

    return "".join(ret_lis)


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


if __name__ == '__main__':
    main()
