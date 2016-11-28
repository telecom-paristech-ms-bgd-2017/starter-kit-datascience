import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
from functools import partial


MAX_PAGE = 10
numProcesses = 4 # my number of cores
run_type = 'Parallel' # Parallel or Sequential


def getOldPrice(soup):

    return float(soup.text.replace(',', '.'))


def getNewPrice(soup):

    return float(soup.next_element+'.'+soup.next_element.next_element.text[1:])


def removeAdsBlock(soup):
    isAds = False
    if (soup.text.find("Publicit") > 0):
        isAds = True
    return not isAds


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


def processPage(search,page):
    prod_featureByPage = []
    page = requests.get("http://www.cdiscount.com/search/10/"+search+"+ordinateur+portable.html?&page={}".format(page))
    soup = BeautifulSoup(page.text, 'html.parser')
    soup_list_prod = soup.find_all("div", class_="prdtBloc")
    for soup_prod in soup_list_prod:
        new_prod = processProduct(soup_prod)
        prod_featureByPage.append(new_prod)
    return prod_featureByPage


def processCdiscount(search):

    prod_feature = []
    if (run_type == 'Sequential'):
        for pageNum in range(1, MAX_PAGE + 1):
            prod_feature = prod_feature + processPage(search,pageNum)
    else:
        pool = Pool(numProcesses)
        func = partial(processPage, search)
        prod_feature = pool.map(func, range(1, MAX_PAGE + 1))
        pool.close()
        pool.join()
        flattenned_prod_feature = [val for sublist in prod_feature for val in sublist] #
        prod_feature = flattenned_prod_feature

    print (len(prod_feature))
    return prod_feature

if __name__ == '__main__':
    start_time = time.time()
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
    print(
        "--- Run type : {0}. Exec time (in s) : {1} ---".format(run_type, time.time() - start_time))
