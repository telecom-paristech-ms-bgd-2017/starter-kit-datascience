import dryscrape
import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://www.leboncoin.fr/voitures/offres/"
TAGS = ['brand', 'model', 'area', 'version', 'year', 'distance_traveled',
        'price', 'phone', 'saler', 'argus']
# AREAS = ["ile_de_france", "aquitaine", "nord_pas_de_calais"]
AREAS = ["ile_de_france"]
# SALERS = ["c", "p"]
SALERS = ["p"]
BRAND = "renault"
MODEL = "zoé"


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
    return ad.find(itemprop="releaseDate").text


def extractVersion(ad):
    return ad.find(class_="adview_header").h1.text


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
        dict_ads.append(list(map(lambda ad: compose(ad, area, saler),
                        adsList_unclean)))

"""print(dict_ads)
df = pd.DataFrame.from_records(dict_ads)
print(df)"""
