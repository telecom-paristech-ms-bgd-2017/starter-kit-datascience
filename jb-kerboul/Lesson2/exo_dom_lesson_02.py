

import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen


def readUrl(urlI):
	result = requests.get(urlI)
	soup = bs4(result.text, 'html.parser')
	return soup


def getValues(soup, listAttr):
	dico=dict()
	try: 
		objLibelle = soup.find_all(class_='libellepetit')
		for curObj in objLibelle:
			if any(curObj.text.find(x)>0 for x in listAttr):
				parObj=curObj.parent
				eurValHab=int(parObj.find_all(class_='montantpetit G')[1].text.replace(u'\xa0','').replace(' ',''))
				eurValStrat=int(parObj.find_all(class_='montantpetit G')[2].text.replace(u'\xa0','').replace(' ',''))
				dico[curObj.text]=[eurValHab, eurValStrat]	
	except ValueError :
		print('no data')
	return dico


urlMain = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
urlAnnee = list(range(2009, 2014))

listAttr = ([r"FONCTIONNEMENT = A",
             r"FONCTIONNEMENT = B",
             r"INVESTISSEMENT = C",
             r"INVESTISSEMENT = D"])
valOrg=dict()
for ii in urlAnnee:
	urlI = urlMain + str(ii)
	soup = readUrl(urlI)
	valOrg[str(ii)] = getValues(soup, listAttr)
	print(valOrg[str(ii)])




# DEbug marche pas

# fieldInteret=['Euros par habitant', 'Moyenne de la strate']
# findColInd=soup.find_all('tr')[7]
# for ii in findColInd:
# 	print(ii)
	


# 	temp = findColInd[ii].text
# 	tutu=[temp.find(x)>0 for x in fieldInteret]