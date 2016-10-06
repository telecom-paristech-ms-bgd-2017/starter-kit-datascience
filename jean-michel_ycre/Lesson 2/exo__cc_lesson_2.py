import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):

    if n < 0 or not isinstance(n, int):
        print('n doit être un entier positif ou nul')
        return
    return n*string

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):

    for i in range(min(3, len(nums))):
        if nums[i] == 9:
            return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):

    test = string[-2:]
    counter = 0
    for i in range(len(string)-2):
            if string[i:i+2] == test:
                counter += 1
    return counter


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):

    longueur = []
    for i in array:
        longueur.append(len(i))
    return longueur

#Write a program that prints the numbers from 1 to 100. But for multiples of three print "Fizz" instead of #the number and for the multiples of five print "Buzz". For numbers which are multiples of both three and #five print "FizzBuzz".
def fizbuzz():
    for i in range(1,101):
        if i%15 == 0:
            print('FizzBuzz')
            continue
        if i%3 == 0:
            print('Fizz')
            continue
        if i%5 == 0:
            print('Buzz')
            continue
        print(i)
    return print('Done')

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):

    maliste = list(str(number))
    maliste = [int(i) for i in maliste]
    return maliste

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):

    mon_texte = text.split(' ')
    traduction = ""
    for i in mon_texte:
        if not i.endswith('ay'):
            traduction += i[1:].lower() + i[0].lower() + 'ay' + ' '
        else:
            traduction += i[-3].lower() + i[0:-3].lower() + ' '
    traduction = traduction[0].upper() + traduction[1:-1]
    return traduction


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
    unittest.main()

if __name__ == '__main__':
    main()
