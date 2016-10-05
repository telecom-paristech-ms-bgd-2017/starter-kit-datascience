from lxml import html 
import requests 
from bs4 import BeautifulSoup



def parser(annee):
	annee = str(annee)
	url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+annee
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser') 
	return soup

def question(letter):
	if letter == ' A':
		print("Total des produits de fonctionnement")
	elif letter == ' B':
		print("Total des charges de fonctionnement")
	elif letter == ' C':
		print("Total des resources d'investissement")
	elif letter == ' D':
		print("Total des emplois d'investissement")


def research(letter):
	letter = ' ' + letter
	for i in (10,14,22,27):
		lis = []
		res = []
		indice = str(i)
		adresse = "tr:nth-of-type("+indice+")"
		for value in soup.select(adresse)[0].text.replace("\xa0",'').split('\n') :
			lis.append(value)
		if lis[0] == '':
			if lis[4].split("=")[1] == letter:
				res.append(lis[2])
				res.append(lis[3])


		else :
			if lis[3].split("=")[1] == letter:
				res.append(lis[2])
				res.append(lis[3])

		if len(res)>0:
			print("=======================")
			print("pour le segment " + letter +" :")
			question(letter)
			print("la valeur euro par habitant est :")
			print (res[0])
			print ("la valeur moyenne par strate :")
			print (res[1])
			print ("=======================")


for i in (2010,2011,2012,2013):
	print("=====================")
	print("===="+ str(i) +"====")
	print("=====================")
	soup=parser(2013)
	research('A')
	research('B')
	research('C')
	research('D')
