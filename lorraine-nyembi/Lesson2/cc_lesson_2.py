import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.
def string_times(string, n):
    if not isinstance(n , int):     #if n n'est pas un entier
        return "bad argument"
    if not isinstance(string , str):    #if string n'est pas une chaine de caractères
        return "bad argument"  * string
       
    return string * n



# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    return_value = False
    if(len(nums) >= 4):
        for num in nums[0:3]:
            if num == 9:
                return_value = True
            else:
                return_value = False
    return return_value


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    count = 0
    size = len(string) - 2      #on enlève les 2 derniers caractères de la chaine
    if len(string) > 4:
        for i in range(0, size - 1):    #par rappor à C, python tient compte du size-ième terme même si on part de 0
            if string[i:(i + 2)] == string[-2:]:
                count += 1
    return count


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    int_array = []
    # contenu de map
    # à tout variable word, on associe la fonction 'len'
    # f:x inclus dans array, on asscie f(x) = list(len(x)).
    int_array = list(map(lambda word: len(word), array))
    return int_array 


#write fizbuzz programm
def fizbuzz():
  while True:
    try:
        value = int(input("Give me a number : "))
    except ValueError:
        print('Could you at least give me an actual number?')
        continue

    if value % 3 == 0 and value % 5 == 0:
     print('fizbuzz')
    elif value % 3 == 0:
     print('fizz')
    elif value % 5 == 0:
     print('buzz')
    else:
      print ('is not fizbuzz')
      break

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    l_of_digits = []
    for char in str(number):
        l_of_digits.append(int(char))
    return l_of_digits

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def make_pig(word):
    new_word = word[1:len(word)] + (word[:1]).lower() + 'ay'
    return new_word

def pigLatin(text):
    
    new_text = ''
    split_text_list = text.split()    
    list_after_make_pig = list(map(lambda word: make_pig(word), split_text_list))
    for pig_word in list_after_make_pig:
        new_text += pig_word + ' '

    return new_text[0:1].upper() + new_text[1:len(new_text)-1]



# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase): #heritage => chercher unittest python

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
    #fizbuzz()
    

if __name__ == '__main__':
    main()
