import requests
from bs4 import BeautifulSoup
import locale
import os
import sys
import unicodedata



#get the mark of items

def get_input(mark,k):
  url = 'http://www.cdiscount.com/search/10/{}.html#_his_'.format(mark)
  #url = 'http://www.cdiscount.com/search/10/{}.html?page='+str(k)+'#_his_'.format(mark)

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


def calcul_taux_global(brand, MAX_P):
  total_reduction = 0
  res = 0

  for ka in range(1, MAX_P+1):
    url2 = get_input(brand, ka)
    res = extractFromDOM(url2, brand)
    print(url2)
    total_reduction = total_reduction + res
  total_reduction_1 = total_reduction / MAX_P
  return (total_reduction_1)


def affichage_reduction_total(mark,result):
    print('TOTAL DES REDUCTION DE LA MARQUE ' + mark.upper() + ' est = ' + str(result))
    return

def meilleur_reduct(mark1,mark2,res_mark1,res_mark2):
    if (res_mark1 < res_mark2):
        print('\nla marque '+ str(mark2) + ' à plus de reduction que la marque '+ str(mark1) + '!!!')
    else:
        print('\nla marque ' + str(mark1) + ' a plus de reduction que la marque ' + str(mark2) + '!!!')
    return

######################### execution du main() ###################################
if __name__ == '__main__':


    mark = 'acer'
    MAX_PAGE = 1

    #url = get_input('acer',MAX_PAGE)
    total_reduction_acer = calcul_taux_global('acer', MAX_PAGE)
    affichage_reduction_total('acer', total_reduction_acer)
    #url = get_input('dell', MAX_PAGE)
    total_reduction_dell = calcul_taux_global('dell', MAX_PAGE)
    affichage_reduction_total('dell', total_reduction_dell)
    meilleur_reduct('acer', 'dell', total_reduction_acer, total_reduction_dell)


