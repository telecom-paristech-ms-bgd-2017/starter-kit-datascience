# -*- coding: utf-8 -*-

import requests
import bs4
import os
import pandas as pd
import json
import numpy as np
from unidecode import unidecode
import re
import pdb

regexphone = '((0|\\+33|0033)[1-9][0-9]{8})|((0|\\+33|0033)[1-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})|((0|\\+33|0033)[1-9].[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2})'
regexversion = 'ZOE(.)*(INTENS|ZEN|LIFE)'
regextype2 = 'TYPE(\s)?2'
base_url = "https://www.leboncoin.fr/annonces/offres/"
param_zoe = {}
param_zoe["q"] = "renault zoe"
maxpage = 20

regions = ["ile_de_france","provence_alpes_cote_d_azur", "aquitaine"]

def analyser_regions(regions):
	tabs = pd.DataFrame()
	for region in regions:
		tabs = pd.concat([tabs, analyser_region(region)])
	tabs.to_csv("RenaultZoe.csv", index = False)

def analyser_region(region):
	tab = pd.DataFrame()
	for page in range(1, maxpage):
		try:
			res = analyser_page(page, region)
			tab = pd.concat([tab, pd.DataFrame(res)])
		except AttributeError:
			continue
	tab.columns = (["Region", "Version", "Type 2", "Annee", "Kilometrage", "Prix", "Telephone", "Type", "Lien", "Cote", "Prix supérieur à la cote ?"])
	return tab

def analyser_page(page, region):
	param_zoe["o"] = page
	r = requests.get(base_url+region+"/", params = param_zoe)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')

	annonces = soup.find("section", class_="tabsContent").find_all("a")
	res = []
	for i in range(0, len(annonces)):

		# Récupération du lien de l'annonce et du flag professionnel/particulier
		lien_annonce = annonces[i]["href"][2:]
		info_annonce = annonces[i]["data-info"]
		if(info_annonce.split(",")[6][16:-2] == "pro"): propart = "professionnel"
		else: propart = "particulier"

	 	# Seules les annonces de voitures doivent être parcourures
	 	if(annonces[i].find("p", class_="item_supp").text.split("\n")[3].strip() == "Voitures"):
			r2 = requests.get("https://"+lien_annonce)
			soup2 = bs4.BeautifulSoup(r2.content, 'html.parser')

			# Récupération de la marque
			item_marque = str(find_property(soup2, "Marque"))

			if(item_marque != "Renault"): continue

			# Récupération du prix
			item_price = float(soup2.find("h2", class_="item_price")["content"])

			# Récupération du kilométrage
			item_kilometrage = int(find_property(soup2, "Kilométrage").replace("KM","").replace(" ",""))

			# Récupération de l'année
			item_annee = int(find_property(soup2, "Année-modèle"))

			# Récupération de la description et dun titre
			item_description = find_description(soup2)
			item_title = unidecode(soup2.find("section", class_ = "adview block-white flex-item-first").find("h1").text.strip().replace(u'\xe9',"e"))

			# Récupération du modèle
			try:
				# On teste d'abord le titre
				item_modele_split_fromtitle = re.search(regexversion,str.upper(item_title)).group().split(" ")
				item_modele = "ZOE "+item_modele_split_fromtitle[len(item_modele_split_fromtitle) - 1].replace("ZOE","")
			except AttributeError:
				item_modele = ""
				try:
					item_modele_split = re.search(regexversion,str.upper(item_description)).group().split(" ")
					item_modele = "ZOE "+item_modele_split[len(item_modele_split) - 1].replace("ZOE","")
				except AttributeError:
					item_modele = ""

			# Récupération de type 2 ou non
			try:
				# On teste d'abord le titre
				item_type2_fromtitle = re.search(regextype2,str.upper(item_title)).group().split(" ")
				flag_type2 = True
			except AttributeError:
				try:
					item_type2 = re.search(regextype2,str.upper(item_description)).group().split(" ")
					flag_type2 = True
				except AttributeError:
					flag_type2 = False

			# 2016 : pas de cote zen, intens, life charge rapide sans type 2
			if(item_annee == 2016): flag_type2 = True

			# Récupération du numéro de téléphone
			try:
				ip = re.search(regexphone,item_description).group().replace(" ","").replace(".","")
				item_phone = ip[:-8]+"."+ip[-8:-6]+"."+ip[-6:-4]+"."+ip[-4:-2]+"."+ip[-2:] # Mise sous la forme 01.23.45.67.89 (pour garder le 0 initial)
			except AttributeError:
				item_phone = ""

			print item_modele, item_annee, item_kilometrage, item_price, item_phone, propart, lien_annonce

			if(item_modele != ""):
				cote = find_cote(item_modele.split(" ")[1], flag_type2, item_annee)
			else:
				cote = -9999

			res.append([region, item_modele, flag_type2, item_annee, item_kilometrage, item_price, item_phone, propart, lien_annonce, cote, item_price > cote])
	 	# else:
	 		# print "Il ne s'agit pas d'une voiture"
	return res

def find_property(soup2, property):
	 div = soup2.find_all("div")
	 property_encoded = unidecode(property.decode("utf8"))
	 for i in range(0, len(div)):
	 	try:
	 		if unidecode(div[i].find("span", class_ = "property").text) == property_encoded:
	 			return div[i].find("span", class_ = "value").text
	 	except AttributeError, IndexError:
	 		continue

def find_description(soup2):
	 div = soup2.find_all("div")
	 description = ""
	 for i in range(0, len(div)):
	 	try:
	 		description = div[i].find("p", itemprop = "description").text.replace(u'\xe9',"e")
	 	except AttributeError:
	 		continue
	 return description.encode("utf8")

def find_cote(modele,type2,annee):
	if(type2):
		type2str = "+type+2"
	else:
		type2str = ""
	r = requests.get("http://www.lacentrale.fr/cote-auto-renault-zoe-"+str.lower(modele)+"+charge+rapide"+type2str+"-"+str(annee)+".html")
	soup = bs4.BeautifulSoup(r.content, 'html.parser')
	try:
		cote = int(unidecode(soup.find("strong",class_="f24").text).replace("EUR","").replace(" ",""))
	except AttributeError:
		cote = 0
	return cote


