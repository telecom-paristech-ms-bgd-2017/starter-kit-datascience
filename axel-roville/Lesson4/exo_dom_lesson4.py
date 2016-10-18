from bs4 import BeautifulSoup
import requests as req
import re

url_base = 'https://www.leboncoin.fr/voitures/offres/'
regex_int = re.compile('\d*')
regex_version = re.compile('life|zen|intens', re.IGNORECASE)

def url(region):
    return

def data_by_region(region):
    html = req.get(url_base + region + '?q=renault%20zoe').text
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.select('#listingAds ul')[0]
    links = ul.select('li > a')
    for link in links[:5]:
        s = BeautifulSoup(req.get('http:' + link['href']).text, 'html.parser')
        lines = s.select('section .properties')[0].select('.line')
        
        price = parse_int(lines[2].select('span')[1].text)
        year = parse_int(lines[6].select('span')[1].text)
        version = parse_version(lines[11].select('.value')[0].text)

        print('year:', year, '\tprice:', price, '\tversion:', version)

def parse_int(s):
    m = regex_int.search(s.strip().replace(' ', ''))
    return m.group(0)

def parse_version(s):
    m = regex_version.search(s)
    return m.group(0).lower() if m else ''

data_by_region('provence_alpes_cote_d_azur')