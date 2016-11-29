import requests
from bs4 import BeautifulSoup


def getMetrics(marque, page):
    # récupération des données de la page
    url = 'http://www.cdiscount.com/search/10/ordinateur+'
    soup = BeautifulSoup(requests.get(url + marque + '.html?page=' + str(page)).text, 'html.parser')

    # prix après réduction
    prix_def = [float(e.text.replace('€', '.')) for e in soup.find_all(class_='price')]

    # prix avant réduction
    prix_depart = []
    for e in soup.find_all(class_='prdtPInfoTC'):
        if e.text == '':
            prix_depart.append(0)
        else:
            prix_depart.append(float(e.text.replace(',', '.')))

    for i in range(0, len(prix_def)):
        if prix_depart[i] == 0:
            prix_depart[i] = prix_def[i]

    # On somme les éléments liste à liste
    return [sum(prix_depart), sum(prix_def)]

def Reduc(marque, page_debut, page_fin):
    a = [0, 0]
    for i in range(page_debut, page_fin + 1):
        a[0] += getMetrics(marque, i)[0]
        a[1] += getMetrics(marque, i)[1]
    return 1 - a[1] / a[0]

print(Reduc('acer', 1, 3))
print(Reduc('dell', 1, 3))
