import requests
from bs4 import BeautifulSoup



def extractinfosFromDomLebonCoin(soup):
    """Extraction des infos du site le bon coin : location 8e 9e et 16e d'appartement entre 30 et 70 m²"""
    list =[]
    appt = {}
    annonces = soup.find_all(class_="list_item clearfix trackable")
    for annonce in annonces:
        titre = annonce.find(class_="item_title").text
        if ("m²" in titre or "m2" in titre):
            try:
                appt['taille'] = titre[titre.index(" m")-2:titre.index(" m")]
            except:
                appt['taille'] = titre[titre.index("m") - 2:titre.index("m")]
            #print(appt.get('taille'))
            prix = annonce.find(class_="item_price").text
            appt['prix'] = prix[prix.index("€")-6:prix.index("€")].replace(" ",'').replace("\xa0","")
            #print(appt.get('prix'))
            appt['prix_m2'] = float(appt.get('prix')) / float(appt.get('taille'))
            #print("%.2f" % appt.get('prix_m2'))
            appt['date'] = annonce.find_all(class_="item_absolute")[0].find(class_="item_supp").text.strip()
            #print(appt.get('date'))
            list.append(appt)
        else:
            continue
    return list

#Max seems to be 2 pages
def getPagesLeBonCoin(nb,annonces):
    """Bouclage sur les pages retournées par la recherche"""
    for page in range(1,nb+1):
        result = requests.get("https://www.leboncoin.fr/locations/offres/ile_de_france/paris/?o="+str(page)+"&location=Paris%2075008&parrot=0&sqs=3&sqe=8&ros=2&roe=2&ret=2&furn=2")
        soup_page = BeautifulSoup(result.text, "html.parser")
        annonces.append(extractinfosFromDomLebonCoin(soup_page))
    return annonces

def extractinfosFromDomPap(soup):
    """Extraction des infos du site le bon coin : location 8e 9e et 16e d'appartement entre 30 et 70 m²"""
    list =[]
    appt = {}
    annonces = soup.find_all(class_="box search-results-item annonce")
    for annonce in annonces:
        appt['prix'] = annonce.find(class_="price").text
        appt['size'] = annonce.find_all(class_="item-summary float-left")[2].text
        list.append(appt)

    return list








annonces = []
annonces = getPagesLeBonCoin(10,annonces)
print(annonces)



