# coding: utf8



import urllib2
from bs4 import BeautifulSoup
import numpy as np


def     extract_pourcentages(adress):

    html = urllib2.urlopen(adress).read()
    soup = BeautifulSoup(html)

    prdt=[]
    prices=[]

    for a in range(len(soup.find_all(class_='prdtBZPrice'))):
        prices.append(float(soup.find_all(class_='prdtBZPrice')[a].find_all(class_='price')[0].text.split('<span class="price">')[0].encode("utf8").replace('€','.')))
        if len(soup.find_all(class_='prdtBZPrice')[a].find_all(class_='prdtPrSt'))>0:
            try :
                prdt.append(float(soup.find_all(class_='prdtBZPrice')[a].find_all(class_='prdtPrSt')[0].text.split('<div class="prdtPrSt">')[0].encode("utf8").replace(',','.')))
            except:
                if len(soup.find_all(class_='prdtBZPrice')[a].find_all(class_='prdtPrSt')[0].text.split('<div class="prdtPrSt">')[0].encode("utf8").replace(',','.'))<1:
                    prdt.append(0.0)
                else:
                    print 'big error'
                    raw_input()
        else:
            prdt.append(0.0)

    pourcentages_remise=[(prdt[a]-prices[a])/prices[a] if prdt[a]!=0 else 0.0   for a in range(len(prdt))]
    return pourcentages_remise

##############################################################################################


web_address1='http://www.cdiscount.com/search/10/dell.html#_his_'
web_address2='http://www.cdiscount.com/search/10/acer.html#_his_'
adresses=[web_address1,web_address2]

for adress in adresses:
    pourcentages=extract_pourcentages(adress)
    print adress
    print np.mean(pourcentages)
    print '-----------------'
    
