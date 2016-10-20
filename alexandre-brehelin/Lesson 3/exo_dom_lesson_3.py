from lxml import html
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 



#### Scrap directement sur l'url sans utilisation de l'api
#### On stock les informations du classement dans une database rank 

url = 'https://gist.github.com/paulmillr/2657075'
page_git = requests.get(url)
soup = BeautifulSoup(page_git.text, 'html.parser')


rank = pd.DataFrame(np.nan, index=np.arange(1,257), columns=['Pseudo','Prenom','Nom','Contribs'])

def name(data):
	max_s = len(soup.select("td"))
	idx = 1
	for indice in np.arange(1,max_s,4):
		adresse = "td:nth-of-type("+str(indice)+")"
		n_p = soup.select(adresse)[0].text.replace('(','').replace(')','').split(" ")

		if len(n_p)==1:
			data.loc[idx,"Pseudo"] = n_p[0]
		elif len(n_p)==2 :
			data.loc[idx,"Pseudo"] = n_p[0]
			data.loc[idx,"Prenom"] = n_p[1]
		else :
			data.loc[idx,"Pseudo"] = n_p[0]
			data.loc[idx,"Prenom"] = n_p[1]
			data.loc[idx,"Nom"] = n_p[2]
		idx += 1 

def contribution(data):
	max_s = len(soup.select("td"))
	idx = 1
	for indice in np.arange(2,max_s,4):
		adresse = "td:nth-of-type("+str(indice)+")"
		n_p = soup.select(adresse)[0].text
		data.loc[idx,'Contribs']=n_p
		idx+=1

name(rank)
contribution(rank)
#### Utilisation de l'API GIT HUB 



def mean_star(contributor):

	ToKeN = 'a0b76931054c5abf1507255253c5a618e412e9a5'
	headers = {"Authorization": "token " + ToKeN}
	url="https://api.github.com/users/"+contributor+"/repos"
	request = requests.get(url,headers=headers)

	profil = request.json()

	sum_stars = 0
	mean_star = 0
	if len(profil) != 0 :
		for i in range(len(profil)):
			sum_stars += profil[i]['stargazers_count']

		mean_star = sum_stars/len(profil)

	return mean_star 

def add_mean_star(data,key):

	data["mean_star"] = np.nan

	for i in data[key]:
		mean = mean_star(i)
		data.loc[data[key]==i,"mean_star"] = mean


add_mean_star(rank,'Pseudo')

rank_sort = rank.sort_values('mean_star',ascending=False)

print(rank_sort.head())