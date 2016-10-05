import requests
from bs4 import BeautifulSoup


# récuperation de l'URL complété de year étudié
def get_urlcomplete(commune,year):
#    debut_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056'
#    milieu_url = '&dep=075&type=BPS&param=5&exercice=2013'
    debut_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom='
    milieu_url = '&dep=075&type=BPS&param=5&exercice='
    url =  debut_url + commune + milieu_url + year
#   print(url)
    return url


def load_fiscal_year(commune,year):
    return get_urlcomplete(commune,year)

def extract_amounts(node):
    decode = lambda text: int(text.replace(u'xa', '').replace(u' ', ''))
    children = node.parent.findAll(class_="montantpetit G")
    return decode(children[1].text), decode(children[2].text)

def recupere_result(year):
    result = requests.get(load_fiscal_year('056', year))
    soup = BeautifulSoup(result.text, 'html.parser')
    #print(soup)
    results = {}
    A = "TOTAL DES PRODUITS DE FONCTIONNEMENT = A"
    B = "TOTAL DES CHARGES DE FONCTIONNEMENT = B"
    C = "TOTAL DES RESSOURCES D'INVESTISSEMENT = C"
    D = "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"
    for libelle in soup.find_all(class_="libellepetit G"):

        if (libelle.text == A) or (libelle.text == B) or (libelle.text == C) or (libelle.text == D) :
            key = libelle.text[-1]
            results[key] = extract_amounts(libelle)

    print("Données de PARIS ANNEE : " + str(year))
    print("==================================")
    libelle = [A , B, C, D]
    j = 0
    if len(results) > 0 :
        for i in results :
            print (libelle[j])
            print("Euros par habitant " + " Moyenne de la strate")
            print(results[i])
            print("-------------------------------")
            j = j + 1
    else :
        print("Pas d'information pour l'année : " + str(year))
    return
#def get_all_fiscal_data_years(years):
#    years_fiscal_data = {}
#    for year in years:
years = ['2009', '2010', '2011', '2012', '2013']
for year in years :
    recupere_result(year)

#result = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013')


#montants = soup.find_all(class_="montantpetit G")
#print( montants)
