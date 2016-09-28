# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 13:44:20 2016

@author: Stephan
"""

# A. donuts
def donuts(count):
    if count<10:
        return 'Number of donuts: %s' % (count)
    else :
        return 'Number of donuts: many'

# B. both_ends

def both_ends(s):
    if len(s)>2:
        s2=s[:2]+s[-2:]
        return '%s' % (s2)
    else :
        return ""

# C. fix_start
def fix_start(s):
    if len(s)>1:
        b=s.replace(s[0],"*")
        return s[0]+b[1:]
    else :
        return ''
    
# D. MixUp
def mix_up(a,b):
    if len(a)>1 and len(b)>1:
        c=a[0:2]+b[2:]
        d=b[0:2]+a[2:]
        return '%s %s' % (d,c)
    else :    
        return ''   

# Provided simple test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print ('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main(): 
  print ('donuts')
  # Each line calls donuts, compares its result to the expected for that call.
  test(donuts(4), 'Number of donuts: 4')
  test(donuts(9), 'Number of donuts: 9')
  test(donuts(10), 'Number of donuts: many')
  test(donuts(99), 'Number of donuts: many')

  print
  print ('both_ends')
  test(both_ends('spring'), 'spng')
  test(both_ends('Hello'), 'Helo')
  test(both_ends('a'), '')
  test(both_ends('xyz'), 'xyyz')

  
  print
  print ('fix_start')
  test(fix_start('babble'), 'ba**le')
  test(fix_start('aardvark'), 'a*rdv*rk')
  test(fix_start('google'), 'goo*le')
  test(fix_start('donut'), 'donut')

  print
  print ('mix_up')
  test(mix_up('mix', 'pod'), 'pox mid')
  test(mix_up('dog', 'dinner'), 'dig donner')
  test(mix_up('gnash', 'sport'), 'spash gnort')
  test(mix_up('pezzy', 'firm'), 'fizzy perm')


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
