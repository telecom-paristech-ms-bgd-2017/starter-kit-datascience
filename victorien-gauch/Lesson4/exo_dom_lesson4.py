import requests
from bs4 import BeautifulSoup

def getData():
	
	url = requests.get('https://gist.github.com/paulmillr/2657075')
	soup = BeautifulSoup(url.text,'html.parser')
	tab = getLine(soup)
	users = []
	for el in range(1,len(tab)):
		users.append(tab[el].find_all('td')[0].text.split(' ')[0])
	return users

def getLine(soup):
  return soup.find_all('tr')

users = getData()

def getStars(id_user):
	headers = {'Accept' : 'application/vnd.github.damage-preview','Authorization': 'Basic dmljbzkyOkZvb3RiYWxsOTI='}
	url = requests.get('https://api.github.com/users/' + str(id_user) + '/repos',headers=headers)
	content = url.json()
	count = 0

	if len(content) != 0:
		for c in content:
			count += c['stargazers_count']
		count /= float(len(content))
	return count

def getStarsForAllusers(users):
	tab = []
	#header = {'Accept' : 'application/vnd.github.damage-preview','Authorization': 'Basic dmljbzkyOkZvb3RiYWxsOTI='}
	#requests.put('https://api.github.com/authorizations/clients/vico92')
	for el in users:
		dico = {}
		dico['users'] = el
		dico['mean'] = getStars(el)
		tab.append(dico)
	
	tab = rank(tab)
	return tab

def rank(results):
	return sorted(results,key= lambda users: users['mean'], reverse=True)

result = getStarsForAllusers(users)

print(result)



