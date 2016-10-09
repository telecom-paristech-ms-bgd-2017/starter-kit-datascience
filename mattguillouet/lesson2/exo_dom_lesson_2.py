import requests
from bs4 import BeautifulSoup
import sys



def getData(crawl, cat):

	record = False
	catList = []
	for c in crawl:
		
		if not c['rowTitle'].find(cat)==-1:
			record = True
			catList.append(c)
			continue
		
		if record and c['cat']=='Big':
			break


		if record:
			catList.append(c)

	return catList



urlbase = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'

years = [2010, 2011, 2012, 2013]
postDict = {'icom':'056', 'dep':'075', 'type':'BPS', 'param':'5'}
results = dict()

for year in years:

	postDict['exercice'] = year
	r = requests.get(urlbase, params = postDict)

	soup = BeautifulSoup(r.content, 'html.parser')


	baseStr = 'table:nth-of-type(3) > tr:nth-of-type({0}) > td:nth-of-type({1})'

	crawl = []
	iRow = 6
	res = soup.select(baseStr.format(iRow, 4))
	while not len(res)==0:

		if not 'class' in res[0].attrs:
			iRow += 1
			res = soup.select(baseStr.format(iRow, 4))
			continue
		
		classes = res[0]['class']

		if ('libellepetit' in classes) or ('libellepetitIi' in classes) or ('libellepetitiI' in classes):

			eurosHab = soup.select(baseStr.format(iRow, 2))[0].text.replace('\xa0','')
			moyenneStrate = soup.select(baseStr.format(iRow, 3))[0].text.replace('\xa0','')
			titleRow = soup.select(baseStr.format(iRow, 4))[0].text.replace('\xa0','')

			if 'G' in classes:
				whichTitle = 'Big'
			elif 'libellepetitIi' in classes:
			 	whichTitle = 'Little'
			else:
				whichTitle = 'Medium'

			
			crawl.append({'eurosPerHab': eurosHab, 'moyStrate': moyenneStrate, 'rowTitle': titleRow, 'cat':whichTitle})

		iRow += 1
		res = soup.select(baseStr.format(iRow, 4))



	dataA = getData(crawl, '= A')
	dataB = getData(crawl, '= B')
	dataC = getData(crawl, '= C')
	dataD = getData(crawl, '= D')

	results[str(year)] = {'A': dataA, 'B': dataB, 'C': dataC, 'D': dataD}













