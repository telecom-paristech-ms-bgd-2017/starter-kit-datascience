import requests
from bs4 import BeautifulSoup


def getMetrics(marque, page):
    # récupération des données de la page
    url = 'http://www.cdiscount.com/search/10/ordinateur+'
    soup = BeautifulSoup(requests.get(url + marque + '.html?page=' + str(page)).text, 'html.parser')

    # prix après réduction
    final_price = [float(e.text.replace('€', '.')) for e in soup.find_all(class_='price')]

    # prix avant réduction
    initial_price = []
    for e in soup.find_all(class_='prdtPInfoTC'):
        if e.text == '':
            initial_price.append(0)
        else:
            initial_price.append(float(e.text.replace(',', '.')))

    for i in range(0, len(final_price)):
        if initial_price[i] == 0:
            initial_price[i] = final_price[i]

    # On somme les éléments liste à liste
    return [sum(initial_price), sum(final_price)]

def calculReduc(marque, page_debut, page_fin):
    a = [0, 0]
    for i in range(page_debut, page_fin + 1):
        a[0] += getMetrics(marque, i)[0]
        a[1] += getMetrics(marque, i)[1]
    return 1 - a[1] / a[0]

print(calculReduc('acer', 1, 3))
print(calculReduc('dell', 1, 3))