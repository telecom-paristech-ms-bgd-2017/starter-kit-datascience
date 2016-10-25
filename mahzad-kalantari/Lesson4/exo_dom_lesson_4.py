from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import time

from subprocess import call
import re

from torrequest import TorRequest


#@ MahzadK October 2016

def findNbPage(lien) :
    r3 = requests.get(lien)
    soup = BeautifulSoup(r3.text, 'html.parser')
    div = soup.find(id="last")
    textPage = div.get('href')
    numPage = int(textPage.split('?')[1].split('=')[1].split('&')[0])
    return numPage


def extractLink(lien):
    r3 = requests.get(lien)
    soup = BeautifulSoup(r3.text, 'html.parser')
    cells = soup.find_all('section', {'class' : "tabsContent block-white dontSwitch"})
    li = cells[0].find_all('li')

    listeLien = []
    for i in li :
        lien =  i.find('a').get('href')
        listeLien.append("https:"+lien)
    return listeLien

def getKm(cells) :
    #find km
    resKm = cells[5].find('span',{'class' : 'value'})
    Km = (re.sub(r'\D', '', resKm.get_text()))
    return Km

def getPrice(cells):
    resPrix = cells[0].find('span',{'class' : 'value'})
    prix =  int(re.sub(r'\D', '', resPrix.get_text()))
    return prix

def getTitre(cells):
    #Find Titre
    cells = soup.find_all('h1',{'class' : 'no-border'})
    res =  (re.sub(r'\w', '', cells[0].get_text()))
    return res

def getModel(cells):
    return cells[3].find('span',{'class' : 'value'}).text

def getYear(cells):
    resAnnee = cells[4].find('span',{'class' : 'value'})
    annee = int(re.sub(r'\D', '', resAnnee.get_text()))
    return annee

def getProOrPart(cells):
    resPro = soup.find('span',{'class' : 'ispro'})
    if not resPro is None :
        res = "pro"
    else :
        res = "particulier"
    print(res)
    return res



def getPhone(lienPage):
    id = lienPage.split('/')[4].split(".")[0]
    lienImage = "https://www2.leboncoin.fr/ajapi/get/phone?list_id="+id
    with TorRequest() as tr:
        time.sleep(5)
        tr.reset_identity()
        tr.ctrl.signal('CLEARDNSCACHE')
        r3 = tr.get(lienImage)
        response = tr.get('http://ipecho.net/plain')
        print("ip", response.text)
        data = json.loads(r3.text)
        if data!= '':
            lien = data['phoneUrl']
            f = open('temp.gif', 'wb')
            f.write(requests.get(lien).content)
            f.close()
            call(["sips", "-s", "format", "jpeg", "temp.gif", "--out", "temp.jpeg",  "-Z", "600" ])
            call(["tesseract", "temp.jpeg", "temp", "-psm", "7", "nobatch", "digits"])
            numero = open('temp.txt').read()
            print(numero)
            if len(numero)>0:
                return (re.sub(r'\D', '', numero))
            else :
                return("000000000")
        else :
            return("000000000")


def getVersion(soup):
    titre = soup.find('h1',{'class' : 'no-border'}).get_text().lower()
    version = None
    for v in versions:
        if v in titre:
            version = v
            break
    return version

#*********************************************************************



listeTotal = []
versions = ['intens', 'zen', 'life']

numPage = findNbPage("https://www.leboncoin.fr/voitures/offres/ile_de_france/?th={}&q=Renault%20Zoe&parrot=0".format('1'))

for page in range(1,numPage) :
    page = str(page)
    print(page)

    listeRegion = ["https://www.leboncoin.fr/voitures/offres/ile_de_france/?th={}&q=Renault%20Zoe&parrot=0".format(page),
                     "https://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?th={}&q=Renault%20Zoe&parrot=0".format(page),
                     "https://www.leboncoin.fr/voitures/offres/aquitaine/?th={}&q=Renault%20Zoe&parrot=0".format(page)]
    liste = []
    lien1 =  listeRegion[0]
    liste = extractLink(lien1)
    listeTotal.extend(liste)

dfLBC = pd.DataFrame(columns=('Modele','Version', 'Année', 'Km', 'TypeVendeur', 'Telephone' ))
dfCentrale= pd.DataFrame(columns=['Année', 'Version', 'Cote'])


listeTitre = []
listeModele = []
listeYear = []
listPrix = []
listeKm = []
listeTypeVendeur = []
listeTelephone = []
listeVersion =[]

with TorRequest() as tr:
    time.sleep(3)
    tr.reset_identity()
    tr.ctrl.signal('CLEARDNSCACHE')
    for li in listeTotal :
        print(li)
        r3 = tr.get(li)
        soup = BeautifulSoup(r3.text, 'html.parser')
        cells = soup.find_all('h2',{'class' : 'clearfix'})
        Km = getKm(cells)
        listeKm.append(Km)
        Model = getModel(cells)
        listeModele.append(Model)
        Year = getYear(cells)
        listeYear.append(Year)
        price = getPrice(cells)
        listPrix.append(price)
        pro = getProOrPart(cells)
        listeTypeVendeur.append(pro)
        Phone = getPhone(li)
        listeTelephone.append(Phone)
        version = getVersion(soup)
        listeVersion.append(version)


# la centrale auto
url_cote = "http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide-{annee}.html"

annees = [2012, 2013, 2014, 2015]

for annee in annees:
    for version in versions:
        url = url_cote.replace('{version}', version)
        url = url.replace('{annee}', str(annee))
        print ('Cote: ' + url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        #cote = float(re.sub(r'\D', '', soup.find('span', {'class': 'Result_Cote'}).get_text()))
        cote = 200
        dfCentrale = dfCentrale.append({
            'Version': version,
            'Année': annee,
            'Cote': cote
        }, ignore_index=True)

dfLBC['Modele'] = listeModele
dfLBC['Année'] = listeYear
dfLBC['Km'] = listeKm
dfLBC['TypeVendeur'] = listeTypeVendeur
dfLBC['Telephone'] = listeTelephone
dfLBC['Version'] = listeVersion
dfLBC.to_csv('leboncoinIldeFrance.csv', sep =';')

# Inner join sur Version et Année
#data_merged = pd.merge(dfLBC, dfCentrale, on=['Version', 'Année'], how='inner')
#data_merged['Delta'] = (data_merged['Prix'] - data_merged['Cote']) / data_merged['Cote'] * 100.
#data_merged = data_merged.sort(columns=['Delta'])
#data_merged = data_merged.reset_index()
#data_merged['Delta'] = data_merged['Delta'].map('{:,.1f}%'.format)
#data_merged.to_csv('zoe_idf.csv', sep=';')







# Argus la centrale de l'auto
#http://www.lacentrale.fr/cote-voitures-renault-zoe--2016-.html

#http://www.lacentrale.fr/cote-voitures-renault-zoe--{}-.html.form(Annee)
