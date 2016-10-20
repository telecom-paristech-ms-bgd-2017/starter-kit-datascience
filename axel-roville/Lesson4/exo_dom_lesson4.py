from bs4 import BeautifulSoup
from multiprocessing import Pool
from splinter import Browser
from selenium.webdriver.support.ui import WebDriverWait
from splinter.exceptions import ElementDoesNotExist
from collections import defaultdict
import re, json, requests, time, csv

url_leboncoin = 'https://www.leboncoin.fr/voitures/offres/'
phone_number_url = 'https://api.leboncoin.fr/api/utils/phonenumber.json'
url_lacentrale = 'http://www.lacentrale.fr/cote-auto-renault-zoe-'
api_key = '54bb0281238b45a03f0ee695f73e704f'
app_id = 'leboncoin_web_utils'
search_params = {'q':'zoe', 'it': 1}

cols = ['version','annee','km','prix','prix lacentrale','comparaison lacentrale','phone','vendeur','ref']
cats = ['url', 'annee', 'km', 'prix', 'titre', 'offres', 'description']
num_cats = ['annee', 'km', 'prix']
versions = ['life', 'zen', 'intens']
regions = ['provence_alpes_cote_d_azur', 'ile_de_france', 'aquitaine']

re_int = re.compile(r'\d+')
re_phone = re.compile('(\d{2}).?(\d{2}).?(\d{2}).?(\d{2}).?(\d{2})')
re_version = re.compile('|'.join(versions), re.IGNORECASE)
re_vendeur = re.compile(r'pro|part')
re_ref = re.compile(r'https?:\/\/www\.leboncoin\.fr\/voitures\/(\d+)\.htm')

browser = None


def data_by_region(region):
    page_exists = True
    info_clean = []
    page_nb = 1
    while True:
        search_params['o'] = page_nb
        html = requests.get(url_leboncoin + region, params=search_params).text
        soup = BeautifulSoup(html, 'html.parser')
        page_exists = len(soup.select('#result_ad_not_found_proaccount')) == 0
        print(page_exists)
        if not page_exists:
            break;

        list_ads = soup.select('#listingAds ul')[0]
        links = ['http:' + a['href'] for a in list_ads.select('li > a')]

        info = Pool().map(get_info, links)
        info_clean.extend(Pool().map(clean_info, info))
        page_nb += 1

    return info_clean

def get_info(url):
    s = BeautifulSoup(requests.get(url).text, 'html.parser')
    script = s.select('body')[0].select('script')[2].text
    bits = list(map(lambda b: b.strip().split(' : '), script.split('\n')))
    bits = {b[0]: b[1] for b in bits if len(b) == 2}
    bits['description'] = s.select('p[itemprop="description"]')[0].text
    bits['url'] = url
    return bits

def clean_info(info):
    clean_info = {cat: parse_int(info[cat]) for cat in num_cats}
    clean_info['version'] = parse_version(info['titre'] + info['description'])
    clean_info['vendeur'] = parse_vendeur(info['offres'])
    clean_info['ref'] = int(re_ref.search(info['url']).group(1))
    try:
        clean_info['phone'] = ''.join(re_phone.search(info['description']).groups())
    except:
        pass
    # data = {'list_id': ref,'app_id': app_id,'text': 1,'key': api_key}
    # resp = requests.post(phone_number_url, data=data).text
    # j = json.loads(resp)['utils']
    # clean_info['phone'] = j['phonenumber'] if j['status'] == 'OK' else ''

    return clean_info

def navigate_to(version, annee):
    browser.visit(url_lacentrale + version + '-' + str(annee) + '.html')

def cote_ajustee(km):
    browser.find_by_id('km')[0].fill(km)

    btn = browser.find_by_id('btnVendeur')[0]
    count = 0
    while count < 5:
        try:
            browser.find_by_id('btnVendeur')[0].click()
            break
        except:
            time.sleep(1)
            count += 1

    cote_affinee = browser.find_by_css('.jsCoteAffinee')[0]
    count = 0
    while count < 5:
        try:
            return int(cote_affinee.text.replace(' ', ''))
        except:
            time.sleep(1)
            count += 1


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

def get_prix_lacentrale(all_data):
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
                    prix_lacentrale = cote_ajustee(km)
                    all_data[i]['prix lacentrale'] = prix_lacentrale
                    plus_cher = all_data[i]['prix'] > prix_lacentrale
                    all_data[i]['comparaison lacentrale'] = '+' if plus_cher else '-'
    browser.quit()
    return all_data


all_data = [d for reg in regions for d in data_by_region(reg)]
all_data = get_prix_lacentrale(all_data)
with open('result.csv', 'w+') as f:
    w = csv.DictWriter(f, cols)
    w.writeheader()
    w.writerows(all_data)


