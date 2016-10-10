import requests
from bs4 import BeautifulSoup

# Base url for searching for computers of a specific brand on the cdiscount web site.
Base_url = 'http://www.cdiscount.com/search/10/ordinateur+<brand>.html'

# Parameters of the HTTP Get request.
Params = {
    'page': 1
}

# Fetches the serach result page for the specified brand and page number;
# returns the html content retrieved.
def load_search_page(brand, page):
    url = Base_url.replace('<brand>', brand)
    Params['page'] = page
    return requests.get(url, Params)


# Retrieves the list recommended retail prices and discount prices for computers of the specified brand from the designated
# search results page;
# returns a list of tuples <retail price, discounted price>.
def get_discounts_on_page(brand, page=1):
    data = load_search_page(brand, page)
    results = []
    parser = BeautifulSoup(data.text, 'html.parser')
    for node in parser.find_all(class_="prdtBZPrice"):
        discount_node = node.find(class_="prdtPrSt")
        if discount_node:
            price_node = node.find(class_="price")
            if price_node:
                try:
                    price = extract_price(price_node)
                    discount = extract_price(discount_node)
                    results.append([price, discount])
                except ValueError:
                    pass
    print(results)
    return results


# Extracts the price from the text of the designated DOM node.
def extract_price(node):
    return float(node.text.replace(u'\xa0', '').replace(u' ', '').replace(u'€', '.').replace(u',', u'.'))


# Retrieves the list of recommended retail prices and discount prices for computers of the specified brand from the first
# search results pages;
# returns a list of tuples <retail price, discounted price>.
def get_discounts(brand, pages=10):
    results = []
    for page in range(1, pages):
        results.extend(get_discounts_on_page(brand, page=page))
    return results


def test(pages):
    discounts_dell = get_discounts('dell', pages)
    discounts_acer = get_discounts('acer', pages)
    average_discounts_dell = (sum(map(lambda v: v[0], discounts_dell)) - sum(map(lambda v: v[1], discounts_dell))) \
                            / sum(map(lambda v: v[0], discounts_dell))
    print(discounts_dell)
    print(discounts_acer)
    average_discounts_acer = (sum(map(lambda v: v[0], discounts_acer)) - sum(map(lambda v: v[1], discounts_acer))) \
                            / sum(map(lambda v: v[0], discounts_acer))
    print("Average discounts for Dell from the %d first pages: %f" % (pages, average_discounts_dell))
    print("Average discounts for Acer from the %d first pages: %f" % (pages, average_discounts_acer))

test(4)