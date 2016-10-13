import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):  ########## OK ############
    # pour verifier que c'est bien un int :
    if not isinstance(n, int):
        return 'bad argument' + n
    if not isinstance(string, str):
        return 'bad argument' + string
    if n >= 0:
        return string * n


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):  ########## OK ############
    b = False
    for i in range(4):
        if nums[i] == 9:
            b = True
    return b


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count
# the end substring).

# on prend les 2 derniers caracteres et on parcourt et on compte le nombre
# de fois que ca apparait
# ATTENTION : on ne compte pas la derniere occurence !!!

def last2(string):  ########## OK ############
    last = string[-2:]
    # print last
    count = 0
    for i in range(len(string)-2):
        #print ("test :", string[i]+string[i+1])
        if (string[i]+string[i+1]) == last:
            count = count+1


            # print count
    return count


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.

# utiliser la fonction map()
# Exemple de Charles : map(['totot', 'tu'], lambda x : len(x) ) 

def length_words(array):   ########## OK ############
    return list(map (lambda x : len(x), array))

# write fizbuzz programm

# correction en ligne => regarder sur internet ce que ca fait

# Ecrire un programme qui affiche les nombres de 1 a 199. 
# Mais pour les multiples de 3, afficher "Fizz" au lieu du nombre et pour 
# les multiples de 5 afficher "Buzz". Pour les nombres multiples de 3 et 5, 
# afficher "FizzBuzz".

def fizbuzz():  ########## OK ############
	for i in range(200) : 
		if i%5==0 and i%3==0 : 
			print i, " FizzBuzz"
		elif i%3==0 : 
			print i, " Fizz"
		elif i%5==0 : 
			print i, " Buzz"

# Write a function that takes a number and returns a list of its digits.

def number2digits(number):   ########## OK ############
    liste = []
    for element in str(number) : 
    	liste.append(int(element))
    return liste

# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'

def pigLatin(text):     ########## OK ############
	t=text.split(" ")
	final=""
	for el in t : 
		sauv=el[0]
		el=el+sauv+"ay"
		el=el[1:]
		final = final + " "+ el
	# on met tout en minuscule 
	final=final.lower()
	# on retire l'espace qui est en trop au debut (ou qui aurait pu etre a la fin)
	final=final.strip()
	# on met la premiere lettre en maj
	final=final.replace(final[0],final[0].upper())
	return final

# Here's our "unit tests".


class Lesson1Tests(unittest.TestCase):

    #    def testArrayFront9(self):
    #        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
    #        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
    #        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    #    def testStringTimes(self):
    #        self.assertEqual(string_times('Hel', 2),'HelHel' )
    #        self.assertEqual(string_times('Toto', 1),'Toto' )
    #        self.assertEqual(string_times('P', 4),'PPPP' )

    #    def testLast2(self):
    #        self.assertEqual(last2('hixxhi'), 1)
    #        self.assertEqual(last2('xaxxaxaxx'), 1)
    #        self.assertEqual(last2('axxxaaxx'), 2)

 	#   def testLengthWord(self):
 	#       self.assertEqual(length_words(['hello','toto']) , [5,4])
 	#       self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

 	#		print fizbuzz() 

    #    def testNumber2Digits(self):
    #        self.assertEqual(number2digits(8849) , [8,8,4,9])
    #        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

        def testPigLatin(self):
     		self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")


def main():
    unittest.main()

if __name__ == '__main__':
    main()
