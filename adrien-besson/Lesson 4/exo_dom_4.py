# coding: utf-8

import requests
from bs4 import BeautifulSoup

def loadHtml():
	url = "https://gist.github.com/paulmillr/2657075"
	r = requests.get(url)
	return BeautifulSoup(r.text,"html.parser")

def loadtopcontributors(soup):
	soup = loadHtml()
	tab = soup.find_all("tr")
	array = []

	for i in range(1,len(tab)):
		array.append(tab[i].find_all("td")[0].text.split(' ')[0])

	return array

def getMeanOfStars(contributor_id):
	headers = {"Authorization": "token 4eb133ca065dbe251ad5676af1a557eb2512bb69"}
	r = requests.get('https://api.github.com/users/' + contributor_id + '/repos',headers=headers)
	json = r.json()
	stargazers_count = 0

	if len(json) != 0:
		for repo in json:
			stargazers_count += repo['stargazers_count']

		stargazers_count /= float(len(json))
		
		return stargazers_count

	else:
		return 0.

def meanRateOfTopContributors(contributors):
	meanRates = []

	for contributor in contributors:
		dico = {}
		dico['Contributor_id'] = contributor
		dico['Note_moyenne'] = getMeanOfStars(contributor)
		meanRates.append(dico)

	return meanRates

def rankByMeanRates(list_of_data):
	return sorted(list_of_data, key=lambda contributor: contributor['Note_moyenne'] , reverse=True)

def getRankTopContributorsByMeanRate():
	meanRates = meanRateOfTopContributors(loadtopcontributors(loadHtml()))
	meanRates = rankByMeanRates(meanRates)
	return meanRates

print(getRankTopContributorsByMeanRate())