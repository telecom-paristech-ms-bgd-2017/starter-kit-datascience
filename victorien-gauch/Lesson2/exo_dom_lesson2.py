import requests
from bs4 import BeautifulSoup



for page in range(2010,2014):

  all_city_count = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(page))
  soup_city = BeautifulSoup(all_city_count.text,'html.parser')

  euros = []
  strate = []
  res_str = soup_city.find_all(class_='bleu')

  for row in res_str:
    cols = row.find_all(class_='montantpetit G')
    cols = [ele.text.strip() for ele in cols]
    
    if len(cols) == 0:
      continue
    else:
      euros.append(cols[1])
      strate.append(cols[2])

  dico_euros = {'A': euros[0] , 'B': euros[1],'C': euros[3], 'D' : euros[4]}
  dico_strate =  {'A': strate[0] , 'B': strate[1],'C': strate[3], 'D' : strate[4]}
  
  print('==========')
  print('Année '+str(page)+' :')
  print()
  print('TOTAL DES PRODUITS DE FONCTIONNEMENT : '+dico_euros['A']+ ' (Euros par habitant)')
  print('TOTAL DES PRODUITS DE FONCTIONNEMENT : '+dico_strate['A']+ ' (Moyenne de la strate)')
  print()
  print('TOTAL DES CHARGES DE FONCTIONNEMENT: '+dico_euros['B']+ ' (Euros par habitant)')
  print('TOTAL DES CHARGES DE FONCTIONNEMENT : '+dico_strate['B']+ ' (Moyenne de la strate)')
  print()
  print('TOTAL DES RESSOURCES D\'INVESTISSEMENT : '+dico_euros['C']+ ' (Euros par habitant)')
  print('TOTAL DES RESSOURCES D\'INVESTISSEMENT : '+dico_strate['C']+ ' (Moyenne de la strate)')
  print()
  print('TOTAL DES EMPLOIS D\'INVESTISSEMENT : '+dico_euros['D']+ ' (Euros par habitant)')
  print('TOTAL DES EMPLOIS D\'INVESTISSEMENT : '+dico_strate['D']+ ' (Moyenne de la strate)')
  print('==========')




  
