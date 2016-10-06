import requests
from bs4 import BeautifulSoup

#import data
def GetData(url):
	request=requests.get(url)
	return BeautifulSoup(request.text, 'html.parser')

#Display result
def displayingStats(soup):
	rowNumbers=[3,7,15,20]
	for num in rowNumbers:
		extraction(num)

#Extract from url
def extraction(data):
	colNumbers=[2,3]
	TagList=soup.findAll( "tr", {"class" : "bleu"})[data]
	print TagList.select('td:nth-of-type('+ str(4) + ')')[0].text
	StrEuroPerCitizen = TagList.select('td:nth-of-type('+ str(colNumbers[0]) + ')')[0]
	StrMStrate = TagList.select('td:nth-of-type('+ str(colNumbers[1]) + ')')[0]
	print 'Result by Strate', int(StrMStrate.text.replace(u'\xa0',u'').replace(' ',''))
	print 'Result by Citizen',int(StrEuroPerCitizen.text.replace(u'\xa0',u'').replace(' ','')), '\n--------'

#Main_code
for year in range(2009, 2014):
	if year == 2009 :
		print 'Year ', year, '\n', 'No data available'
	else :
		print 'Year',year, '\n*******'
		url='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=%YEAR%'
		url = url.replace('%YEAR%', str(year))
		soup=GetData(url)
		displayingStats(soup)