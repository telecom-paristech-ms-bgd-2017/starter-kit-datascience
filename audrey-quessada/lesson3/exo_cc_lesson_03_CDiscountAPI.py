import requests
import numpy as np
import json
myKey = "c0a67d5c-79a1-4188-bb8b-965509e6a824"
product = "ordinateur"
#brand = "acer"
#créer une API pour chercher les produits d'intérêts sur CDiscount
def get_the_indicator(brand, nb_page):
    indicator = []
    for i in range(nb_page):
        data_request = {
            "ApiKey": myKey,
            "SearchRequest": {
                "Keyword": product,
                "SortBy": "relevance",
                "Pagination": {
                    "ItemsPerPage": 5,
                    "PageNumber": i
                },
                "Filters": {
                    "Price": {
                        "Min": 0,
                        "Max": 10000
                    },
                    "Navigation": "computers",
                    "IncludeMarketPlace": 'false',
                    "Brands": [
                        brand
                    ],
                    "Condition": "new"
                }
            }
        }
        data_json = json.dumps(data_request)  # , ensure_ascii=False
        request = requests.post('https://api.cdiscount.com/OpenApi/json/Search', data_json)
        res = json.loads(request.text)
        # print(res)
        count = 0
        total_discount_per_brand = []
        for el in res.get("Products"):
            best_offer = el.get("BestOffer")
            price_detail = best_offer.get("PriceDetails")
            original_price = float(price_detail.get("ReferencePrice").split('\\.')[0])
            saving = price_detail.get("Saving")
            if not (saving): continue
            discount = float(saving.get("Value").split('\\.')[0])
            count += 1
            percentage_discount = (original_price - discount) / original_price
            total_discount_per_brand.append(percentage_discount)
        print(count)
        print(total_discount_per_brand)
        indicator1 = np.mean(total_discount_per_brand)
        indicator.append(indicator1)

    return indicator

get_the_indicator("asus", 5)
get_the_indicator("dell", 5)
