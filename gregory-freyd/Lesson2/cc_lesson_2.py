import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.
def string_times(string, n):
    if not isinstance(n, int):
        return "bad argument"
    if not isinstance(string, str):
        return "bad argument"

    if n >= 0:
        return n * string

    return string

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    if not isinstance(nums, list):
        print("bad argument")
        return False
    count = 0
    while count < 4 and count < len(nums):
        if nums[count] == 9:
            return True
        count = count + 1
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    if not isinstance(string, str):
        return "bad argument"

    string_pattern_to_find = string[-2:]
    count_occurence = 0
    index = 0
    string_to_look_for_pattern_into = string[:-2]
    while index < len(string_to_look_for_pattern_into) - 1:
        if string_pattern_to_find == string_to_look_for_pattern_into[index] \
                                    + string_to_look_for_pattern_into[index + 1]:
            count_occurence = count_occurence + 1
        index = index +1
    return count_occurence


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    if not isinstance(array, list):
        print("bad argument")
        return []
    int_array = []
    for word in array:
        int_array.append(len(word))
    return int_array

#write fizbuzz programm
def fizbuzz():
    result_string = ''
    for number in range(50):
        if number % 3 == 0:
            print("Fizz", end="")
            result_string = result_string + "Fizz"
        if number % 5 == 0:
            print("Buzz", end="")
            result_string = result_string + "Buzz"
        if number % 3 != 0 and number %5 != 0:
            result_string = result_string + str(number)
            print(number, end="")
        print(", ", end="")
        result_string = result_string + ", "
    return result_string

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    if not isinstance(number, int):
        print("bad argument")
        return []
    number_in_list = []
    number_in_string = str(number)
    for character in number_in_string:
        number_in_list.append(int(character))
    return number_in_list

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    if not isinstance(text, str):
        return "bad argument"

    tab_strings = text.split(" ");
    for index, temp_string in enumerate(tab_strings):
        first_letter_to_move_at_the_end = temp_string[0:1]
        if first_letter_to_move_at_the_end.isupper():   #Handling first letter upper case
            new_first_letter = temp_string[1:2].upper()
            first_letter_to_move_at_the_end = first_letter_to_move_at_the_end.lower()
        else:                                           #No casing change required
            new_first_letter = temp_string[1:2]

        #Pig latinizing
        tab_strings[index] = new_first_letter + temp_string[2:] \
                                   + first_letter_to_move_at_the_end + 'ay'
    s = " " #Restoring spaces between words
    return s.join(tab_strings)

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
    fizbuzz()
    unittest.main()

if __name__ == '__main__':
    main()
