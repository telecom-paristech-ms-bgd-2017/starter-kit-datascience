# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 00:28:07 2016

@author: laura
"""
 
import urllib.request
from bs4 import BeautifulSoup

def get_top_github():   
    #read file
    url = "https://gist.github.com/paulmillr/2657075"
    s = urllib.request.urlopen(url).read()

    #make soup
    soup = BeautifulSoup(s,"html.parser")
    res=soup.find_all("td")
    #les multiple de 4 donne le nom
    #0 nom
    #1 contrib
    #2 location
    #3 picture
    print("ranking-------name----------user")
    for i in range(0,len(res),4):
        #print(res[i].find("a").text) #pseudo
        rank=i
        pseudo=res[i].find("a").text
        debut=str(res[i]).find("(")
        fin=str(res[i]).find(")")
        ligne=str(res[i])
        name=ligne[debut+1:fin]
        if debut==-1:
            name=pseudo
        print(int(i/4+1),"--  ",name," --  ",pseudo)
    
get_top_github()