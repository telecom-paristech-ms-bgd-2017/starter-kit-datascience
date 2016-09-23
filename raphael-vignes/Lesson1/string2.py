def verbing(s):
  if s.__len__() >= 3:
      print(s[-3:])
      if s[-3:] != 'ing':
          s+='ing'
      else:
          s+= 'ly'
  return s


def not_bad(s):
  if 'not' in s and 'bad' in s:
      a = s.find('not')
      b = s.find('bad')
      if a < b :
          return s[:a] + 'good' +s[b+3:]
  return s


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
    if len(a) % 2 == 0:
        middleA = int(len(a)/2)
    else:
        middleA = int(len(a)/2 +1)
    if len(b) % 2 == 0:
        middleB = int(len(b)/2)
    else:
        middleB = int(len(b)/2+1)
    return a[:middleA] + b[:middleB] + a[middleA:] + b[middleB:]




# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print(prefix+" Got : "+repr(got)+" Expected : " +repr(expected))



# main() calls the above functions with interesting inputs,
# using the above test() to check if the result is correct or not.
def main():
  print('verbing')
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print
  print('not_bad')
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

  print
  print('front_back')
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')

if __name__ == '__main__':
  main()
