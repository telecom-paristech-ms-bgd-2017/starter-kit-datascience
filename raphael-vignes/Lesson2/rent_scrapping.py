import requests
from bs4 import BeautifulSoup
import datetime
import re

def extractinfosFromDomLebonCoin(soup):
    """Extraction des infos du site le bon coin : location 8e 9e et 16e d'appartement entre 30 et 70 m²"""
    list =[]
    appt = {}
    annonces = soup.find_all(class_="list_item clearfix trackable")
    for annonce in annonces:
        titre = annonce.find(class_="item_title").text
        if (" m² " in titre or " m2 " in titre):
            try:
                appt['taille'] = titre[titre.index(" m")-2:titre.index(" m")]
            except:
                appt['taille'] = titre[titre.index("m") - 2:titre.index("m")]
            print(appt.get('taille'))
            prix = annonce.find(class_="item_price").text
            appt['prix'] = prix[prix.index("€")-6:prix.index("€")].replace(" ",'').replace("\xa0","")
            print(appt.get('prix'))
            appt['prix_m2'] = float(appt.get('prix')) / float(appt.get('taille'))
            print(appt.get('prix_m2'))
            date = annonce.find_all(class_="item_absolute")[0].find(class_="item_supp").text.strip()
            if "Aujourd\'hui" in date:
                date.replace("Aujourd\'hui",str(datetime.date))
            appt['date'] = date
            print(appt.get('date'))
            list.append(appt)
        else:
            continue
    return list

#Max seems to be 2 pages
def getPagesLeBonCoin(nb):
    """Bouclage sur les pages retournées par la recherche"""
    infos = []
    for page in range(1,nb+1):
        result = requests.get("https://www.leboncoin.fr/locations/offres/ile_de_france/paris/?o="+str(page)+"&location=Paris&parrot=0&sqs=3&sqe=8&ros=2&roe=2&ret=2&furn=2")
        soup_page = BeautifulSoup(result.text, "html.parser")
        infos.append(extractinfosFromDomLebonCoin(soup_page))
    return infos

annoncesParis = getPagesLeBonCoin(10)
print(annoncesParis)


