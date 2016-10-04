import requests
from bs4 import BeautifulSoup

url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2010"

def dataForYear(year):
	url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(year)
	r = requests.get(url)
	soup = BeautifulSoup(r.text,"html.parser")
	return getEuro(soup)

def getSpecifyLineData(soup,index):
	return soup.find_all(class_ = "montantpetit G")[index].text.replace('\xa0','')

def getEuro(soup):
	dico = {}
	dico['europarhabitantA'] = getSpecifyLineData(soup,1)
	dico['europarstrateA'] = getSpecifyLineData(soup,2)
	dico['europarhabitantB'] = getSpecifyLineData(soup,4)
	dico['europarstrateB'] = getSpecifyLineData(soup,5)
	dico['europarhabitantC'] = getSpecifyLineData(soup,10)
	dico['europarstrateC'] = getSpecifyLineData(soup,11)
	dico['europarhabitantD'] = getSpecifyLineData(soup,13)
	dico['europarstrateD'] = getSpecifyLineData(soup,14)

	return dico

def printData(dico):
	print("Euro par habitant A : " + dico['europarhabitantA'] + " -- Moyenne de la strate A : " + dico['europarstrateA'])
	print("Euro par habitant B : " + dico['europarhabitantB'] + " -- Moyenne de la strate B : " + dico['europarstrateB'])
	print("Euro par habitant C : " + dico['europarhabitantC'] + " -- Moyenne de la strate C : " + dico['europarstrateC'])
	print("Euro par habitant D : " + dico['europarhabitantD'] + " -- Moyenne de la strate D : " + dico['europarstrateD'])

for year in range(2010,2014):
	dico = dataForYear(year)
	print("-----" + str(year) + "-----")
	printData(dico)