# coding: utf8
from bs4 import BeautifulSoup
import requests


BRANDS = ['dell','acer']

def get_DOM(brand,page_number):
    url = "http://www.cdiscount.com/search/10/ordinateur+portable.html?\
                    TechnicalForm.SiteMapNodeId=0\
                    &TechnicalForm.DepartmentId=10\
                    &TechnicalForm.ProductId=\
                    &hdnPageType=Search\
                    &TechnicalForm.SellerId=\
                    &TechnicalForm.PageType=SEARCH_AJAX\
                    &TechnicalForm.LazyLoading.ProductSheets=False\
                    &NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01\
                    &FacetForm.SelectedFacets%5B4%5D=f%2F6%2" + brand + "\
                    &GeolocForm.ConfirmedGeolocAddress=\
                    &SortForm.SelectedSort=PERTINENCE\
                    &ProductListTechnicalForm.Keyword=ordinateur%2Bportable\
                    &page="+str(page_number)+"\
                    &_his_"
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def get_discount_by_page(soup, promos):
    produits = soup.find_all("div", {"class": "prdtBloc"})
    for produit in produits:
        brand = get_brand(produit)
        intial_price_tag = produit.find("div",{"class":"prdtPrSt"})
        # La marque est parmi celles qui nous intéressent et le produit dispose d'une promo
        if brand and intial_price_tag:
            get_product_discount(produit,brand, intial_price_tag,promos)

def get_product_discount(produit, brand, intial_price_tag, promos):
    initial_product_price = intial_price_tag.text
    price_tag = produit.find("span", {"class": "price"})
    discounted_product_price = get_cents(price_tag)
    promos[brand].append({"before": initial_product_price, "after": discounted_product_price})

def get_brand(produit):
    for b in BRANDS:
        if b in produit.find('div', {'class': 'prdtBTit'}).string.lower():
            return b
    return ""

def get_cents(price_tag):
    discounted_product_price_str = price_tag.text
    # if price 135€00, remove the cents part
    discounted_product_price_str = discounted_product_price_str.split('€')[0]
    discounted_product_additional_cents = price_tag.find('sup').text.replace('€', '')
    discounted_product_price = int(discounted_product_price_str)
    if discounted_product_additional_cents:
        discounted_product_price = discounted_product_price + int(discounted_product_additional_cents) / 100
    return discounted_product_price

def get_all_discount(promos):
    for brand in BRANDS:
        soup = get_DOM(brand,1)
        #Je n'utilise pas le vrai page number car le temps de réponse est trop long. On se limitiera ici à 2 pages pour chaque marque
        #total_page_number = int(soup.find('input',{"id":"PaginationForm_TotalPage"})["value"])
        total_page_number = 1

        # Scrappe les promos de la 1ere page
        get_discount_by_page(soup, promos)

        # Scrappe les pages suivantes
        for page in range(2,total_page_number):
            soup = get_DOM(brand, page)
            get_discount_by_page(soup, promos)


def main():
    promos = {"acer":[],"dell":[]}
    get_all_discount(promos)
    for brand, promos_list in promos.items():
        print("***********  BRAND ************")
        #print("Total euros saved for {} for {} laptops : {}".format(len(promos_list)),sum( price.before - price.after for price in [promos_list] ) )
    print(promos)
    #TODO : Calculer les pourcentages correspondants

main()





