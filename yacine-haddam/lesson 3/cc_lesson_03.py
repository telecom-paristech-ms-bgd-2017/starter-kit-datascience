import requests
from bs4 import BeautifulSoup
import pandas as pd


def products_brand_page (brand, page):
    html = requests.get('http://www.cdiscount.com/search/10/' + brand + '.html?&page=' + str(page) + '#_his_')
    soup = BeautifulSoup(html.text, 'html.parser')
    products = soup.find_all(class_="prdtBloc")
    return products


def products_brand(brand, pages=1):

    products_list = []

    for i in range(1, pages+1):

        products = products_brand_page(brand, i)
        products_list.extend(describ_product(products))

    return products_list


def describ_product(products):
    sheet_product = []
    for i in range(0, len(products)):
        sheet = {}
        product_name = products[i].find(class_="prdtBTit").text.replace('\xa0', '')
        old_price = products[i].find(class_="prdtPrSt")
        new_price = products[i].find(class_="price")

        if old_price == None or old_price.text == '':
            sheet['Produit'] = product_name
            sheet['ancien_prix'] = float(new_price.text.replace('\xa0', '').replace('€', '.'))
            sheet['prix'] = float(new_price.text.replace('\xa0', '').replace('€', '.'))
            sheet['discount'] = 0
        else:
            sheet['Produit'] = product_name
            sheet['ancien_prix'] = float(old_price.text.replace('\xa0', '').replace(',', '.'))
            sheet['prix'] = float(new_price.text.replace('\xa0', '').replace('€', '.'))
            sheet['discount'] = round((sheet['ancien_prix'] - sheet['prix']), 2)

        sheet_product.append(sheet)
    return sheet_product


def discount_metric(product_list):
    results = []
    Y = pd.DataFrame(product_list)
    number_product = Y['Produit'].count()
    results.append(number_product)
    number_product_discount = Y['Produit'][(Y['discount']!= 0)].count()
    results.append(number_product_discount)
    mean_discount = round((Y['discount'].mean()), 2)
    results.append(mean_discount)
    rate_discount = pd.DataFrame(((Y['discount']/Y['ancien_prix'])*100))
    mean_rate_discount = round((rate_discount.mean()[0]), 2)
    results.append(mean_rate_discount)

    print('Nombre de produit: ' + str(number_product))
    print('Nombre de produit avec remise: ' + str(number_product_discount))
    print('Remise moyenne: ' + str(mean_discount) +' €' )
    print('Taux de remise:'+ str(mean_rate_discount) + " %")

    return results


if __name__ == "__main__":
    nb_pages=10
    acer_product = products_brand('acer pc', nb_pages)
    dell_product = products_brand('dell pc', nb_pages)

    print('Comparaison des remises sur les pc de marque acer et dell')

    print('==========================================================')
    print ('ACER\n')

    discount_metric(acer_product)

    print('\n==========================================================')
    print ('DELL\n')

    discount_metric(dell_product)
