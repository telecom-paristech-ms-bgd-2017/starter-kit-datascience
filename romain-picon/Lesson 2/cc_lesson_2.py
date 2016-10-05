import unittest

# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    print('\n--------string_times------------')
    if not isinstance(n, int) or n <= 0:
        return 'n must be a positive integer'
    return n * string


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    if (len(nums) >= 3):
        for numNums in nums[:4]:
            if numNums == 9:
                return True
    return False


# Given a string, return the count of the number of times the 2 last chars will
# appear.
# Two last chars. How many time they appear in the string ?
def last2(string):
    print('\n-------last2---------')
    if len(string) >= 2:
        sub = string[-2:]
        # Generic case
        last2char_count = string.count(sub) - 1
        if sub[0] == sub[1]:
            # More tricky case where xx needs to match xxx
            sub = sub + sub[0]
            last2char_count = last2char_count + string.count(sub)
        return last2char_count
    else:
        return 0


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    i = 0
    word_length_array = [0 for j in range(0, len(array))]

    for word in array:
        word_length_array[i] = len(word)
        i = i +1

    return word_length_array


# write fizbuzz programm
# Écrire un programme qui affiche les nombres de 1 à 199. Mais pour les multiples de 3, afficher “Fizz” au lieu du
# nombre et pour les multiples de 5 afficher “Buzz”. Pour les nombres multiples de 3 et 5, afficher “FizzBuzz”.
def fizbuzz(max=101):

    # skip means will not display the digit
    skip = False
    text = ''
    output = ''

    for i in range(1,max):
        if i%3 == 0:
            text = 'Fizz'
            skip = True
        if i%5 == 0:
            text = text + 'Buzz'
            skip = True

        if skip:
            output = output + text + '\n'
            text = ''
            skip = False
        else:
            output = output + str(i) + '\n'


    return output


# Write a function that takes a number and returns a list of its digits.
def number2digits(number):

    # Get 5 for 35456
    number_digits = len(str(number))
    # Init the returned table
    digits_array = [0 for j in range(0, number_digits)]

    for i in range(1, number_digits+1):
        # 35456 // 10000 = 3
        digits_array[i-1] = number // 10**(number_digits-i)
        # Prepare next digit and pray
        # 35456 - 3 * 10000 = 5456
        number = number - digits_array[i-1]*10**(number_digits-i)


    return digits_array


# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'
def pigLatin(text):

    # "The quick brown fox" -> "Hetay uickqay rownbay oxfay"
    sentence_starts = True
    new_text =''

    for word in text.split():
        new_word = word[1:] + word[0] +'ay'
        if sentence_starts:
            new_word = new_word.capitalize()
            sentence_starts = False
        new_text = new_text + new_word + ' '

    # So our sentence will no finish with ' '
    new_text = new_text.rstrip()
    return new_text


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

    def testfizbuzz(self):
        file_fizzbuzz_res = open('fizzbuzzout.txt')
        fizzbuzz_result = file_fizzbuzz_res.read()
#        print(fizzbuzz_result)
        self.assertEqual(fizbuzz(), fizzbuzz_result)


def main():


    unittest.main()


if __name__ == '__main__':
    main()
