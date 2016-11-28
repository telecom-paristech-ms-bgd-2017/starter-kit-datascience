# @Author : BENSEDDIK Mohammed

import requests
from bs4 import BeautifulSoup


product_brands = ['dell', 'hp', 'acer']


def get_soup(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


def find_price_index(brand_product):
    url = 'http://www.cprice_index.com/search/10/' + brand_product + '.html#_his_'
    soup = get_soup(url)
    tiles = soup.findAll("div", {"class": "prdtBloc"})
    price_index = 0.0
    sum_new_price = 0.0
    sum_old_price = 0.0
    for tile in tiles:
        for old_price in tile.findAll("div", {"class": "prdtPrSt"}):
            new_price = tile.findAll("span", {"class": "price"})[
                0].text.replace(u"\u20AC", ',')
            new_price = new_price.replace('\'', '')
            new_price = new_price.replace(',', '.')
            new_price = float(new_price)
            try:
                old_price = old_price.text
                old_price = old_price.replace(',', '.')
                old_price = old_price.replace('\'', '')
                old_price = float(old_price)
            except ValueError:
                old_price = new_price

        sum_new_price = sum_new_price + new_price
        sum_old_price = sum_old_price + old_price
        price_index = round((sum_new_price / sum_old_price) * 100, 2)
    return(price_index)


def print_result(brand_product):
    print('price_index index for : ' + brand_product +
          ' is : ' + str(find_price_index(brand_product)))

for brand in product_brands:
    print_result(brand)
