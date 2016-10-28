import pandas as pd
import requests
from bs4 import BeautifulSoup

MAX_PAGE = 3


def getOldPrice(soup):

    return float(soup.text.replace(',', '.'))


def getNewPrice(soup):

    return float(soup.next_element+'.'+soup.next_element.next_element.text[1:])


def processProduct(soup):

    prod_title_soup = soup.find(attrs={"class": "prdtBTit"}).string

    new_price_soup = soup.find(attrs={"class": "price"})
    new_price = getNewPrice(new_price_soup)

    # equivalent a find("div",class_"prdtPrSt")
    old_price_soup = soup.find(attrs={"class": "prdtPrSt"})
    if ((old_price_soup == None) or (len(old_price_soup) == 0)):
        old_price = new_price
    else:
        old_price = getOldPrice(old_price_soup)

    print '====='
    print prod_title_soup
    print "old_price", old_price
    print "new_price", new_price
    print "discount", 100 * (old_price - new_price) / float(old_price)
    print '====='
    product = {}
    product['PC'] = prod_title_soup
    product['old_price'] = old_price
    product['new_price'] = new_price
    product['discount'] = 100 * (old_price - new_price) / float(old_price)

    return product


def removeAdsBlock(soup):
    isAds = False
    if (soup.text.find("Publicit") > 0):
        isAds = True
    return not isAds


def processCdiscount(search):

    prod_feature = []
    for page in range(1, MAX_PAGE + 1):
        page = requests.get(
            "http://www.cdiscount.com/search/10/"+search+"+ordinateur+portable.html?&page={}".format(search))
        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())
        # soup_list_prod =soup.find_all(attrs={"class":"prdtBloc"})# prdtBZPrice:
        # Article avec et sans remise et des publicites retournes
        soup_list_prod = soup.find_all("div", class_="prdtBloc")
        # print(len(soup_list_prod))
        #soup_list_prod = filter(removeAdsBlock, soup_list_prod)

        for soup_prod in soup_list_prod:
            # print soup_prod.prettify()
            new_prod = processProduct(soup_prod)
            prod_feature.append(new_prod)

    return prod_feature

metrics_acer = processCdiscount('Acer')
df_acer = pd.DataFrame(
    metrics_acer, columns=['PC', 'old_price', 'new_price', 'discount'])
df_acer.to_csv('Acer.csv', index=False, encoding='utf-8')
avg_acer = 0
for product in metrics_acer:
    avg_acer += product['discount']

metrics_dell = processCdiscount('Dell')
df_dell = pd.DataFrame(
    metrics_dell, columns=['PC', 'old_price', 'new_price', 'discount'])
df_dell.to_csv('Dell.csv', index=False, encoding='utf-8')
avg_dell = 0
for product in metrics_dell:
    avg_dell += product['discount']
print(
    "=================================================================================")

print("Acer AVG Discount = "+str(float(avg_acer) / len(metrics_acer)))
print("Dell AVG Discount = "+str(float(avg_dell) / len(metrics_dell)))
