# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 16:41:10 2016

@author: Franck
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import pandas as pd


def crunch_site(marque):

	compteur = 0
	compteur_disc = 0
	somme_prix_public = 0
	somme_prix = 0

	for page in range(1, 5):#on ne prend que les 5 premières pages, les plus fiables du point de vue de la recherche marque + ordinateur
	    adresse_page_dell = u'http://www.cdiscount.com/search/10/dell+portable.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=14&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=dell%2Bportable&page=' + \
	        str(page) + '&_his_'
	    adresse_page_hp = u'http://www.cdiscount.com/search/10/hp+portable.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=hp%2Bportable&page=' + \
	        str(page) + '&_his_'
	    if (marque=='hp'):
	    	adresse_page = adresse_page_hp
	    elif (marque=='dell'):
	    	adresse_page = adresse_page_dell
	    else:
	    	print('Problème: la marque doit etre dell ou hp')

	    whole_page = requests.get(adresse_page)
	    soup_page = BeautifulSoup(whole_page.text, 'html.parser')
	    liste_produits = soup_page.find_all(class_="prdtPrice")

	    for produit in liste_produits:
	        compteur = compteur + 1
	        if produit.previousSibling.text != "":  # Test pour savoir si un prix publiuc est renseigné
	            compteur_disc += 1
	            prix_pub = float(
	                str(produit.previousSibling.text).replace(",", "."))
	            prix = float(str(produit.text).replace("€", "."))
	            somme_prix_public += prix_pub
	            somme_prix += prix
	            # nom_produit = produit.parent.parent.previousSibling.text
	            # print(nom_produit)
	return [compteur,compteur_disc,somme_prix,somme_prix_public]

crunch_hp = crunch_site('hp')
print("Pour HP: %s produits observés" % crunch_hp[0] + ", %s pris en compte" % crunch_hp[1] + " / Discount moyen(pourcentage): %4.1f" %
	      (100 * (1 - crunch_hp[2] / crunch_hp[3])) + " / Prix public moyen: %4.0f" % (crunch_hp[3] / crunch_hp[1]))
crunch_dell= crunch_site('dell')
print("Pour Dell: %s produits observés" % crunch_dell[0] + ", %s pris en compte" % crunch_dell[1] + " / Discount moyen(pourcentage): %4.1f" %
	      (100 * (1 - crunch_dell[2] / crunch_dell[3])) + " / Prix public moyen: %4.0f" % (crunch_dell[3] / crunch_dell[1]))

print("Discouts (en pourcent) HP vs Dell: %4.1f vs %4.1f" %((100 * (1 - crunch_hp[2] / crunch_hp[3])),(100 * (1 - crunch_dell[2] / crunch_dell[3]))) )

