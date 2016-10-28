# Zoé issue du bon coin
# Ile de france Paca Aquitaine
# Version Année Km prix Téléphone vendue par pro ou particulier

from lxml import html
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def region_car_url(region):

	url = "https://www.leboncoin.fr/voitures/offres/" + \
	    region + "/?th=1&parrot=0&brd=Renault&mdl=Zoe"
	text_lb = requests.get(url)
	soup = BeautifulSoup(text_lb.text,  'html.parser')
	# On identifie la dernieère page
	last_page = list(
	    map(lambda x: x['href'], soup.find_all(class_='element page static')))

	if len(last_page) != 0:
		idx_last_page = last_page[0].index("=")
		nb_last_page = int(last_page[0][idx_last_page + 1])
	else:
		nb_last_page = 1

	list_url_zoe = list()
	for i in range(1, nb_last_page + 1):
		url_i = "https://www.leboncoin.fr/voitures/offres/" + \
		    region + "/?th=1&parrot=" + str(i) + "&brd=Renault&mdl=Zoe"
		text_lb_i = requests.get(url_i)
		soup = BeautifulSoup(text_lb_i.text,  'html.parser')
		ma_liste_url = map(lambda x: x['href'], soup.find_all(
		    class_='list_item clearfix trackable'))
		list_url_zoe.extend(ma_liste_url)

	return list_url_zoe


def extraction_information(url):
	# Accés à l'url de chaque voiture
    text_page = requests.get("https:" + url)
    soup_page = BeautifulSoup(text_page.text, 'html.parser')
    title = soup_page.find(
        class_="no-border").text.replace("\n", "").replace("\t", "")
    clear_title = [i.lower() for i in title.split(" ") if i != " "]
    # Modèle de la voiture issue de la voiture
    liste_name_modele = ['life', 'intens', 'zen']
    modele = [i for i in clear_title if i in liste_name_modele]

    type_car = ""
    # définition du type de voiture
    for idx, i in enumerate(clear_title):
    	if i == 'charge':
    		if clear_title[idx + 2] == "type":
    			type_car = clear_title[idx] + " " + clear_title[idx + 1] + " " + clear_title[idx + 2] \
    						+ " " + clear_title[idx + 3]
    		else:
    			type_car = clear_title[idx] + " " + clear_title[idx + 1]

    		break

    	elif i == 'type':
    		type_car = clear_title[idx] + " " + clear_title[idx + 1]
    		break

    # pour ne pas renvoyer une liste
    modele = ''.join(modele)

    # Le prix, l'année et la distance parcouru
    price = soup_page.find_all(class_='value')[0].text.replace(
        "\xa0", "").replace("\n", "").replace(" ", "").replace("€","")
    year = soup_page.find_all(class_='value')[4].text.replace(
        "\xa0", "").replace("\n", "").replace(" ", "")
    distance = soup_page.find_all(class_='value')[5].text.replace(
        "\xa0", "").replace("\n", "").replace(" ", "").replace("KM","")

    # Le vendeur est il un professionnel
    pro = soup_page.find_all(class_='ispro')
    if len(pro) == 0:
        ispro = 'Particulier'
    else:
        ispro = soup_page.find_all(class_='ispro')[0].text.split(" ")[0]

    # Obtenir le numéro de téléphone
    idx_description = len(soup_page.find_all(class_='value'))
    description = soup_page.find_all(class_='value')[idx_description - 1].text
    pattern_regex = ("(0|\\+33|0033)[1-9]([\S  \s -,.][0-9]{1,2}){4}")
    find_patern = re.compile(pattern_regex).search(description.strip())

    if find_patern is None:
        mobile_number = 'None'
    else:
        mobile_number = find_patern.group()

    # On retourne l'information sous forme de dictionnaire
    value_return = {'Modele': modele, 'type': type_car, 'Année': year, 'Km': distance, 'Vendeur': ispro,
    	'Prix €': price, 'Numéro': mobile_number}

    return value_return


# Recherche de la cote sur la centrale pour ma_table

def transform_data(ma_table) :
	for i in range(ma_table.shape[0]) :

		if ma_table.loc[i,"type"]!="" :

			type_c = ma_table.loc[i,"type"].split(" ")
			type_url = "+".join(type_c)
			url = "http://www.lacentrale.fr/cote-auto-renault-zoe-"+ ma_table.loc[i,"Modele"] + "+" \
						+type_url+"-"+ ma_table.loc[i,"Année"] +".html"
		else :
			url = "http://www.lacentrale.fr/cote-auto-renault-zoe-"+ ma_table.loc[i,"Modele"]  \
						+"-"+ ma_table.loc[i,"Année"] +".html"

		text_lc = requests.get(url)
		soup_lc = BeautifulSoup(text_lc.text,  'html.parser')

 
		price_init = soup_lc.find(class_="f24 bGrey9L txtRed pL15 mL15")

		if 	price_init is not None:
			price_lc = soup_lc.find(class_="f24 bGrey9L txtRed pL15 mL15").text.replace("\n","") \
					.replace(" ","").replace("€","")
		else : 
			price_lc = np.nan



		ma_table.loc[i,"Price Central €"] = price_lc	

	return ma_table 




def fullfil():
	# crée la table de remplissage
	columns_name = ['Modele', 'type', 'Année', 'Km', 'Vendeur', 'Prix €', 'Numéro']
	data_zoe = pd.DataFrame(columns=columns_name)

	# On remplit pour chaque region
	for region in ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']:

		liste_car = region_car_url(region)

		# On remplit notre table pour cette region
		for v in liste_car:
			it_dict = extraction_information(v)
			data_zoe = data_zoe.append(it_dict, ignore_index=True)

	data_zoe_2 = transform_data(data_zoe)

	#data["Least Price"] = data_zoe_2["Prix"] - data_zoe_2["Price Central"]

	# Cleaning table
	data_zoe_2["Prix €"] = data_zoe_2["Prix €"].apply(float)
	data_zoe_2["Km"] = data_zoe_2["Km"].apply(float)
	data_zoe_2["Price Central €"] = data_zoe_2["Price Central €"].apply(float)

	data_zoe_2["Value Argus"] = data_zoe_2["Prix €"] - data_zoe_2["Price Central €"]

	data_zoe_2["Numéro"] = data_zoe_2["Numéro"].apply(lambda x : x.replace(".","").replace("/","").replace(" ",""))
	data_zoe_2["Numéro"] = data_zoe_2["Numéro"].apply(lambda x : None if len(x)!=10  else x) 


	return data_zoe_2

ma_table = fullfil()
path = "/home/brehelin/Documents/Kit Data Science/starter-kit-datascience/alexandre-brehelin/Lesson 4/"
ma_table.to_csv(path + "export_le_boncoin.csv")


