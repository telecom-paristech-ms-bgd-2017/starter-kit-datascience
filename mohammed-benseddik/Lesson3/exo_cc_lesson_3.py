import requests
from bs4 import BeautifulSoup

url = "http://www.cdiscount.com/search/10/oridnateur+dell.html#_his_"

req = requests.get(url)

soup = BeautifulSoup(req.text, 'html.parser')


def find_price_barre(soup):
    liste_prix_ori = []
    liste_prix_barre = []
    liste_nom_ordi = []
    prix_barre = soup.find_all(class_='prdtPrSt')
    noms_ordi = soup.find_all(class_='prdtBTit')
    prix_ori = soup.find_all('span', {'class': 'price'})

    for elmt in prix_barre:
        liste_prix_barre.append(elmt.text)
    for elmt in noms_ordi:
        liste_nom_ordi.append(elmt.text)
    for elmt in prix_ori:
        liste_prix_ori.append(elmt.text)

    return len(liste_nom_ordi), len(liste_prix_ori), len(liste_prix_barre)

print(find_price_barre(soup))

original_price = soup.find_all('div', class_='prdTprice')


prix_barre = soup.find_all(class_='prdtPrSt')
nom_ordi = soup.find_all(class_='prdtBTit')

print(nom_ordi.text)
print(prix_barre[0].text)
print(original_price)
