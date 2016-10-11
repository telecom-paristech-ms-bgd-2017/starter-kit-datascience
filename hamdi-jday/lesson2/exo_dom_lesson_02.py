from urllib.request import urlopen
from bs4 import BeautifulSoup

years = [2013, 2012, 2011, 2010]
Taxe = ['Taxe d\'habitation (y compris THLV)', 'Taxe foncière sur les propriétés bâties']
Taxe.append('Taxe foncière sur les propriétés non bâties')
Taxe.append('Cotisation foncière des entreprises')


# retourne le contenue de la page de l'année n
def get_page(n):
    u = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=118&dep=014&type=BPS&param=5&exercice=' + str(n)
    data = urlopen(u)
    soup = BeautifulSoup(data, "lxml")
    return soup


# retourne les indices d'emplacements de la chaine s
def mes_indices(soup, s):
    res = []
    for i in range(len(soup('td'))):
        if len(soup('td')[i].contents) == 0:
            continue
        elif soup('td')[i].contents[0].find(s) == -1:
            continue
        else:
            res.append(i)
    return res


# retourne un tableau de 2-tuples (une matrice de 3x4) contenant les montants (Euros, par habitant, par strate)

def montant_taxes(soup, taxe, indices, n):
    res = []
    if n==2010:
        a = soup('td')[indices[-3] + 1].contents[0].replace('\xa0', '').replace(' ', '')
        b = soup('td')[indices[-3] + 2].contents[0].replace('\xa0', '').replace(' ', '')
        c = soup('td')[indices[-3] + 3].contents[0].replace('\xa0', '').replace(' ', '')
        res.append([a, b, c])
    else:
        a = soup('td')[indices[-2] + 1].contents[0].replace('\xa0', '').replace(' ', '')
        b = soup('td')[indices[-2] + 2].contents[0].replace('\xa0', '').replace(' ', '')
        c = soup('td')[indices[-2] + 3].contents[0].replace('\xa0', '').replace(' ', '')
        res.append([a, b, c])
    return res


# retourne le dictionnaire taxe : (valeur par habitant, valeur par strate)  pour l'année n
def table_page(n):
    res = {}
    for taxe in Taxe:
        res[taxe] = montant_taxes(get_page(n), taxe, mes_indices(get_page(n), taxe), n)
    return res


for n in years:
    print("année " + str(n) + ":" + str(table_page(n)))
