# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# que vaut 100 euros à 1.025% ds 10 ans

import matplotlib.pyplot as plt
u = 100
r = 2.5/100
n = range(11)
l = []


def f(x):
    for i in n:
        g = u*((1+r)**i)
        l.append(g)        
f(n)
print('\n')
print(l)

plt.title("suite")
plt.xlabel("i")
plt.ylabel("g")
plt.plot(l)
