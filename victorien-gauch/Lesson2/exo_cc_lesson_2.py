import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    return n * string

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):

    for i in nums[:4]:
        if i == 9:
            return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
 #return string.count(string[-2:]) - 1
def last2(string):
    
    last2 = string[len(string)-2:]
    count = 0
   
    for i in range(len(string)-2):
        sub = string[i:i+2]
        if sub == last2:
            count = count + 1
 
    return count
    


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    len_tab = []

    for word in array:
        len_tab.append(len(word))
    return len_tab

#write fizbuzz programm
def fizbuzz(n):
    for i in range(0,n):
        if i % 15 == 0:
            print('Fizbuzz')
        elif i % 5 == 0:
            print('Buzz')
        elif i % 3 == 0:
            print('Fiz')


#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    string = str(number)
    digits = []

    for digit in string:
        digits.append (int(digit))
    return digits

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):

    text = text.lower().split()
    result = ''
    for i in text:
        i = i + "%say" % (i[0]) 
        i = i[1:]
        result += i + ' '
    return (result[0].upper() + result[1:]).strip()

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

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
