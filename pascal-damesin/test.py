# -*- coding: utf-8 -*-
"""
Created on Wed May  4 17:37:03 2016

@author: SIO BAS
"""

def test(a, n=2):
    out = a
    for k in range(1,n):
        out += a
    return out
type(test(0,5))
if test('a')== "aa":
    print("ok")
print("test a = ",test('a'),type(test('a')))
print("test([1,2],1) = ",test([1,2],1),type(test([1,2],1)))
print("test n=10 et a=3 donne ",test(n=10,a=3),type(test(n=10,a=3)))
#test()==None
#print("test () donne ",test(),type(test()))
s="roissy"
#(r,t,u,v,x,y)=enumerate(s))
#print(r,t,u,v,x,y)
def fonction1(s):
    print("%s est de longueur %d" % (s,len(s)))
fonction1([1,2,3])
print(fonction1("test"))
if fonction1("test")==None:
    print("ok")
a=7//float(2)
if a==3.0:
    print(a,"ok")
import time as t
print("t.ctime ",t.ctime())
#print("time.t.ctime ",time.t.ctime())
l=[3,0,1]
print("l1 ",l)
l=l+l[:2]
print (l)
m=l.sort()
#print("l.sort ",l)
#print("m ",m)
l.pop()
#print("l.pop ",l)
print("m ",m)