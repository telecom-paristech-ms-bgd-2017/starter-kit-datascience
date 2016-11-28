import requests
from bs4 import BeautifulSoup

#get the year of needed data

def get_indate(indate):

  indate=str(indate)
  url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
  return url + indate

#def extractIntFromDOM(soup, classname):


def results(res,x,y):

  params ={}

  params['']=res
  params[" Total Euros par habitant "] = x
  params[" Moyenne de la strate "]=y

  for key in params:
    print (key,params[key], "\n")

  return(params.items)



def extractFromDOM(url, classname, position):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  res_type_fiscale = soup.find_all(class_="bleu")[position].find(class_=classname).text.replace(u'\xa0','')
  res_1_euro_par_habitant = soup.find_all(class_="bleu")[position].find_all(class_="montantpetit G")[1].text.replace(u'\xa0', '')
  res_1_moyenne_de_la_state = soup.find_all(class_="bleu")[position].find_all(class_="montantpetit G")[2].text.replace(u'\xa0',
                                                                                                              '')
  return (res_type_fiscale,res_1_euro_par_habitant,res_1_moyenne_de_la_state)

######################### execution du main() ###################################

date = 2010

url= get_indate(date)

dictA = extractFromDOM(url, "libellepetit G", 3)
sortie_A = results(dictA[0],dictA[1],dictA[2])

dictB = extractFromDOM(url, "libellepetit G", 7)
sortie_B = results(dictB[0],dictB[1],dictB[2])

dictC = extractFromDOM(url, "libellepetit G", 15)
sortie_C = results(dictC[0],dictC[1],dictC[2])

dictD = extractFromDOM(url, "libellepetit G", 20)
sortie_D = results(dictD[0],dictD[1],dictD[2])