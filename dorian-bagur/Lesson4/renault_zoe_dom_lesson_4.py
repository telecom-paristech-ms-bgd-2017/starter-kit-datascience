import dryscrape
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import os


URL = "https://www.leboncoin.fr/voitures/offres/"
TAGS = ['brand', 'model', 'area', 'version', 'year', 'distance_traveled',
        'price', 'phone', 'saler', 'argus']
# AREAS = ["ile_de_france", "aquitaine", "nord_pas_de_calais"]
AREAS = ["ile_de_france"]
# SALERS = ["c", "p"]
SALERS = ["p"]
BRAND = "renault"
MODEL = "zoé"
PATH = os.path.dirname(os.path.realpath(__file__))
print(PATH)


def extractArgus(ad):
    return None


def extractPhone(ad):
    return None


def extractModel(ad):
    return ad.find(itemprop="model").text


def extractBrand(ad):
    return ad.find(itemprop="brand").text


def extractDistanceTraveled(ad):
    return ad.find_all(class_="line")[7].find(class_="value").text


def extractYear(ad):
    year = ad.find(itemprop="releaseDate").text
    pattern = r'\d{4}'
    regex_year = re.compile(pattern)
    return regex_year.findall(year)[0]


def extractVersion(ad):
    version = ad.find(class_="adview_header").h1.text
    # gestion des accents
    version = unicodedata.normalize('NFKD', version).encode('ASCII', 'ignore'
                                                            ).decode('UTF-8')
    pattern = r'(?i)zoe\s\w+'
    regex_version = re.compile(pattern, flags=re.IGNORECASE)
    return regex_version.findall(version)[0].split(' ')[1].upper()


def extractPrice(ad):
    return ad.find(itemprop="price")['content']


def compose(ad, area, saler):
    return {'brand': extractBrand(ad), 'model': extractModel(ad),
            'area': area, 'version': extractVersion(ad),
            'year': extractYear(ad), 'distance_traveled':
            extractDistanceTraveled(ad), 'price': extractPrice(ad),
            'phone': extractPhone(ad), 'saler': saler,
            'argus': extractArgus(ad)
            }


def getAd(url):
    url = "https:" + url
    session = dryscrape.Session()
    session.visit(url)
    res = session.body()
    print(url)
    return BeautifulSoup(res, "html.parser").find(id="adview")


def getAdLink(ad):
    return ad.find("a")["href"]


def getAdsList(url, brand, model, area, saler):
    payload = {"q": brand + " " + model, "f": saler}
    res = requests.get(url + area, params=payload)
    print(url)
    return BeautifulSoup(res.text, "html.parser").find(id="listingAds"
                                                       ).find_all("li")

dict_ads = []
for area in AREAS:
    for saler in SALERS:
        adsList = getAdsList(URL, BRAND, MODEL, area, saler)
        adsUrl = map(getAdLink, adsList)
        adsList_unclean = map(getAd, adsUrl)
        dict_ads.append(map(lambda ad: compose(ad, area, saler),
                        adsList_unclean))

df = pd.DataFrame.from_records(dict_ads[0])
df.to_csv(PATH + "/" + BRAND + "_" + MODEL + ".csv")
print(df)
