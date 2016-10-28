#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

"""Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires ?
Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les dépassement d'honoraires ?
Est ce que la densité de certains médecins / praticiens est corrélé à la densité de population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

C'est un sujet assez ouvert pris du Hackathon "données de santé" de Etalab.
Il y a un github qui contient une partie des données dont vous aurez besoin.
Vous pouvez compléter ça avec de l'INSEE et des données sur la démographie des médecins."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

honoraires_file = './sante/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'
hon_xl = pd.ExcelFile(honoraires_file)
df_hon_gen = hon_xl.parse('Généralistes et MEP')
df_hon_spe = hon_xl.parse('Spécialistes')

densite_file = './sante/Effectif_et_densite_par_departement_en_2014.xls'
dens_xl = pd.ExcelFile(densite_file)
df_dens_gen = dens_xl.parse('Généralistes et MEP')
df_dens_spe = dens_xl.parse('Spécialistes')

income_file = './sante/base-cc-filosofi-13.xls'
income_xl = pd.ExcelFile(income_file)
df_income = income_xl.parse('DEP', skiprows=3, header=2)

# Cleaning empty columns
for i in range(5, 12):
    del df_dens_spe['Unnamed: ' + str(i)]

df_hon_gen.rename(columns = {'Généralistes et compétences MEP':'Spécialité'}, inplace = True)
df_hon_spe.rename(columns = {'Spécialistes':'Spécialité'}, inplace = True)
df_dens_gen.rename(columns = {'Généralistes et compétences MEP':'Spécialité'}, inplace = True)
df_dens_spe.rename(columns = {'Spécialistes':'Spécialité'}, inplace = True)

df_dens = pd.concat([df_dens_spe, df_dens_gen])
df_hon = pd.concat([df_hon_spe, df_hon_gen])

df_dens.rename(columns = {'EFFECTIF':'EFFECTIFS'}, inplace = True)

df = pd.merge(df_dens,df_hon)

# df['Revenu median pop.'] = 

df['EFFECTIFS'] = df['EFFECTIFS'].astype('float64')
df['EFFECTIFS'] = df['EFFECTIFS'].replace({0 : np.nan})
df['TOTAL DES HONORAIRES (Euros)'] = df['TOTAL DES HONORAIRES (Euros)'].replace({'nc' : np.nan})
df['DEPASSEMENTS (Euros)'] = df['DEPASSEMENTS (Euros)'].replace({'nc' : np.nan}) 

df['Honoraires totaux par médecin'] = df['TOTAL DES HONORAIRES (Euros)']/df['EFFECTIFS'].replace({0 : np.nan})

df['Pct dépassement'] = df['DEPASSEMENTS (Euros)']/df['TOTAL DES HONORAIRES (Euros)']

# Avg France métropolitaine
#df.loc[df['DEPARTEMENT'] == 'TOTAL FRANCE METROPOLITAINE'][df['Spécialité'] == 'TOTAL MEDECINS']

dfdrop = df.drop(df[np.isnan(df['Pct dépassement'])].index)

fig1 = plt.figure()
ax = plt.subplot()
#ax.scatter(dfdrop['DENSITE /100 000 hab.'], dfdrop['Pct dépassement par médecin'])

dfdrop_non_gene_dens = dfdrop['DENSITE /100 000 hab.'][~(dfdrop['Spécialité'] == '01- Médecine générale')]
dfdrop_non_gene_dep = dfdrop['Pct dépassement'][~(dfdrop['Spécialité'] == '01- Médecine générale')]
ax.scatter(dfdrop_non_gene_dens, dfdrop_non_gene_dep, color='navy', label='Non-généralistes')

dfdrop_gene = dfdrop['DENSITE /100 000 hab.'][dfdrop['Spécialité'] == '01- Médecine générale']
dfdrop_gene_dep = dfdrop['Pct dépassement'][dfdrop['Spécialité'] == '01- Médecine générale']
ax.scatter(dfdrop_gene, dfdrop_gene_dep, color='royalblue', label='Généralistes')

ax.set_xlabel('DENSITE /100 000 hab.')
ax.set_ylabel('\%\ dépassement honoraires')

#sns.lmplot(dfdrop['DENSITE /100 000 hab.'], dfdrop['Pct dépassement par médecin'], data=df, fit_reg=False, hue="z")
plt.legend()
plt.show()