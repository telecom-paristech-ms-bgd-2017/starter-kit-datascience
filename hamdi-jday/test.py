# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 08:57:24 2016

@author: hamdi
"""


for n in range(2,10):
    for i in range(2,n):
        if n%i == 0:
            print(n, '= ', i , ' * ' , n/i)
            break
    else:
        print(n, ' est premier')
        
        
squares = [x**2 for x in range(10)]
print(squares)
