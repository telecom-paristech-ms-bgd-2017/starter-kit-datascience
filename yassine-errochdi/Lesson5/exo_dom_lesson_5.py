
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#------------------------------------------------------------------------
# Peut-on établir un lien entre la densité de médecins par spécialité  et
# par territoire et la pratique du dépassement d'honoraires ?
# Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent
# le moins les dépassement d'honoraires ?
#------------------------------------------------------------------------
files_dir = os.environ['USERPROFILE']+'/PycharmProjects/DAMIR/fichiers'
#--------------------------------------------------------------
honoraires_file = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2015.xls'
#Avec none on récupère tous les onglets ( voir leur nom avec data.keys())
data = pd.read_excel(honoraires_file, sheetname=None)
df = data['Spécialistes']
#Supprimer les lignes nc
df = df.replace('nc', np.nan).dropna()
#Supprimer les totaux
df = df[df['DEPARTEMENT'].str.contains('- ')]
df = df[df['SPECIALISTES'].str.contains('- ')]
#Supprimer les lignes sans effectif
df = df[df['EFFECTIFS'] > 0]

def subCode(x):
    iDash = x.index('-')
    return x[0:iDash]

#Extraction du numéro de département pour jointure avec dénombrement population
df['NUM_DEP'] = df['DEPARTEMENT'].apply(subCode)

df['DEPASSEMENTS (euros)'] = df['DEPASSEMENTS (euros)'].astype('float')
df['HONORAIRES SANS DEPASSEMENT (euros)'] = df['HONORAIRES SANS DEPASSEMENT (euros)'].astype('float')
df['TAUX_DEPASSEMENT']= (df['DEPASSEMENTS (euros)']*100)/df['HONORAIRES SANS DEPASSEMENT (euros)']

#--------------------------------------------------------------

demo_file = files_dir+'/estim-pop-dep-sexe-aq-1975-2014.xls'
data = pd.read_excel(demo_file, sheetname=None)

demoDf= data['2013']
demoDf = demoDf.dropna()
colTab=['NUM_DEP','DEP']
def appendColName(pref,tab):
    i = 0
    while i < 95:
        tab.append(pref+'_'+str(i)+'_'+str(i+4))
        i = i+5
    tab.append(pref+'_'+str(i))

appendColName('TOT',colTab)
colTab.append('TOTAL')
appendColName('H',colTab)
colTab.append('H_TOTAL')
appendColName('F',colTab)
colTab.append('F_TOTAL')
demoDf.columns = colTab
demoDf.set_index('NUM_DEP')
#--------------------------------------------------------------
medDf = pd.merge(df,demoDf,how='inner',on='NUM_DEP')

medDf.to_csv(files_dir+'/med.csv')
medDf['MED_DENSITE']= (medDf['EFFECTIFS'] * 100000) / medDf['TOTAL']
grouped = medDf.groupby('SPECIALISTES')

specialites = sorted(grouped.groups.keys())

anest = grouped.get_group('02- Anesthésie-réanimation chirurgicale')

def regplot(spe):

    sns.set_context('notebook')
    sns.set_style('darkgrid')
    sns.set_palette('colorblind')
    sns.regplot(x='MED_DENSITE', y='TAUX_DEPASSEMENT', data=spe, ci=None, line_kws={'color': 'r', 'linewidth': 1.5})
    plt.tight_layout()
    plt.show()

def histo(spe,title):
    f = plt.figure(figsize=(15, 10))
    mySpe= spe.loc[:,['NUM_DEP','MED_DENSITE','TAUX_DEPASSEMENT']]
    ax=mySpe.plot(ax=f.gca(),x='NUM_DEP',y='MED_DENSITE',kind='bar',stacked=True)
    mySpe.plot(ax=f.gca(),x='NUM_DEP',y='TAUX_DEPASSEMENT',secondary_y=True, kind='bar',stacked=True, color=['r'])
    plt.title(title)
    plt.show()

for speciality in specialites:
    histo(grouped.get_group(speciality),speciality)