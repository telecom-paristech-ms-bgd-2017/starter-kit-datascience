import unittest

#Python version 3, Audrey Quessada-Vial test fini le 01/10/2016
# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if  n < 0:
        print('choose a positive number')
    elif type(string) is not str :
        print('enter a string')
    else:
       s = n * string
    return s

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    boo = True
    n_length = len(nums)
    if n_length < 4 :
        nums.append([0])
    else:
        for el in nums[0:3]:
            if el != 9 :
               boo = False
            else:
                boo = True
    return boo


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    s_last2 = string[-2:]
    s_length = len(string)-2
    count = 0
    for i in range(0, s_length):
        el = string[i]+string[i+1]
        if el == s_last2:
            count += 1
    return count


#Write a program that maps a list of words into a list of
#integers representing the lengths of the corresponding words.
def length_words(array):
    ln_w = []
    for el in array:
        count = len(el)
        ln_w.append (count)
    print(ln_w)
    return ln_w

#write fizbuzz programm
def fizbuzz(number):
    my_list = []
    for i in range(number):
        if i % 3 == 0 and i % 5 == 0:
            my_list.append((i, 'fizzbuzz'))
        elif i % 5 == 0:
            my_list.append((i, 'buzz'))
        elif i % 3 == 0:
            my_list.append((i, 'fizz'))
    return my_list

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    conv = []
    for el in str(number):
        conv.append(int(el))
    print(conv)
    return conv

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    txt_not_latin = text.split(" ")
    txt_latin = ''
    for el in txt_not_latin:
        if el == txt_not_latin[0]:
            if len(el) == 1:
                a = el
                a += 'ay '
            elif len(el) == 2:
                a = el[1].upper() + el[0].lower()
                a += 'ay '
            else:
                a = el[1].upper() + el[2:] + el[0].lower()
                a += 'ay '
            txt_latin += a
        elif el == txt_not_latin[-1]:
            if len(el) == 1:
                a = el
                a += 'ay'
            elif len(el) == 2:
                a = el[1] + el[0].lower()
                a += 'ay'
            else:
                a = el[1] + el[2:] + el[0].lower()
                a += 'ay'
            txt_latin += a
        else:
            if len(el) == 1:
                a = el
                a += 'ay '
            elif len(el) == 2:
                a = el[1] + el[0].lower()
                a += 'ay '
                txt_latin += a
            else:
                a = el[1] + el[2:]+el[0].lower()
                a += 'ay '
            txt_latin += a
    return txt_latin

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