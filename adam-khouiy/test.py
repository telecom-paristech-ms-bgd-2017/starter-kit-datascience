''''a = ['a', 'b', 'c']
x = [-1, 1, 0]
c = [a, x]
#print(c)

print(c[1][0])

#print(list(range(2, 2)))


def chercher(n):
    for n in range(2, 15):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n // x)
                break
        else:
            # loop fell through without finding a factor
            print(n, 'is a prime number')





def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)


i = [50,30]

def  concat(*l,sep="/"):
        return sep.join(l)

print(concat("k","n","j","l"))

squares =[]

squares = [x**2  for x in range(10)]

print(squares)
squares2 =[]

squares2 = list(map(lambda x : x**2 ,range(5)))

print(squares2)

print ([(x,y) for x in [0,1,2] for y in [1,2,3] if x==y])

vec = [[1,2,3], [4,5,6], [7,8,9]]
print ([num for i in vec for num in i])

a = set('abracadabra')
b ={"adam","amine","adam","ghita"}
print (b)

string1, string2, string3 = 'ff', 'Trondheim', ''
non_null =  string1 or string2 or string3

print(non_null)

#print ((1, 2, 3, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4))

string ="ma da md"

print(int(7/2))
'''
def words_count (fileName):

    r = open(fileName, encoding="utf8")
    words = r.read().split()
    word = {}

    for w in words:
        if (w.lower() in word.keys()):
            word[w.lower()] = word[w.lower()] + 1
        else:

            word[w.lower()] =  1
    return (word)

def print_words (filename):

    word_s = (words_count(filename))
    word_s_keys = sorted(word_s.keys())
    for i in word_s_keys:
        print(i , word_s[i])

def print_top(filename):

    words= (words_count(filename))


    items = sorted(words.keys(),key= lambda  x : words[x], reverse=True)

    for item in items[:2]:
        print(item)

def get_count(word_count_tuple):
  """Returns the count from a dict word/count tuple  -- used for custom sort."""
  return word_count_tuple[1]

def print_top_s(filename):
  """Prints the top count listing for the given file."""
  word_count = words_count(filename)

  # Each item is a (word, count) tuple.
  # Sort them so the big counts are first using key=get_count() to extract count.
  items = sorted(word_count.items(), key= lambda w : w[1], reverse=True)

  # Print the first 20
  for item in items[:20]:
    print (item[0], item[1])



def method1(list,search_age):
    for age in list.values():
            if int(age) == int(search_age):
                    return list.keys()




if __name__ == '__main__':
    import re
    fileName = r"C:\Users\adam\Desktop\python\basic\small.txt"

    #print_words(fileName)

    #print_top(fileName)
    print_top_s(fileName)

    print( re.search(r'\b\d+', 'he33llo 42 I\'m a 32 string 30'))