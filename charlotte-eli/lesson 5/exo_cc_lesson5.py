import requests
from bs4 import BeautifulSoup
import urllib2
import re
# coding: utf-8


def get_medic(medic):
    r = requests.post("http://base-donnees-publique.medicaments.gouv.fr/index.php", data={'choixRecherche': 'medicament', 'txtCaracteres': medic, 'action': 'show'})
    soup = BeautifulSoup(r.text, "lxml")
    names_medic = soup.findAll('td',{'class':'ResultRowDeno'})
    liste_medoc=[]
    for name in names_medic:
        liste_medoc.append(name.text)
    return liste_medoc
 
ibus =  get_medic('IBUPROFENE')   
#print get_medic('IBUPROFENE')   
    
ibuprofene=[]
for ibu in ibus:
    temp = (re.findall(r'(.*)\s(\d{1,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)\s(\S*)', ibu))
    ibuprofene.append(temp)
    

for i in range(len(ibuprofene)):
    if ibuprofene[i]!=[]:
        print ibuprofene[i][0][0]+ibuprofene[i][0][1]+' '+ibuprofene[i][0][2]+' '+ibuprofene[i][0][3]



