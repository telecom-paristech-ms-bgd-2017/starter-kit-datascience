
import requests
from bs4 import BeautifulSoup as bs4
import re
import pandas as pd
import numpy as np
from itertools import compress


########################################################################


def getSoup(urlBase, region, locParams, nbPages):

    result = requests.get(urlBase.format(region), locParams)
    print("searching :" + result.url)
    soup = bs4(result.text, "html.parser")

    if nbPages == 1:

        link = soup.find('a', id='last')

        if link is not None:
            pattern = re.compile(r'\W*(/?o=)\W*(\d*)')
            nbPages = int(pattern.search(link.get("href")).group(2))
        else:
            nbPages = 1
        print(str(nbPages) + ' pages to scrap')
    return soup, nbPages

#########################################################################


def extractInfos(soup, vendeur, allZoes):

    telPattern = re.compile(
        r'(0[1-9])[ .-]*(\d{2})[ .-]*(\d{2})[ .-]*(\d{2})[ .-]*(\d{2})')

    AllLi = (soup.find(class_="tabsContent block-white dontSwitch")
             .find_all(class_="list_item clearfix trackable"))
    adresses = [x.get('href') for x in AllLi]
    for adr in adresses:
        dicLoc = {}
        resAnnonce = requests.get("https:{}".format(adr))
        resSoup = bs4(resAnnonce.text, "html.parser")

        dicLoc['title'] = resSoup.find(
            class_="adview_header clearfix").find("h1").text.strip()
        dicLoc['price'] = float(
            resSoup.find(class_="item_price clearfix").get('content'))
        dicLoc['location'] = resSoup.find(
            class_="line line_city").find(class_='value').text.strip()
        dicLoc['année'] = int(
            resSoup.find('span', itemprop="releaseDate").text.strip())

        # marche pas bordel de merde
        # speCSS = ("adview > section > section > section.properties.lineNegative >"
        #"div:nth-of-type(10) > h2 > span.value")
        # resSoup.select(speCSS)
        objProp = resSoup.find_all(class_="property")
        for tt in objProp:
            if tt.text == "Kilométrage":
                dicLoc['kilométrage'] = float(tt.find_next_sibling('span')
                                              .text.replace(" ", "")
                                              .replace("KM", ""))
                break
        try:
            tel = ''.join(telPattern.search(
                resSoup.find('p', itemprop="description").text).groups())
        except:
            tel = "0000000000"

        dicLoc['tel'] = tel
        if vendeur == 'c':
            dicLoc['vendeur'] = 'pro'
        else:
            dicLoc['vendeur'] = 'part'

        allZoes = allZoes.append(dicLoc, ignore_index=True)
    return allZoes

##############################################################################


def getZoes(urlBase, params):

    allZoes = pd.DataFrame(
        columns=['title', 'price', 'location', 'année',
                 'kilométrage', 'tel', 'vendeur'])

    for ii in params["region"]:

        for jj in params["vendeur"]:
            print(allZoes.shape)
            page = 1
            nbPages = 1
            temp = {'o': page, 'q': "renault zoé", 'f': jj}
            soup, nbPages = getSoup(urlBase, ii, temp, nbPages)
            allZoes = extractInfos(soup, jj, allZoes)

            for kk in range(2, nbPages + 1):
                temp = {'o': kk, 'q': "renault zoé", 'f': jj}
                soup, nbPages = getSoup(urlBase, ii, temp, nbPages)
                allZoes = extractInfos(soup, jj, allZoes)
    return allZoes

##############################################################################


def getArgus(url, années):

    suffix = "cote-voitures-renault-zoe--{}-.html"
    allArgus = pd.DataFrame(columns=["Description", "année", "prix"])

    for annee in années:
        print(annee)
        result = requests.get(url.format(suffix.format(annee)))
        soup = bs4(result.text, 'html.parser')
        listeLink = soup.find(class_="listingResult").find_all("a")
        links = [x.get("href") for x in listeLink]

        for link in links:
            if link.find('renault-zoe') == -1:
                continue
            locDico = {}
            result = requests.get(url.format(link))
            soup = bs4(result.text, 'html.parser')
            locDico['prix'] = float(
                soup.find(class_="f24 bGrey9L txtRed pL15 mL15")
                .text.strip().replace(' ', '')
                .replace('€', ''))
            locDico['Description'] = soup.find(
                class_="txtGrey58 f14 noBold").text.lower().split()
            locDico['année'] = annee
            allArgus = allArgus.append(locDico, ignore_index=True)
    return allArgus


##############################################################################

urlBase = "https://www.leboncoin.fr/voitures/offres/{}/"
params = {}
params["region"] = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]
params["vendeur"] = ["c", "p"]

allZoes = getZoes(urlBase, params)

urlArgus = "http://www.lacentrale.fr/{}"
années = list(range(2012, 2017))

allArgus = getArgus(urlArgus, années)


##############################################################################
# mixing des deux tables


temp = list(allArgus.columns)
temp.append(["index", '+/-'])
selSortArg = pd.DataFrame(columns=list(allArgus.columns))

for ii in allZoes.index:
    curZoeList = allZoes["title"][ii].lower().split()
    selArgus = allArgus[allArgus['année'].isin([allZoes.loc[ii]["année"]])]

    test1 = []
    test2 = []
    for ind, argus in enumerate(selArgus.index):
        test1.append(len(set(curZoeList).intersection(selArgus["Description"][argus])))
        test2.append(test1[ind] / len(selArgus["Description"][argus]))

    crit1 = max(test1)
    mask1 = [test1[x] == crit1 for x in range(len(test1))]
    crit2 = max(list(compress(test2, mask1)))
    mask2 = [test2[x] == crit2 for x in range(len(test2))]
    mask = np.asarray(mask1) * np.asarray(mask2)
    indexMatch = list(compress(selArgus.index, mask))[0]
    tempDico = selArgus.loc[indexMatch].to_dict()
    tempDico["index"] = ii
    if allZoes["price"][ii] <= selArgus["prix"][indexMatch]:
        tempDico["+/-"] = '-'
    else:
        tempDico["+/-"] = '+'

    selSortArg = selSortArg.append(tempDico, ignore_index=True)
selSortArg = selSortArg.set_index("index")
finalZoes = pd.concat([allZoes, selSortArg[['Description', 'prix','+/-', 'année']]], axis=1)

myFile = r"C:\Users\jbker\Documents\2016_TELECOM\999_RepoGit\starter-kit-datascience\jb-kerboul\Lesson4\Zoes.csv"

finalZoes.to_csv(myFile)
