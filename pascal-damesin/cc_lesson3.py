# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:43:36 2016

@author: Pascal
"""
import requests
from bs4 import BeautifulSoup

def brand_crawling(brand):
    brand_discount = requests.get('http://www.cdiscount.com/search/10/' + str(brand) + '.html')
    brand_soup = BeautifulSoup(brand_discount.text, 'html.parser')
    brand_product = brand_soup.find_all(class_="prdtBloc")
    return brand_product


def brand_discount(soup):
    discounts = []
    for amount in soup:
        price = amount.find(class_="price")
        price = price.text.split("€")
        price = float(price[0]) + float(price[1]) / 100
        try:
            previous_price = amount.find(class_="prdtPrSt")
            previous_price = previous_price.text.split("€")
            previous_price = float(previous_price[0].replace(",", "."))
        except:
            previous_price = price
        discount = (1.0 - price / previous_price)
        discounts.append(discount)

    avg_discount_rate = sum(discounts) / len(discounts)
    return avg_discount_rate

avg_dell_discount_rate = brand_discount(brand_crawling("dell"))
avg_acer_discount_rate = brand_discount(brand_crawling("acer"))

print("average dell discount :", round(100 * avg_dell_discount_rate), " %")
print("average acer discount :", round(100 * avg_acer_discount_rate), " %")
