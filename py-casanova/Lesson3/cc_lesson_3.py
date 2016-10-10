#! /usr/bin/python3.5
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def crawlCDiscount(brands, pages):
    """
    Crawls Cdiscount pages to get product discounts and returns dict of lists by brand 
    Arguments: 
    - brands = list of strings with brand names to crawl
    - pages = number of pages to crawl
    """

    db_discounts = {}

    # Crawler
    for brand in brands:

        discounts = []

        for page in range(1, pages + 1):

            url = 'http://www.cdiscount.com/search/10/' + str(brand) + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=' + \
                brand + '&page=' + str(page) + '&_his_'

            try:
                results = requests.get(url)
                soup = BeautifulSoup(results.text, "html.parser")
                print("*" * 40)
                print("Getting page number " +
                      str(page) + " for brand: " + brand)
                print("*" * 40)

                # Getting precedent price and current price figures for products
                # on current page
                products = soup.find_all(class_="prdtBloc")

                for i, product in enumerate(products):
                    price = product.find(class_="price")
                    price = price.text.split("€")
                    price = float(price[0]) + float(price[1]) * 0.01
                    try:
                        precedent_price = product.find(class_="prdtPrSt")
                        precedent_price = float(precedent_price.text.split("€")[
                                                0].replace(",", "."))
                    except:
                        precedent_price = price
                    discount = 1. - price / precedent_price
                    print(discount)
                    discounts.append(discount)

            except:
                print("Page number " + str(page) + " not found")
                break

        db_discounts[brand] = discounts

    return db_discounts

# MAIN
target_brands = ["dell", "acer"]
nb_pages = 3
df = pd.DataFrame.from_dict(crawlCDiscount(target_brands, nb_pages))
print(df.describe())
