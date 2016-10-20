from bs4 import BeautifulSoup
from multiprocessing import Pool
from splinter import Browser
from selenium.webdriver.support.ui import WebDriverWait
from splinter.exceptions import ElementDoesNotExist
from collections import defaultdict
import re, json, requests, time

url_leboncoin = 'https://www.leboncoin.fr/voitures/offres/'
phone_number_url = 'https://api.leboncoin.fr/api/utils/phonenumber.json'
url_lacentrale = 'http://www.lacentrale.fr/cote-auto-renault-zoe-'
api_key = '54bb0281238b45a03f0ee695f73e704f'
app_id = 'leboncoin_web_utils'
search_params = {'q':'zoe', 'it': 1}

cats = ['url', 'annee', 'km', 'prix', 'titre', 'offres', 'description']
num_cats = ['annee', 'km', 'prix']
versions = ['life', 'zen', 'intens']

re_int = re.compile(r'\d+')
re_version = re.compile('|'.join(versions), re.IGNORECASE)
re_vendeur = re.compile(r'pro|part')
re_ref = re.compile(r'https?:\/\/www\.leboncoin\.fr\/voitures\/(\d+)\.htm')

browser = None


def data_by_region(region):
    html = requests.get(url_leboncoin + region, params=search_params).text
    list_ads = BeautifulSoup(html, 'html.parser').select('#listingAds ul')[0]
    links = ['http:' + a['href'] for a in list_ads.select('li > a')]

    with Pool() as pool:
        info = pool.map(get_info, links)
    pool.join()
    with Pool() as pool:
        info_clean = pool.map(clean_info, info)
    return info_clean

def get_info(url):
    s = BeautifulSoup(requests.get(url).text, 'html.parser')
    script = s.select('body')[0].select('script')[2].text
    bits = list(map(lambda b: b.strip().split(' : '), script.split('\n')))
    bits = {b[0]: b[1] for b in bits if len(b) == 2}
    bits['description'] = s.select('p[itemprop="description"]')[0].text
    # bits['url'] = url
    return bits

def clean_info(info):
    clean_info = {cat: parse_int(info[cat]) for cat in num_cats}
    clean_info['version'] = parse_version(info['titre'] + info['description'])
    # clean_info['vendeur'] = parse_vendeur(info['offres'])
    # ref = int(re_ref.search(info['url']).group(1))
    # clean_info['ref'] = ref

    # data = {'list_id': ref,'app_id': app_id,'text': 1,'key': api_key}
    # resp = requests.post(phone_number_url, data=data).text
    # j = json.loads(resp)['utils']
    # clean_info['phone number'] = j['phonenumber'] if j['status'] == 'OK' else ''

    return clean_info

def navigate_to(version, annee):
    browser.visit(url_lacentrale + version + '-' + str(annee) + '.html')

def get_prix_lacentrale(km):
    browser.find_by_id('km')[0].fill(km)
    browser.find_by_id('btnVendeur')[0].click()
    time.sleep(2)
    return browser.find_by_css('.jsCoteAffinee')[0].text.replace(' ', '')

def parse_vendeur(s):
    return re_vendeur.search(s).group(0)

def parse_int(s):
    return int(re_int.search(s).group(0))

def parse_version(s):
    m = re_version.search(s)
    return m.group(0).lower() if m else ''

def open_browser():
    global browser
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)

def est_cotee():
    try:
        browser.find_by_id('btnVendeur')[0]
        return True
    except ElementDoesNotExist:
        return False

# regions = ['provence_alpes_cote_d_azur', 'ile_de_france', 'aquitaine']
# all_data = [d for reg in regions for d in data_by_region(reg)]
# with open('output.json', 'w+') as outfile:
#     json.dump(all_data, outfile)


all_data = json.loads(open('output.json', 'r').read())
lc_roadmap = {v: defaultdict(list) for v in versions}
for i, d in enumerate(all_data):
    if d['version']:
        lc_roadmap[d['version']][d['annee']].append((i, d['km']))

open_browser()
for version in versions:
    for annee in lc_roadmap[version].keys():
        navigate_to(version, annee)
        if (est_cotee()):
            for i, km in lc_roadmap[version][annee]:
                print(','.join([version, str(annee), str(km)]))
                all_data[i]['prix lacentrale'] = get_prix_lacentrale(km)

print(all_data)

with open('output2.json', 'w+') as otherfile:
    json.dump(all_data, otherfile)

browser.quit()
