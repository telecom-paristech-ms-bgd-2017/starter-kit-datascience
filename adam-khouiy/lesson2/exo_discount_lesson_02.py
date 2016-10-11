import requests
from bs4 import BeautifulSoup





url = 'http://www.cdiscount.com/search/10/{}+ordinateur+portable.html?&page={}#_his_'

def formatagedonne(price):
    if (price != ''):
      price1 =price.replace(',', '.')
      price2= price1.replace('€', '.')
      return float (price2)
    else :
        return float("0.0")

def discountIndicator (name , page):

    list_indicator=[]
    resultat = requests.get(url.format(name ,str(page)))
    soup = BeautifulSoup(resultat.text, 'html.parser')
    list_result = soup.select("#lpBloc > li")
    for result in list_result:
        indicator=0
        if result.select(".prdtPrSt") != []  and  result.select(".price") !=[]:
             prix_initial = formatagedonne(result.select(".prdtPrSt")[0].text)
             prix_reduit = formatagedonne(result.select(".price")[0].text)
             if prix_reduit !=0:
                 indicator = (prix_initial-prix_reduit)/prix_reduit
             else :
                 indicator= 0
             list_indicator.append(indicator)

             for l in list_indicator :
                 l +=l

             moyenne = l/len(list_indicator)

    return moyenne



print ("indicator dell" ,discountIndicator('dell',2))
print ("indicator  acer" ,discountIndicator('acer',2))


print("**************************");


