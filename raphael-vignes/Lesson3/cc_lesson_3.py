import requests
import numpy as np
import json


def getMeanDiscountByProductForABrand(url, apiKey, product, brand, number_of_pages):
    discounts = []
    for nb in range(nb_page) :
        post_datas = {
                "ApiKey":apiKey,
                "SearchRequest":
                    {
                        "Keyword":product, "SortBy":"relevance", "Pagination":{"ItemsPerPage":10, "PageNumber":nb},
                        "Filters":
                            {
                                "Price":{"Min":0, "Max":9999},
                                "Navigation":"all", "IncludeMarketPlace":"false", "Brands":[brand], "Condition":"new"
                            }
                    }
            }
        json_datas = json.dumps(post_datas, ensure_ascii = False)
        request = requests.post(url, json_datas)
        result = json.loads(request.text)
        try :
            for prod in result.get('Products'):
                p_name = prod.get('Name')
                best_offer = prod.get('BestOffer')
                priceDetails = best_offer.get('PriceDetails')
                ref_price = float(priceDetails.get('ReferencePrice').split('.')[0])
                saving = priceDetails.get('Saving')
                if not(saving) : continue
                discount = float(saving.get('Value').split('\\.')[0])
                discount_rate = 1.0 - (ref_price - discount) / ref_price
                discounts.append(discount_rate)
        except :
                continue
    return np.mean(discounts)

product = ['ordinateur']
liste_marque = ['dell','acer']
url_search = 'https://api.cdiscount.com/OpenApi/json/Search'
my_key = '19babd20-2093-400c-ad40-8b4e99298775'
nb_page = 5

for marque in liste_marque:
    print(marque)
    print(getMeanDiscountByProductForABrand(url_search, my_key, product[0], marque, nb_page))
