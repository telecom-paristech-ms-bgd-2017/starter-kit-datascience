import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n,int):
        return 'bad argument'
    if not isinstance(string,str):
        return 'bad argument'
    if n>=0:
        return string * n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    if len(nums)<4:
        if 9 in nums:
            return True
        else :
            return False
    else:
        if 9 in nums[:5]:
            return True
        else:
            return False



# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    if len(string) < 2:
        print("Error: string is too short")

    end_char = string[-2:]
    count=0
    for i in range(len(string)-3):
        if string[i,i+2]==end_char:
            count +=1
    return count


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    ## Utiliser la fonction map
    return list(map(lambda x : len(x), array))

#write fizbuzz programm
def fizbuzz():
    s = ""
    for i in xrange(1,101):
        if i%15 == 0:
            s += "fizbuzz"
        elif i%3 == 0:
            s += "fiz"
        elif i%5 == 0:
            s+= "buzz"
        else:
            s+= str(i)
    return s


#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    return [int(i) for i in str(number)]

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    listeText = text.split(' ')
    return ' '.join([word[1:] + word[0] + 'ay' for word in listeText]).capitalize()


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
