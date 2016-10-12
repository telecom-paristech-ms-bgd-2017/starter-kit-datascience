import requests
from bs4 import BeautifulSoup

def GetSoupFromUrl(url):
    request=requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')

def GetInfo(NameProduct):
    url='http://www.cdiscount.com/search/10/'+ NameProduct +'.html#_his_'

    print(url)
    soup = GetSoupFromUrl(url)
    tile = soup.findAll("div", { "class" : "prdtBloc" })
    discount = 0.0
    sumNew = 0.0
    sumOld = 0.0
    for tiles_links in tile:

        for oldPrice in tiles_links.findAll("div", {"class": "prdtPrSt"}):
            oldPrice = oldPrice.text.encode('utf-8')
            oldPrice = oldPrice.replace(',', '.')
            oldPrice = oldPrice.replace('\'', '')
            oldPrice = float(oldPrice)
            print 'old', oldPrice
            newPrice = tiles_links.findAll("span", {"class": "price"})[0].text.replace(u"\u20AC", ',')
            newPrice = newPrice.replace('\'', '')
            newPrice = newPrice.replace(',', '.')
            newPrice = float(newPrice)
            print 'new', newPrice
            sumNew = sumNew + newPrice
            sumOld = sumOld + oldPrice
        discount = round((sumNew / sumOld)* 100,2)

    print 'Le pourcentage de discount de la marque', NameProduct, 'est', discount, '%'

NameProduct = 'dell'
GetInfo(NameProduct)
NameProduct = 'acer'
GetInfo(NameProduct)