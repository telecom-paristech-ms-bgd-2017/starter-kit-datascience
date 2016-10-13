import requests
import json
from pprint import pprint

##############
# CONSTANTES #
##############
base_url_api = "https://api.cdiscount.com/OpenApi/json/Search"

#############
# FONCTIONS #
#############
def getDiscountPricesAPI(brand):
    json_template = open('api_params.json')
    json_req = json.load(json_template)
    json_req['SearchRequest']['Filters']['Brands'] = [brand]

    step = 100
    p_max = 2000
    for min_price in range(0, p_max, step):
        json_req['SearchRequest']['Filters']['Price']['Min'] = min_price
        json_req['SearchRequest']['Filters']['Price']['Max'] = min_price + step

        # Had to use json.dumps because calling str on json_req leaves ' characters
        pprint(json_req['SearchRequest']['Filters']['Price'])
        resp = requests.post(base_url_api, data=json.dumps(json_req))
        offers = json.loads(resp.text)['Products']
        for offer in offers:
            pprint(offer['BestOffer']['SalePrice'])

########
# MAIN #
########
def main():
    acer_discounts = getDiscountPricesAPI("acer")
    # dell_prices = getCDiscountPrices("dell")


if __name__ == '__main__':
    main()