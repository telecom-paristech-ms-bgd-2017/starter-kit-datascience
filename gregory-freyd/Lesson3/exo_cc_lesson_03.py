import requests
from bs4 import BeautifulSoup

def computeOriginalPrice(original_price_soup):
    """
    Returns original price without discount
    from soup containing price
    """
    if original_price_soup is None or original_price_soup == "":
        return 0
    else:
        res_str = original_price_soup.text.replace(u'\xa0', '').replace(",", ".")
        if res_str == "":
            return 0
    return float(res_str)

def computePrice(price_soup):
    """
    Returns discounted price
    from soup containing price
    """
    res_str = price_soup.text.replace(u'\xa0', '').replace(u'\N{euro sign}', ".")
    return float(res_str)

def getMeanDiscount(computer_brand):
    """
    Returns average discount rate
    for a computer brand
    """
    all_metrics = []
    MAX_PAGE = 1
    sum_original_prices = 0
    sum_discount_prices = 0
    for page in range(1, MAX_PAGE + 1):
        all_laptop_brand = requests.get("http://www.cdiscount.com/search/10/ordinateur+" +
                                        computer_brand + "+.html?page=" + str(page))
        soup_brand = BeautifulSoup(all_laptop_brand.text, 'html.parser')
        list_laptop = soup_brand.find_all(class_="prdtBloc")
        # for each laptop getting its original and discounted price and summing in two variables
        for laptop in list_laptop:
            price_soup = laptop.find(class_="price")

            original_price_soup = laptop.find(class_="prdtPrSt")
            discount_price = computePrice(price_soup)
            original_price = computeOriginalPrice(original_price_soup)
            if original_price == 0:
                original_price = discount_price
            sum_original_prices = sum_original_prices + original_price
            sum_discount_prices = sum_discount_prices + discount_price
            # ratio includes also prices of products on which no discount is
            # applied, in this case original_price = discount_price
            # the average discount ratio is considered on the complete
            # product offering of computers from the brand
    return (1 - sum_discount_prices / sum_original_prices)

mean_discount_acer = getMeanDiscount('acer')
print("Discount moyen pour les ordinateurs portables Acer : " + '{0:.2f}'.format(mean_discount_acer * 100) + "%")
mean_discount_dell = getMeanDiscount('dell')
print("Discount moyen pour les ordinateurs portables Dell : " + '{0:.2f}'.format(mean_discount_dell * 100) + "%")
