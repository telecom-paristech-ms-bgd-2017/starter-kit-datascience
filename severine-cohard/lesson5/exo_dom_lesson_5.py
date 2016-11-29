#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:49:58 2016

@author: severine
"""

"""Peut-on établir un lien entre la densité de médecins par spécialité  
et par territoire et la pratique du dépassement d'honoraires ?
"""

import numpy as np
import pandas as pd



hono_file = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'
excel_honoraire = pd.ExcelFile(hono_file)
data_generaliste = excel_honoraire.parse('Généralistes et MEP')
data_spe = excel_honoraire.parse('Spécialistes')

dens_file = 'Effectif_et_densite_par_departement_en_2014.xls'
excel_densite = pd.ExcelFile(dens_file)
data2_generaliste = excel_densite.parse('Généralistes et MEP')
data2_spe = excel_densite.parse('Spécialistes')


# nettoyage des colonnes
for i in range(5, 12):
    del data2_spe['Unnamed: ' + str(i)]

data_generaliste.rename(columns = {'Généralistes et compétences MEP':'Spécialité'}, inplace = True)
data_spe.rename(columns = {'Spécialistes':'Spécialité'}, inplace = True)
data2_generaliste.rename(columns = {'Généralistes et compétences MEP':'Spécialité'}, inplace = True)
data2_spe.rename(columns = {'Spécialistes':'Spécialité'}, inplace = True)

#creation des dataframes
densite = pd.concat([data2_spe, data2_generaliste])
honoraire = pd.concat([data_spe, data_generaliste])

densite.rename(columns = {'EFFECTIF':'EFFECTIFS'}, inplace = True)

#on garde un tableau donc on merge
data0 = pd.merge(densite,honoraire)


# on met le bon format et on gère les NA
data0['EFFECTIFS'] = data0['EFFECTIFS'].astype('float64')
data0['EFFECTIFS'] = data0['EFFECTIFS'].replace({0 : np.nan})
data0['TOTAL DES HONORAIRES (Euros)'] = data0['TOTAL DES HONORAIRES (Euros)'].replace({'nc' : np.nan})
data0['DEPASSEMENTS (Euros)'] = data0['DEPASSEMENTS (Euros)'].replace({'nc' : np.nan}) 

#calcul des honoraires totaux
data0['Honoraires totaux par médecin'] = data0['TOTAL DES HONORAIRES (Euros)']/data0['EFFECTIFS'].replace({0 : np.nan})

#calcul pourcentage depassement
data0['Pct dépassement'] = data0['DEPASSEMENTS (Euros)']/data0['TOTAL DES HONORAIRES (Euros)']

print(data0)
