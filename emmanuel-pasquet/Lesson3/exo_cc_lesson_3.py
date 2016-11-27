import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

urlAcer = 'http://www.cdiscount.com/search/10/acer.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&FacetForm.SelectedFacets.Index=15&FacetForm.SelectedFacets.Index=16&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=acer&&_his_'
urlNovo = 'http://www.cdiscount.com/search/10/lenovo.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&FacetForm.SelectedFacets.Index=15&FacetForm.SelectedFacets.Index=16&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=lenovo&&_his_'

soupAcer = requests.get(urlAcer)
soupNovo = requests.get(urlNovo)

soupAcer2 = BeautifulSoup(soupAcer.text, "html.parser")
soupNovo2 = BeautifulSoup(soupNovo.text, "html.parser")

marques = {0:'Acer', 1:'LeNovo'}
listProducts = []
listProducts.append(soupAcer2.find_all(class_="prdtBloc"))
listProducts.append(soupNovo2.find_all(class_="prdtBloc"))

# Printer les éléments textuels des listes permet:
# -- de visualiser les regex qu'il y aura à appliquer
# -- ainsi que d'identifier d'un coup d'oeil le contenu des résultats plutôt que d'aller dans le code source de la page
for i in range(2):
    print marques[i], "a ", len(listProducts[i]), "produits en ligne en page 1 :\n"
    for el in listProducts[i]:
        print el.text
        
# On itère sur les listes puis sur leurs éléments pour ramener chaque montant de remise
# et chaque montant de prix original afin de calculer le pourcentage de réduction. 
# On met également en place de 2 compteurs pour comparer le nombre de produits avec réduction de part et d'autre
listReducs = []
counterReducs = []
counter = 0
for i in range(2):
    liste = []
    print marques[i], ':'
    for el in range(len(listProducts[i])):
        try:
            a = float(re.search('([0-9]+)', listProducts[i][el].find(class_="ecoBlk").text).group(0))
            b = float(re.search('([0-9]+)', listProducts[i][el].find(class_="prdtPrSt").text).group(0))
            print 'a', a
            print 'b', b

            if b > 200.0:
                liste.append(a / b)
                print 'q = ', a / b
                counter += 1
        except:
            continue
    print i, ':', counter
    listReducs.append(liste)
    counterReducs.append(counter)
    counter = 0

# Comparatif des pourcentages de réductions en fonction de la marque. \n
# Comparatif du nombre de produits avec réduction trouvés dans la première page

for i in range(2):
    print "La reduction moyenne pour les PC portables de la marque", marques[i], "est :", np.mean(listReducs[i])
    print marques[i], " a ", counterReducs[i], "produits soldes"
