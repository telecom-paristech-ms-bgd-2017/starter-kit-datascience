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
import time
import matplotlib.pyplot as plt


###### EXERCICE 1 : corrélation entre la densité de médecins par territoire et les dépassements d'honoraires

# Lecture des infos sur les médecins
rpps_2015_medecins = pd.read_csv("rpps-2015-medecins.csv", sep=";", skiprows = 4)
rpps_2015_medecins = rpps_2015_medecins.dropna()
rpps_2015_medecins.index = map(lambda x: x.split("-")[0].strip(), rpps_2015_medecins["SPECIALITE"])
# Gestion des 'é' dans les noms des spécialités
rpps_2015_medecins.columns = rpps_2015_medecins.columns.map(lambda x: x.replace('\xe9','e'))


# Transformation des données dans un cube
rpps_2015_cube = pd.DataFrame()
for column_name in rpps_2015_medecins.columns[1:]:
	for dep in range(0, len(rpps_2015_medecins[column_name])):
		rpps_2015_cube = pd.concat([rpps_2015_cube,
									pd.DataFrame(np.reshape(np.transpose([rpps_2015_medecins.ix[dep,0], column_name, rpps_2015_medecins.ix[dep,column_name]]), (1,3)))])

rpps_2015_cube["Departement"] = rpps_2015_cube[0].map(lambda x: x.split("-")[0].strip())
rpps_2015_cube.columns = ["Departement long", "Specialite", "Densite", "Departement"]
rpps_2015_cube["Densite"] = rpps_2015_cube["Densite"].astype(float)

# Correspondance entre colonne exe_spe et le label RPPS
correspondance_rpps_fichierR = pd.read_csv("CorrespondanceRPPS_fichierR.csv", sep=";")
correspondance_rpps_fichierR["LabelRPPS"] = correspondance_rpps_fichierR["LabelRPPS"].map(lambda x: x.replace('é','e'))

# Merge entre infos RPPS et label exe_spe du fichier R
rpps_2015_cube_merge = pd.merge(rpps_2015_cube, correspondance_rpps_fichierR, left_on = "Specialite", right_on = "LabelRPPS", how = "left")
# Quelles sont les lignes qui n'ont pas de correspondance ?
rpps_2015_cube_merge[rpps_2015_cube_merge["exe_spe"].isnull()].groupby("Specialite").count()
# "Biologie médicale", "Genetique medicale" et "Recherche medicale" n'ont pas de correspondance dans le fichier R
# Nécessaire également d'adapter l'épélation de Neurochirurgie, ORL et chirurgie cervico-faciale, Radiodiagnostic et imagerie médicale, Radiotherapie

# Quelles sont les lignes qui ont une correspondance "None" ?
rpps_2015_cube_merge[rpps_2015_cube_merge["exe_spe"] == "None"].groupby("Specialite").count()
# Ces lignes n'ont pas d'équivalent dans les référentiels des fichiers R :
# Hematologie => mettre 99
# Médecine du travail => je propose de mettre exe_spe = 1 comme les médecins généralistes
# Médecine interne => mettre 9
# Médecine nucléaire => mettre 99
# Oncologie => 99

# On peut construire une table donnant la densité par label exe_spe
rpps_2015_cube_merge["Densite"] = rpps_2015_cube_merge["Densite"].astype(float)
densite_exe_spe = rpps_2015_cube_merge.groupby(["Departement", "exe_spe"], as_index = False)[["Densite"]].sum()
densite_exe_spe["key"] = densite_exe_spe["Departement"].astype(str) + "_" + densite_exe_spe["exe_spe"].astype(str)

# Lecture des fichiers R

analyse_annee = pd.DataFrame()

for mois in range(1, 12):
	if mois < 10 : mois = "0"+str(mois)
	else: mois = str(mois)

	R2015mois = pd.read_csv("R2015/R2015"+mois+"_sanslib.csv", sep=";", decimal = ",", thousands = ".")

	# Département à partir de cpam
	def rajoutezero(s):
		if(s == "201"):
			return "2A"
		if(s == "202"):
			return "2B"
		if(s[:2] == "97"):
			return s 
		else:
			if(len(s[:-1]) == 1):
				return "0" + s[:-1]
			else:
				return s[:-1]

	R2015mois["Departement"] = R2015mois["cpam"].map(lambda x: rajoutezero(str(x)))
	R2015mois["exe_spe"] = R2015mois["exe_spe"].replace([19, 36], [18, 18]) # Voir commentaire ci-après

	# Somme de dep_mon et rec_mon par département et spécialité
	analyse = R2015mois.groupby(["Departement","exe_spe"], as_index = False)[["dep_mon", "rec_mon"]].sum()
	# analyse["Depassement"] = analyse["dep_mon"]/(analyse["dep_mon"] + analyse["rec_mon"])
	analyse["key"] = analyse["Departement"].astype(str) + "_" + analyse["exe_spe"].astype(str)
	analyse["mois"] = mois

	# pdb.set_trace()

	analyse_annee = pd.concat([analyse_annee, analyse])

