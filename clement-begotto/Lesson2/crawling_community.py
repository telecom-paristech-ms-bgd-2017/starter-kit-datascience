import requests
from bs4 import BeautifulSoup
   
def getFinancials(id_commune, id_departement, year):
    ville = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' 
                            + "%03d"%id_commune + '&dep=' + "%03d"%id_departement 
                            + '&type=BPS&param=5&exercice=' + str(year) )
    soup = BeautifulSoup(ville.text, 'html.parser')
    hashmap = {}
    for x in soup.find_all('tr') :
        if x.find_all(class_="libellepetit G") != [] and "TOTAL DES " in x.find_all(class_="libellepetit G")[0].text:
            title =  x.find_all(class_="libellepetit G")[0].text.split('>')[0].split(' = ')[0]
            hashmap[title] = ( x.find_all(class_="montantpetit G")[1].text.replace('\xa0',''), 
                                        x.find_all(class_="montantpetit G")[2].text.replace('\xa0','') ) 
    return hashmap

for i in range(2009,2014):
    print( getFinancials(118, 14, i) )
    print( getFinancials(56, 75, i) )
