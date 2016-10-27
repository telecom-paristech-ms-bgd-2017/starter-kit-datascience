import requests
from bs4 import BeautifulSoup
import locale
import os
import sys
import unicodedata



#get the mark of items

def get_input(mark,k):
  k = str(k)
  url ='http://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-'+mark+ '.html?page='+k+'#_his_'

  return url


def extractFromDOM(url,mark):
  total_reduction = 0
  model_name = []
  old_price = []
  new_price = []
  reduction = []

  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  model_name = soup.find_all(class_="prdtBTit") #recuperation de l'info "nom du produit

  for i in range(len(model_name)):

    old = soup.find_all(class_="prdtPInfoTC")[i].get_text().replace(',','.')#recupération ancien prix si produit soldé
    new = soup.find_all(class_="prdtPrice")[i].get_text().replace('€','.')#recupération nouveau prix si produit soldé
    old = str(old)
    new = str(new)
    if (old != '') : #test si le produit est soldé ou non
       red = (round((float(old) - float(new))*100 / float(old),2)) #calcul du taux de reduction du produit elementaire
       old_price.append(old) #ajout dans la liste de type Array
       reduction.append(red) #ajout dans la liste de type Array
       new_price.append(new) #ajout dans la liste de type Array
       total_reduction = round(sum(reduction)/len(reduction),2) #calcul de la reduction moyenne de la page

  return (total_reduction)



######################### execution du main() ###################################

MAX_PAGE = 2
total_reduction = 0
mark = 'acer'
for k in range(1,MAX_PAGE):
    url2= get_input(mark,k)
    res = extractFromDOM(url2, mark)
    print('total_reduction page ',k,' = ',res)
    total_reduction_acer = (total_reduction + res)/k
    print('TOTAL DES REDUCTION DE LA MARQUE', mark, ' est = ', total_reduction_acer)

mark = 'dell'

for k in range(1,MAX_PAGE):
    url2= get_input(mark,k)
    res = extractFromDOM(url2, mark)
    print('total_reduction page ',k,' = ',res)
    total_reduction_dell = (total_reduction + res)/k
    print('TOTAL DES REDUCTION DE LA MARQUE', mark, ' est = ', total_reduction_dell)

if(total_reduction_dell<total_reduction_acer):
  print( "\nla marque Acer à plus de reduction que la marque Dell")
else :
  print("\nla marque Dell à plus de reduction que la marque Acer")