# Faire le merge de ces deux tables
analyse_annee_merge = analyse_annee.merge(densite_exe_spe, left_on = "key", right_on = "key", how = 'left')[["Departement_x", "exe_spe_x", "dep_mon", "rec_mon", "Densite"]]
# Certaines des dépenses du fichier R2015 n'ont pas de correspondance dans le fichier démographique des médecins :
# Infirmier, Masseur kiné, Pédicure, Orthophoniste, Orthoptiste, Labo => pas dans RPPS
# Pour Stomato, Chirurgie dentaire et chirurgie dentaire spé : mapping 'Chirurgie maxillo-faciale et stomatologie' RPPS => exe_spe 18
# et recatégorisation de exe_spe 19 et 36 en 18
# De plus, rajout manuel du mapping exe_spe 38 pour RPPS "Biologie médicale"
analyse_annee_merge = analyse_annee_merge.dropna()

# Calculer la corrélation entre "depassement" et "densité"
analyse_annee_merge["Taux depassement"] = analyse_annee_merge["dep_mon"] / (analyse_annee_merge["dep_mon"] + analyse_annee_merge["rec_mon"])
print analyse_annee_merge[["Densite", "Taux depassement"]].corr()
def plot_spe(exe_spe):
	data = analyse_annee_merge[analyse_annee_merge["exe_spe_x"] == exe_spe]
	plt.figure()
	plt.plot(data["Densite"], data["Taux depassement"], "xr")
	plt.show()

def plot_dep(dep):
	data = analyse_annee_merge[analyse_annee_merge["Departement_x"] == dep]
	plt.figure()
	plt.plot(data["Densite"], data["Taux depassement"], "xr")
	plt.show()

# Quelle spécialité fait le plus de dépassement ?
dep_par_spe = analyse_annee_merge.groupby("exe_spe_x")[["dep_mon", "rec_mon"]].sum()
dep_par_spe["Taux depassement spe"] = dep_par_spe["dep_mon"] / (dep_par_spe["dep_mon"] + dep_par_spe["rec_mon"])

# Dans quel département y a-t-il le plus de dépassements ?
dep_par_dep = analyse_annee_merge.groupby("Departement_x")[["dep_mon", "rec_mon"]].sum()
dep_par_dep["Taux depassement dep"] = dep_par_dep["dep_mon"] / (dep_par_dep["dep_mon"] + dep_par_dep["rec_mon"])

# Il n'y a jamais de dépassement pour exe_spe = 99
R2015mois[R2015mois["exe_spe"] == 99]["dep_mon"].unique() # Uniquement 0.0

###### EXERCICE 2 : corrélation entre la densité de médecins par territoires et certaines caractéristiques de la population

# Récupération données INSEE recensement 2013
categories = ["0-4", "5-9", "10-14", "15-20", "20-24", "25-30", "30-34", "35-40", "40-44", "45-50", "50-54", "55-60", "60-64", "65-70", "70-74", "75-80", "80-84", "85-90", "90-94", "95-100", "100+"]

def get_dep_pop(dep):
	res = []
	tab_url = "http://www.insee.fr/fr/themes/tableau_local.asp?ref_id=POP1B&millesime=2013&niveau=1&typgeo=DEP&codgeo="+str(dep)
	r = requests.get(tab_url)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')
	a = soup.find_all("td", class_ = "tab-chiffre")
	for i in range(0, len(a)/3 - 1):
		res.append([dep, categories[i], int(a[3*i+2].text.replace(" ",""))])
	return res

pop = pd.DataFrame()
for dep in rpps_2015_cube["Departement"].unique():
	print(dep)
	pop = pd.concat([pop, pd.DataFrame(get_dep_pop(dep))])
# Mayotte (976) ne renvoie pas de données, mais c'est le dernier élément donc pop est complet

pop.columns = ["Departement", "Bande", "Population"]
pop_totale_dep = pop.groupby("Departement").sum()
pop["Proportion par dep"] = pop.apply(lambda x: x["Population"] / float(pop_totale_dep["Population"][x["Departement"]]), axis = 1)

pop_med = pd.merge(pop, rpps_2015_cube, left_on = "Departement", right_on = "Departement", how = "left")

# Corrélation entre "Pediatrie" et les enfants de moins de 15 ans ?
pop_jeune = pop[pop["Bande"].isin(["0-4", "5-9", "10-14"])].groupby("Departement").sum()
pop_jeune_med = pd.merge(pop_jeune, rpps_2015_cube[rpps_2015_cube["Specialite"] == "Pediatrie"], left_index = True, right_on = "Departement", how = "left")
print pop_jeune_med[["Proportion par dep", "Densite"]].corr()

# Corrélation entre "Geriatrie" et les personnes de plus de 70 ans ?
pop_vieux = pop[pop["Bande"].isin(["70-74", "75-79", "80-84", "85-89", "90-94", "95-99", "100+"])].groupby("Departement").sum()
pop_vieux_med = pd.merge(pop_vieux, rpps_2015_cube[rpps_2015_cube["Specialite"] == "Geriatrie"], left_index = True, right_on = "Departement", how = "left")
print pop_vieux_med[["Proportion par dep", "Densite"]].corr()



