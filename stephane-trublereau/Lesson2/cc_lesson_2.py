import unittest
import numpy as np


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(mot, n):
    #   i = 0
    if not isinstance(n, int):
        return "bad argument n pas entier"
    if not isinstance(mot, str):
        return "bad argument mot "
    if n < 1:
        return "bad argument n negatif "
    print (" String_times : " + n * mot)
    return n * mot


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    #    fonction map
    i = 0
    for i in range(4):
        if nums[i] == 9:
            print (" Trouve_9 : " + str(nums))
            print ("=========================")
            return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
#
# methode reccursive usage memoire non optimise

def trouve(mot, chaine):
    nb = 0
    if len(mot) < 2:
        return 0
    if mot[:2] == chaine:
        nb = 1 + trouve(mot[1:], chaine)
    else:
        nb = trouve(mot[1:], chaine)
    return nb


def trouve2(mot, chaine, nb):
    if len(mot) < 2:
        return nb
    if mot[:2] == chaine:
        nb = nb + 1
    return trouve2(mot[1:], chaine, nb)


def last2(mot):
    finmot = mot[-2:]
    #    print("fin mot : " + finmot)
    debmot = mot[:-2]
    #    print("debut mot : " + debmot)
    #
    # methode 1
    #nombre = trouve(debmot, finmot)
    #print("nombre " + str(nombre))
    #
    # methode 2
    nb = 0
    nombre = trouve2(debmot, finmot, nb)
    print("nombre " + str(nombre))
    return nombre


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    #    lengh[]
    liste = []
    for word in array:
        count = len(word)
        #    print("count :  " + str(count))
        liste.append(count)
    print("Liste : " + str(liste))
    return liste


# write fizbuzz programm
def fizbuzz(n):
    count = 0
    while count < n:
        fizz = not count % 3
        buzz = not count % 5
        if fizz and buzz:
            print("FizzBuzz")
        elif fizz:
            print("Fizz")
        elif buzz:
            print("Buzz")
        else:
            print(count)
        count = count + 1
    return


# Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    liste = list(str(number))
    print("list : " + str(liste))
    return list(map(int, liste))


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'
def pigLatin(text):
    print("texte" + text)
    liste = text.split(" ")
    print (liste)
    result = []
    i = 1
    for mot in liste:
        if len(mot) > 1:
            #            print(mot)
            #            chaineATester.equals(chaineATester.toUpperCase())
            #            newprem = mot[-1:]
            if mot.islower():
                newmot = mot[1:] + mot[0] + "ay"
            else:
                newfirst = mot[1].upper()
                newlast = mot[0].lower()
                newmot = newfirst + mot[2:] + newlast + "ay"
        else:
            newmot = mot
        result.append(newmot)
        #       print(" new mot " + newmot)
        if i < len(mot):
            result.append(" ")
        i = i + 1
    print(result)
    return "".join(result)


# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    def testStringTimes(self):
        print("+ testStringTimes +")
        self.assertEqual(string_times('Hel', 2), 'HelHel')
        self.assertEqual(string_times('Toto', 1), 'Toto')
        self.assertEqual(string_times('P', 4), 'PPPP')

    def testArrayFront9(self):
        print("+ testArrayFront9 +")
        self.assertEqual(array_front9([1, 2, 9, 3, 4]), True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]), False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]), False)

    def testLast2(self):
        print("+ testLast2 +")
        self.assertEqual(last2('hixxhi'), 1)
        self.assertEqual(last2('xaxxaxaxx'), 1)
        self.assertEqual(last2('axxxaaxx'), 2)

    def testLengthWord(self):
        print("+ testLengthWord +")
        self.assertEqual(length_words(['hello', 'toto']), [5, 4])
        self.assertEqual(length_words(['s', 'ss', '59fk', 'flkj3']), [1, 2, 4, 5])

    def testNumber2Digits(self):
        print("+ testNumber2Digits +")
        self.assertEqual(number2digits(8849), [8, 8, 4, 9])
        self.assertEqual(number2digits(4985098), [4, 9, 8, 5, 0, 9, 8])

    def testPigLatin(self):
        print("+ testPigLatin +")
        self.assertEqual(pigLatin("The quick brown fox"), "Hetay uickqay rownbay oxfay")


def main():
    fizbuzz(100)
    unittest.main()


if __name__ == '__main__':
    main()
