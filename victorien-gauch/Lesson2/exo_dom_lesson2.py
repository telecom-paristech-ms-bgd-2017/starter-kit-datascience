import requests
from bs4 import BeautifulSoup
import sys

def getData(year):
  
  url = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
  soup = BeautifulSoup(url.text,'html.parser')
  tab = saveData(soup)
  return tab

def toString(year, dico):
  
  print('==========')
  print('Année '+str(year)+' :')
  print()
  print('TOTAL DES PRODUITS DE FONCTIONNEMENT : '+dico['euroA']+ ' (Euros par habitant)')
  print('TOTAL DES PRODUITS DE FONCTIONNEMENT : '+dico['strateA']+ ' (Moyenne de la strate)')
  print()
  print('TOTAL DES CHARGES DE FONCTIONNEMENT: '+dico['euroB']+ ' (Euros par habitant)')
  print('TOTAL DES CHARGES DE FONCTIONNEMENT : '+dico['strateB']+ ' (Moyenne de la strate)')
  print()
  print('TOTAL DES RESSOURCES D\'INVESTISSEMENT : '+dico['euroC']+ ' (Euros par habitant)')
  print('TOTAL DES RESSOURCES D\'INVESTISSEMENT : '+dico['strateC']+ ' (Moyenne de la strate)')
  print()
  print('TOTAL DES EMPLOIS D\'INVESTISSEMENT : '+dico['euroD']+ ' (Euros par habitant)')
  print('TOTAL DES EMPLOIS D\'INVESTISSEMENT : '+dico['strateD']+ ' (Moyenne de la strate)')
  print('==========')

def getLine(soup,pos):
  return soup.find_all(class_ = "montantpetit G")[pos].text.replace('\xa0','')

def saveData(soup):
  dico = {}

  dico['euroA'] = getLine(soup,1)
  dico['strateA'] = getLine(soup,2)
  dico['euroB'] = getLine(soup,4)
  dico['strateB'] = getLine(soup,5)
  dico['euroC'] = getLine(soup,10)
  dico['strateC'] = getLine(soup,11)
  dico['euroD'] = getLine(soup,13)
  dico['strateD'] = getLine(soup,14)

  return dico


def main(argv):
  years = [2010, 2011, 2012, 2013]

  for y in years:
    data = getData(y)
    toString(y,data)


if __name__ == '__main__':
    main(sys.argv)

  
