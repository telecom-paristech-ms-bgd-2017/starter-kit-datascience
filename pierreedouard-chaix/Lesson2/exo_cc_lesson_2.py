import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n, int):
        return 'bad argument'
    if not isinstance(string, str):
        return 'bad argument'

    if n >= 0:
        return string * n
    else:
        return 'bad argument'

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    res = False
    for i in range(0, min(len(nums), 4)):
        if nums[i] == 9: res = True
    return res


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    if(len(string) < 2): return 'Pas assez de caracteres en input'
    else:
        tomatch = string[-2:]
        count = 0
        for i in range(0, len(string)-2):
            if string[i:i+2] == tomatch: count = count + 1
    return count


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    res = []
    for word in array:
        res.append(len(word))
    return res

#write fizbuzz programm
def fizbuzz(N):
  for i in range(1, N+1):
      if i % 15 == 0 : print str(i) + " fizbuzz"
      elif i % 5 == 0 : print str(i) + " buzz"
      elif i % 3 == 0 : print str(i) + " fiz"
      else: print str(i)

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
  nstr = str(number)
  a = []
  for i in range(0, len(nstr)):
      a.append(int(nstr[i]))
  return a

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
  textsplit = text.split(" ")
  newwords = []
  for word in textsplit:
      maj = word[0].upper() == word[0]
      if(len(word) == 1): newwords.append(word + "ay")
      if(len(word) == 2):
          newwords.append(majoupas(word[1], maj) + word[0].lower() + "ay")
      if(len(word) > 2):
          newwords.append(majoupas(word[1], maj) + word[2:len(word)] + word[0].lower() + "ay")
  res = ""
  for word in newwords:
      res = res + word + " "
  return res[0:len(res)-1]

def majoupas(s, b):
    if b == True: return s.upper()
    else: return s

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
        self.assertEqual(last2('xxx') , 1)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")



def main():
    fizbuzz(50)
    unittest.main()


if __name__ == '__main__':
    main()

