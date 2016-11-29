import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

car_quote_buffer = {}

def getCarQuote(version, year):
    """Retrieves car quote from
    lacentrale website
    """
    price = 'N/A'
    url1 = 'http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide-{year}.html'
    url2 = 'http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide+gamme+{nyear}-{year}.html'
    nyear = int(year) + 1
    if (version, year) not in car_quote_buffer:
        for url in [url1.format(version=version, year=year),
                    url2.format(version=version, year=year, nyear=nyear)]:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            h2 = soup.find('h2', string=re.compile(r"\s*Cote\s+brute\s*"))
            if h2:
                h2 = h2.parent.find(class_="txtRed")
                if h2:
                    price = h2.text.replace(u'\xa0', '').replace(' ', '').replace(u'\N{euro sign}', "")\
                        .replace("\n", "")
                    car_quote_buffer[(version, year)] = price
                    return price
            return 'N/A'
    return price

def extractPhoneFromDOM(soup):
    """Extracts phone number
    from car ad webpage html code
    """
    match_result = re.match(".*[^\d]((\s?\d){9,10}).*", soup.find(itemprop="description").text.lower()
                                                            .replace(u'\xa0','').replace('\n', ' '))
    phone_number = match_result.group(1).replace(' ', '') if match_result is not None else ''
    if len(phone_number) == 9:
        phone = "0" + phone_number
    return str(phone_number)

def extractMileageFromDOM(soup):
    """Extracts mileage
    from car ad webpage html code
    """
    res_str_list = soup.find_all(class_="clearfix")
    for item in res_str_list:
        if "Kilométrage" in item.text:
                return (int(item.find(class_="value").text.replace(u'\xa0','').replace(" ", "").replace('KM', "")))
    return 0

def extractPriceFromDOM(soup):
    """Extracts car price
    from car ad webpage html code
    """
    res_str = soup.find(itemprop="price").find(class_="value").text.replace(u'\xa0','')\
        .replace(u'\N{euro sign}', "").replace(" ", "").replace('\n', "")
    return (int(res_str))

def extractYearFromDOM(soup):
    """Extracts car model year
    from car ad webpage html code
    """
    res_str = soup.find(itemprop="releaseDate").text.replace(u'\xa0','')
    res = int(res_str)
    return (int(res))

def extractVersionFromDOM(soup):
    """Extracts commercial version
    from car ad webpage html code
    """
    soup_text_upper_case = soup.text.upper()
    if "ZEN" in soup_text_upper_case:
        return "Zen"
    elif "LIFE" in soup_text_upper_case:
        return "Life"
    elif "INTENS" in soup_text_upper_case:
        return "Intens"
    else:
        return "N/A"


def fillInfoFromPage(url, seller_type, zoe_info_list_):
    """Process info located into the
    car ad webpage html code
    """
    zoe_info_df = pd.DataFrame(columns=['url', 'version', 'year', 'mileage', 'seller_type', 'phone', 'price'])

    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    version = extractVersionFromDOM(soup)
    year = extractYearFromDOM(soup)
    mileage = extractMileageFromDOM(soup)
    price = extractPriceFromDOM(soup)
    phone = extractPhoneFromDOM(soup)

    zoe_info_list = zoe_info_list_.append(({'url': url,
                                      'seller_type': seller_type,
                                      'version': version,
                                      'year': year,
                                      'mileage': mileage,
                                      'phone': phone,
                                      'price': price,
                                      }))#,
    return zoe_info_list_

def resultToCleanDataFrame(zoe_info_list):
    """Gathering info into a clean
    dataframe as a result
    """
    zoe_info_df = pd.DataFrame.from_records(zoe_info_list,
                        columns=['url', 'version', 'year', 'mileage', 'seller_type', 'phone', 'price'])
    zoe_info_df['phone'].astype(str)
    zoe_info_df = zoe_info_df.drop(['url'], axis=1)
    zoe_info_df['quote'] = zoe_info_df[['version', 'year']].apply(lambda x: getCarQuote(*x), axis=1)
    print(zoe_info_df)
    zoe_info_df.to_csv("zoe_data.csv", sep=';', encoding='utf-8')
    return zoe_info_df

def getAllAdsInfoForZoe():
    """Loops on all available ads
    for Zoe car model
    """
    all_metrics = []
    MAX_PAGE = 10
    zoe_info_list = []

    for page in range(1, MAX_PAGE + 1):
        base_url = requests.get('https://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/occasions/?o=' + str(page) + '&q=renault%20zoe')
        soup_car = BeautifulSoup(base_url.text, 'html.parser')
        infos_zoe = soup_car.find_all(class_="list_item clearfix trackable")

        for url in infos_zoe:
            url_address = "https:" + url['href']

            if url.find(class_="ispro"):
                seller_type = 'Professional'
            else:
                seller_type = 'Individual'
            zoe_info_list = (fillInfoFromPage(url_address, seller_type, zoe_info_list))

        resultToCleanDataFrame(zoe_info_list)
    return all_metrics

info_ads_zoe = getAllAdsInfoForZoe()
