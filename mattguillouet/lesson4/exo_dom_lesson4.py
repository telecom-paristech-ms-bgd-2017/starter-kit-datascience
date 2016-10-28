import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import json
import re
import json
import ipdb


def getAttr(prop, listSoup):

    for s in listSoup:
        if s.find('span', {'class': 'property'}).text.lower().replace('é', 'e').replace('è', 'e') == prop:
            return s.find('span', {'class': 'value'}).text.strip()


regions = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']
versions = ['intens', 'zen', 'life']

#for reg in regions:
baseUrl = 'https://www.leboncoin.fr/annonces/offres/{0}/?o={1}&q=Renault%20Zo%E9'

selectedCat = 'voitures'
voitures = []

regExpPhoneNb = re.compile('(0{1}[1-7][\.-]?\d{2}[\.-]?\d{2}[\.-]?\d{2}[\.-]?\d{2})')
regExpUrl = re.compile('(www.+)')

for reg in regions:

	page = 1

	while 1 == 1:    
	    print('{0}: page {1}'.format(reg, page))

	    r = requests.get(baseUrl.format(reg, page))
	    soup = BeautifulSoup(r.content, 'html.parser')
	    selSection = soup.find('section', {'class': 'tabsContent block-white dontSwitch'})
	    
	    if selSection is None:
	        break

	    items = selSection.select('ul > li')

	    for item in items:
		    # first item_supp seems to always be the categorie
		    tmp = item.find(class_="item_supp")
		    if tmp is None:
		        continue

		    cat = tmp.text.lower()
		    if cat.find(selectedCat) == -1:
		        continue

		    # pro
		    isPro = tmp.find(class_="ispro") is not None and 1 or 0

		    # title
		    tmp1 = item.find(class_="item_title").text.strip().lower()

		    if tmp1.find('zoe') == -1 or tmp1.find('renault') == -1:
		    	continue 

		    ver = list(map(lambda x: not tmp1.find(x) == -1 and 1 or 0, versions))

		    # get url
		    itemUrl = item.find('a')['href']
		    matchUrl = regExpUrl.search(itemUrl)

		    # url not found
		    if matchUrl is None:
		        continue

		    matchUrl = matchUrl.group()
		    idItem = re.search('/(\d+).', matchUrl).group(1)

		    r_ = requests.get('http://' + matchUrl)

		    soup_ = BeautifulSoup(r_.content, 'html.parser')

		    infoSoup_ = soup_.find_all('h2', {'class': 'clearfix'})

		    item_detail = soup_.find(class_='item_price clearfix')
		    price = item_detail.attrs['content']
		    price = int(price)

		    kilometrage = getAttr('kilometrage', infoSoup_)
		    kilometrage = re.search('[\d ]+', kilometrage).group().strip()
		    kilometrage = kilometrage.replace(' ', '')
		    kilometrage = int(kilometrage)

		    anneModel = getAttr('annee-modele', infoSoup_)

		    # phone number
		    data = {'list_id': idItem, 'app_id': 'leboncoin_web_utils',
		             'key': '54bb0281238b45a03f0ee695f73e704f', 'text': 1}

		    # rPhone = requests.post('https://api.leboncoin.fr/api/utils/phonenumber.json', data=data)
		    # rPhone = json.loads(rPhone.text)

		    # if rPhone['utils']['status'] == 'OK':
		    #     phoneNumber = rPhone['utils']['phonenumber']
		    # else:
		    #     phoneNumber = 'none'

		    description = soup_.find('p',{'itemprop':'description'}).text.lower()

		    phoneNb = regExpPhoneNb.search(description)

		    if not phoneNb is None:
		    	phoneNumber = phoneNb.group().replace('-','').replace('.','')
		    else:
		    	phoneNumber = 'none'
		    
		    # in case test with description
		    if not 1 in ver:
		    	ver = list(map(lambda x: not description.find(x) == -1 and 1 or 0, versions))
		    
		    if not 1 in ver:
		    	version = 'none'
		    else:
		    	version = versions[ver.index(1)]

		    typeVersion = not description.find('type 2') == -1 and 2 or 1 

		    itemDict = {'isPro': isPro, 'version': version, 'type': typeVersion, 'annee': anneModel, 'kilo': kilometrage, 'price': price, 'phoneNumber': phoneNumber}

		    voitures.append(itemDict)

	    page += 1

dfVoitures = pd.DataFrame(voitures)

# get cote 2013
baseUrlCote = 'http://www.lacentrale.fr/'
coteUrl = baseUrlCote + 'cote-voitures-renault-zoe--2013-.html'
r_cote = requests.get(coteUrl)
soup_cote = BeautifulSoup(r_cote.content, 'html.parser')

allZoe = soup_cote.find_all('div', {'class': 'listingResultLine f14 auto'})

cotes = dict()
for cote in allZoe:

	zoeTitle = cote.find("h3", {"class": "f14"}).text.lower()

	typeVersion = not zoeTitle.find('type 2') == -1 and 2 or 1
	
	ver = list(map(lambda x: not zoeTitle.find(x) == -1 and 1 or 0, versions))
	version = versions[ver.index(1)]

	urlZoe = baseUrlCote + cote.find('a')['href']
	soupZoe = BeautifulSoup(requests.get(urlZoe).content, 'html.parser')

	soupZoe.find('strong', {'class': 'f24 bGrey9L txtRed pL15 mL15'})

	cotePrice = soupZoe.find('strong', {'class': 'f24 bGrey9L txtRed pL15 mL15'}).text.strip().replace('€','').replace(' ','')

	cotes[(version, typeVersion)] = int(cotePrice)


coteCol = list(map(lambda x: cotes[x], list(zip(dfVoitures['version'], dfVoitures['type']))))
plusMoinsCher = list(map(lambda x: x[0] > x[1] and '-' or '+', list(zip(coteCol, dfVoitures['price'])))) 

# add columns
dfVoitures['cote'] = pd.Series(coteCol, index=dfVoitures.index)
dfVoitures['affaire'] = pd.Series(plusMoinsCher, index=dfVoitures.index)


dfVoitures.to_csv('renault_zoe_leboncoin.csv')






