import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    string_t=''
    
    """print 'idule\n '
    print n
    print string*n
    print string
    raw_input()
    """
    if not isinstance( n, int ):
        raise NameError('n not an int ')

    if not isinstance( string, str ):
        raise NameError('string not a string ')

    """raw_input()
    for i in range(n):
        string_t=string_t+string
    print string_t
    print 'lalaa'
    raw_input()
    print n
    print string
    raw_input()
    """
    return string*n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    """print nums
    
    print [nums[i]==9 for i in range(len(nums))]
    print sum([nums[i]==9 for i in range(len(nums))])
    """
    N=len(nums)
    M=min([N,4])
    """raw_input()
    print 'badoul'
    """                                
    return sum([nums[i]==9 for i in range(M)])


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).


def last2(string):
    """wrds=string.split()
    print wrds
    raw_input()
    """
    
    '''print '\n'
    print string
    #print string[-2:]
    print [string[-2:]==string[i:i+2] for i in range(len(string))]
    print sum([string[-2:]==string[i:i+2] for i in range(len(string))])-1
    raw_input()
    '''
    return sum([string[-2:]==string[i:i+2] for i in range(len(string))])-1


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    """
    print '\n bidule'
    print map(lambda x: len(x),array)
    raw_input()
    """
    return map(lambda x: len(x),array)

#write fizbuzz programm

''' Display numbers from 1 to x, replacing the word 'fizz' for multiples of 3, 'buzz' for
 multiples of 5 and 'fizzbuzz' for multiples of both 3 and 5. Th result must be:1 2 fizz 
4 buzz fizz 7 8 fizz buzz 11 fizz 13 14 fizzbuzz 16 ...
'''

def fizbuzz(N):
    #    N=25
    list_new=[]
    for i in range(N):
        if i%3==0:
            if i%5==0:
                #print 'fizzbuzz'# if i%3==0 and i%5==0 for i in range(N) )]
                list_new.append('fizzbuzz')
            else:
                #print 'fizz'
                list_new.append('fizz')
        else:
            if i%5==0:
                #                print 'buzz'
                list_new.append('buzz')
            else:
                #                print i
                list_new.append(i)
                #    raw_input()
                #    print list_new
                #    raw_input()
    return list_new

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    #    print [a for a in number.__str__()]
    #raw_input()
    return [int(a) for a in number.__str__()]

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    """print [a[1:]+a[0]+'ay' for a in text.split()]
    print ' '.join([a[1:]+a[0]+'ay' for a in text.split()])
    raw_input()
    """
    string_bud=' '.join([a[1:]+a[0].lower()+'ay' for a in text.split()])
    rosebud=string_bud[0].upper()+string_bud[1:]
    return rosebud
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

    def testfizbuzz(self):
        self.assertEqual(fizbuzz(6) , ['fizzbuzz',1,2,'fizz',4,'buzz'])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
