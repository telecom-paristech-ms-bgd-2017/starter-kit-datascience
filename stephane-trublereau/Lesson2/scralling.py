import requests
from bs4 import BeautifulSoup

A = "TOTAL DES PRODUITS DE FONCTIONNEMENT = A"
B = "TOTAL DES CHARGES DE FONCTIONNEMENT = B"
C = "TOTAL DES RESSOURCES D'INVESTISSEMENT = C"
D = "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"

# récuperation de l'URL complété de year étudié
def get_urlcomplete(commune,dpt,year):
#           debut_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056'
#           milieu_url = '&dep=075&type=BPS&param=5&exercice=2013'
    debut_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom='
    m1_url = '&dep='
    m2_url = '&type=BPS&param=5&exercice='
    url =  debut_url + commune + m1_url + dpt + m2_url+ year
    return url

def extract_amounts(node):
    decode = lambda text: int(text.replace(u'xa', '').replace(u' ', ''))
    children = node.parent.findAll(class_="montantpetit G")
    return decode(children[1].text), decode(children[2].text)

def recupere_result(commune,dpt,year):
    result = requests.get(get_urlcomplete(commune,dpt,year))
    soup = BeautifulSoup(result.text, 'html.parser')
    #print(soup)
    results = {}
    for libelle in soup.find_all(class_="libellepetit G"):
#        print("libellé : " + str(libelle.text))
        if (libelle.text == A) or (libelle.text == B) or (libelle.text == C) or (libelle.text == D) :
            key = libelle.text
            results[key] = extract_amounts(libelle)
    return results

def restitution_result(results):
# restitution des données récupérées
    libelle = [A , B, C, D]
    j = 0
    l1 = {}
    if len(results) > 0 :
        for i in results :
            print(libelle[j])
            l1 = results[i]
            print("----------------------------------------------------------+")
            print("Euros par habitant : " + str(l1[0]) + " Moyenne de la strate : " + str(l1[1]) + "     +")
            print("----------------------------------------------------------+")
            j = j + 1
    else :
        print("+        Pas d'information pour l'année : " + str(year) + "            +")
    return
#
#
#
dpt = '075'
commune = '056'
years = ['2009', '2010', '2011', '2012', '2013']
for year in years :
    print("===========================================================")
    print("+             Données de PARIS ANNEE : " + str(year) + "               +")
    print("===========================================================")
    resultats = recupere_result(commune,dpt,year)
    restitution_result(resultats)
#result = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013')


#montants = soup.find_all(class_="montantpetit G")
#print( montants)
