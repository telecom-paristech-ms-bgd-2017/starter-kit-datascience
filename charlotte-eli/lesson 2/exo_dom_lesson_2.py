import requests
from bs4 import BeautifulSoup
import urllib2
# coding: utf-8

#http://alize2.finances.gouv.fr/communes/eneuro/tableau.php?icom=118&dep=014&type=BPS&param=0&comm=0&exercice=2014


def getdata(icom,departement, year):
    r = requests.post("http://alize2.finances.gouv.fr/communes/eneuro/tableau.php", {'ICOM': icom, 'DEP': departement, 'TYPE': 'BPS', 'PARAM': '0',
                                                                                     'dep': '', 'reg': '', 'nomdep': '', 'moysst': '', 'exercice': '', 'param': '', 'type': '', 'siren': '', 'comm': '0', 'EXERCICE': year})
    soup = BeautifulSoup(r.text.encode("utf8").decode(
        'ascii', 'ignore'), 'html.parser')

    labels = soup.findAll('td', {"class": "libellepetit"})
    interesting_idx = [2,3,5,6]
    labels = [labels[i] for i in interesting_idx]
    
    print "***************"+ " Year = " + year + "***************"
    #print "******************************************************"

    for label in labels:
        print label.text.encode("utf8").decode('ascii', 'ignore').strip()
        temp1 = label.findNextSibling()
        print 'En euros par habitant ' + temp1.findNextSibling().string.strip()
        temp2 = temp1.findNextSibling()
        print 'Moyenne de la strate ' + temp2.findNextSibling().string.strip()
    
    #print "******************************************************"
        

        


years =['2008','2009','2010','2011','2012','2013','2014','2015']

print "*********************PARIS**************************"
for year in years:
    getdata('056','075',str(year))
    
print "******************END PARIS***************"

print "*********************CAEN*****************"
for year in years:
    getdata('118','014',str(year))
    
print "******************END CAEN**************************"
        
    

    
    
