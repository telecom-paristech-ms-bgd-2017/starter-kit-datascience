import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


###################################################################
###################################################################
#####             Fonctions utilitaires                   #########
###################################################################
###################################################################
def getSoupFromUrl(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def prettyPrint(listData):
    print(tabulate(listData, headers=['version', 'annee', 'kilometrage', 'prix', 'telephone', 'professionnel', 'argus',
                                      'gooddeal'], tablefmt='psql'))

###################################################################
###################################################################





###################################################################
###################################################################
#####             Fonction principale                     #########
###################################################################
###################################################################
def getAllCarUrl(zone_recherche):
    df = pd.DataFrame(
        columns=['version', 'annee', 'kilometrage', 'prix', 'telephone', 'professionnel', 'argus', 'gooddeal'])
    for zone in zone_recherche:
        url = 'https://www.leboncoin.fr/voitures/offres/' + zone + '/?th=1&q=ZOE&parrot=0'
        soupSearch = getSoupFromUrl(url)
        for a in soupSearch.find("section", {"class": "tabsContent block-white dontSwitch"}).findAll("a"):
            try:
                soupCar = getSoupFromUrl("https:"+a['href'])
                brand = soupCar.find('span', {"itemprop": "brand"}).text
                model = soupCar.find('span', {"itemprop": "model"}).text
                if brand.lower() == 'renault' and model.lower() == 'zoe':
                    v = re.search("(intens|life|zen)", soupCar.find('h1', {"itemprop": "name"}).text.lower())
                    if v:
                        version = v.group(1)
                    annee = soupCar.find('span', {"itemprop": "releaseDate"}).text.strip()
                    #print("SoupCar")
                    #print(soupCar)
                    kilometrage_raw = soupCar.find(
                        "section", {"class": "properties lineNegative"}).findAll("h2")[5].find("span", {"class": "value"}).text.replace(" ", "")
                    kilometrage_reg = re.search("(.*)KM", kilometrage_raw)
                    if kilometrage_reg:
                        kilometrage = float(kilometrage_reg.group(1))

                    prix_raw = soupCar.find('h2', {"itemprop": "price"}).text
                    prix_reg = re.search("(.*)€", prix_raw)
                    if prix_reg:
                        prix = float(prix_reg.group(1).replace(" ", ""))
                    m = re.search("0[1-9][0-9]{8}", soupCar.find('p', {"itemprop": "description"}).text)
                    telephone = 0000000
                    if m:
                        telephone = m.group(0)
                    professionnel = 'non'

                    pro = soupCar.find('span', {"class": "ispro"})
                    if  pro:
                        professionnel = 'oui'
                    urlArgus = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + version + '+charge+rapide-' + annee + '.html'
                    print("urlArgus   " + urlArgus)
                    soupArgus = getSoupFromUrl(urlArgus)
                    argus_reg = re.search("(.*) €", soupArgus.find('strong', {"class": "f24 bGrey9L txtRed pL15 mL15"}).text)

                    #argus_reg = re.search("(.*) €", soupArgus.select(".Result_Cote.arial.tx20")[0].text)
                    if argus_reg:
                        argus = float(argus_reg.group(1).replace(" ", ""))
                    if argus != 0:
                        test = prix - argus
                        if (test < -1000):
                            gooddeal = "mega good deal"
                        elif (-1000 <= test <= 0):
                            gooddeal = "good deal"
                        elif (0 <= test <= 1000):
                            gooddeal = "bad deal"
                        else:
                            gooddeal = "very bad deal"
                    else:
                        gooddeal = "NA"
                    df = df.append(pd.Series({'version': version, 'annee': annee, 'kilometrage': kilometrage, 'prix': prix,
                                              'telephone': telephone, 'professionnel': professionnel, 'argus': argus,
                                              'gooddeal': gooddeal},
                                             index=['version', 'annee', 'kilometrage', 'prix', 'telephone', 'professionnel',
                                                    'argus', 'gooddeal']), ignore_index=True)

            except:
                print('pb connexion')
    df.to_csv('zoe.csv')
    return (df)

###################################################################
###################################################################
###################################################################





###################################################################
###################################################################
#####             Lancement du traitement                     #####
###################################################################
###################################################################
zone_recherche = ["ile_de_france", "provence_alpes_cote_d_azur", "aquitaine"]
datas = getAllCarUrl(zone_recherche)
prettyPrint(datas)

