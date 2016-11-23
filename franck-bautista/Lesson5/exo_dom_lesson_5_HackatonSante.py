
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn import linear_model
import statsmodels.api as sm
import requests
from bs4 import BeautifulSoup
import re
import json  # json.loads
from sklearn import preprocessing
# --------------------------------------ENONCE ---------------------------
# Peut-on établir un lien entre la densité de médecins par spécialité  et
# par territoire et la pratique du dépassement d'honoraires ? Est-ce  dans
# les territoires où la densité est la plus forte que les médecins
# pratiquent le moins les dépassement d'honoraires ?

# ----------------------------------- APPROCHE --------------------------
# 1) Récupération d'un fichier de remboursements élémentaires de la CPAM (1 mois pris en compte - 3.7 M de lignes)
# Consolidation des données pour en déduire des taux de dépassement par spécialité et par département
# 2) Récupération d'un fichier donnant la densité des praticiens par spécialité et par département
# 3) Récupération d'un fichier donnant des indicateurs de niveau de vie par département
# 4) Recodification des spécialités des deux premiers fichiers pour en permettre un croisement
# 5) Affichage et calcul des corrélations entre Taux de dépassement d'une
# spécialité sur un territoire donné par rapport à la densité des
# praticiens et le niveau de vie de la population sur ce territoire
# (granularité = département)


# Recodification spécialité fichier RPPS (densité médecin)
mapping_rpps = {
    'Ensemble des spécialités d\'exercice': 'Doublons',
    'Spécialistes': 'Doublons',
    'Anatomie et cytologie pathologiques': 'Divers',
    'Anesthésie-réanimation': 'Divers',
    'Biologie médicale': 'Divers',
    'Cardiologie et maladies vasculaires': 'Divers',
    'Chirurgie générale': 'Chirurgie',
    'Chirurgie maxillo-faciale et stomatologie': 'Chirurgie',
    'Chirurgie orthopédique et traumatologie': 'Chirurgie',
    'Chirurgie infantile': 'Chirurgie',
    'Chirurgie plastique reconstructrice et esthétique': 'Chirurgie',
    'Chirurgie thoracique et cardio-vasculaire': 'Chirurgie',
    'Chirurgie urologique': 'Chirurgie',
    'Chirurgie vasculaire': 'Chirurgie',
    'Chirurgie viscérale et digestive': 'Chirurgie',
    'Dermatologie et vénéréologie': 'Dermato',
    'Endocrinologie et métabolisme': 'Divers',
    'Génétique médicale': 'Divers',
    'Gériatrie': 'KO',
    'Gynécologie médicale': 'Gynecologie',
    'Gynécologie-obstétrique': 'Gynecologie',
    'Hématologie': 'Divers',
    'Gastro-entérologie et hépatologie': 'Divers',
    'Médecine du travail': 'Divers',
    'Médecine interne': 'Divers',
    'Médecine nucléaire': 'Divers',
    'Médecine physique et réadaptation': 'Divers',
    'Néphrologie': 'Divers',
    'Neurochirurgie': 'Divers',
    'Neurologie': 'Divers',
    'ORL et chirurgie cervico-faciale': 'ORL',
    'Oncologie option médicale': 'Divers',
    'Ophtalmologie': 'Ophtalmologie',
    'Pédiatrie': 'Pediatre',
    'Pneumologie': 'Pneumologie',
    'Psychiatrie': 'Psychiatrie',
    'Radiodiagnostic et imagerie médicale': 'Divers',
    'Radiothérapie': 'Divers',
    'Réanimation médicale': 'Divers',
    'Recherche médicale': 'Divers',
    'Rhumatologie': 'Rhumatologie',
    'Santé publique et médecine sociale': 'Divers',
    'Généralistes': 'Generale',
    'Médecine générale': 'Doublons'}

# Recodification spécialité fichier R (remboursements unitaires CPAM)
mapping_R = {
    '01-TOTAL Omnipraticiens': 'Generale',
    '02-TOTAL Anesthésie-réanimation chirurgicale': 'KO',
    '03-Pathologie cardio-vasculaire': 'KO',
    '04-TOTAL Chirurgie': 'Chirurgie',
    '05-Dermatologie et vénérologie': 'Dermato',
    '06-TOTAL Radiologie': 'KO',
    '07-TOTAL Gynécologie': 'Gynecologie',
    '08-Gastro-entérologie et hépatologie': 'KO',
    '09-TOTAL Médecine Interne': 'KO',
    '11-Oto-rhino laryngologie': 'ORL',
    '12-TOTAL Pédiatrie': 'Pediatre',
    '13-Pneumologie': 'Pneumologie',
    '14-Rhumatologie': 'Rhumatologie',
    '15-Ophtalmologie': 'Ophtalmologie',
    '17-TOTAL Psychiatrie': 'Psychiatrie',
    '18-TOTAL Stomatologie': 'KO',
    '19-TOTAL Chirurgie dentaire': 'KO',
    '21-Sages-femmes': 'KO',
    '24-Infirmier': 'KO',
    '26-Masseur-kinésithérapeute': 'KO',
    '31-Médecine physique et de réanimation': 'KO',
    '32-Neurologie': 'KO',
    '34-Gériatrie': 'KO',
    '35-Néphrologie': 'KO',
    '36-Chirurgie dentaire spécialistes': 'KO',
    '37-Anatomie-cytologie-pathologique': 'KO',
    '38-Médecin biologiste': 'KO',
    '42-Endocrinologie': 'KO',
    '80-Santé publique et Médecine Sociale': 'KO',
    '99-Spécialité Inconnue': 'KO'}

# Fonction de traduction d'un nombre formaté à l'européenne / française
# (espace en spérateur de milliers, ',' en séparateur décimal)


def to_decimal(val):
    if type(val) == int or type(val) == float:
        return val
    if type(val) == str:
        try:
            temp = float(val.replace(',', '.').replace(' ', '').strip())
            return temp
        except:  # catch *all* exceptions
            return np.nan

# Fonction de recentrage du numéro de département vs un libellé mixete
# numéro + libellé


def to_dept(val):
    return str(val[:val.find('-') - 1])

# Application de la recodification des spécialités du fichier RPPS (fusion
# ensuite par somme des colonnes)


def recodage_rpps(val):
    try:
        temp = mapping_rpps[val]
        return temp
    except:
        return 'KO'

# Application de la recodification des spécialités du fichier R


def recodage_R(val):
    try:
        temp = mapping_R[val]
        return temp
    except:
        return 'KO'

# Lecture du gros fichier R (>3.5 M de lignes pour ne le faire qu'une
# fois), et consolidation pour récupération des données utiles, sauvegarde


def lecture_fileR():
    df = pd.read_csv('R201402.CSV', sep=";", encoding="ISO-8859-1")

    df['rec_mon'] = df['rec_mon'].apply(to_decimal)
    df['dep_mon'] = df['dep_mon'].apply(to_decimal)

    depasst2ParSpecDept = df[['rec_mon', 'dep_mon', 'l_pre_spe', 'dpt']].groupby(
        ('l_pre_spe', 'dpt')).sum()
    depasstParDept = df[['rec_mon', 'dep_mon', 'dpt']].groupby(('dpt')).sum()
    depasstParSpec = df[['rec_mon', 'dep_mon', 'l_pre_spe']
                        ].groupby(('l_pre_spe')).sum()

    depasst2ParSpecDept[
        'taux'] = depasst2ParSpecDept.dep_mon / depasst2ParSpecDept.rec_mon
    depasstParDept['taux'] = depasstParDept.dep_mon / depasstParDept.rec_mon
    depasstParSpec['taux'] = depasstParSpec.dep_mon / depasstParSpec.rec_mon

    depasst2ParSpecDept.to_csv('exo_dom_lesson_5_depasst2ParSpecDept.csv')
    depasstParDept.to_csv('exo_dom_lesson_5_depasstParDept.csv')
    depasstParSpec.to_csv('exo_dom_lesson_5_depasstParSpec.csv')


# DEBUT ANALYSES
# Chargement de la version consolidée des fichiers "lourds"
depasst2ParSpecDept = pd.read_csv(
    'exo_dom_lesson_5_depasst2ParSpecDept.CSV', encoding="ISO-8859-1")
depasstParDept = pd.read_csv('exo_dom_lesson_5_depasstParDept.CSV', encoding="ISO-8859-1")
depasstParSpec = pd.read_csv('exo_dom_lesson_5_depasstParSpec.CSV', encoding="ISO-8859-1")


densite_brut = pd.read_csv('exo_dom_lesson_5_rpps-medecins-tab7_31127192093470.csv',
                           skiprows=4, sep=";", encoding="ISO-8859-1")
densite_brut.specialite = densite_brut.specialite.apply(to_dept)
densite_brut = densite_brut.dropna()
densite_brut.index = densite_brut.specialite


# Recodifcation des colonnes de densité par spécialité (départements en ligne)"
new_names = []
for name in map(recodage_rpps, list(densite_brut.columns)):
    new_names.append(name)

densite = densite_brut.T
densite['agreg'] = new_names
densite_spec = densite.groupby('agreg').sum()
densite_spec = densite_spec.T
densite_spec = pd.DataFrame(densite_spec)

# Chargement du fichier de niveau de vie par département
revenu_brut = pd.read_csv('exo_dom_lesson_5_TCRD_022.csv', skiprows=9,
                          sep=";", decimal=',', encoding="ISO-8859-1")
revenu_brut.index = revenu_brut.dpt
# Choix et normalisation du revenu 
col_rev = 'rev_dec9' # Decile le plus aise
# col_rev = 'rev_median' # Revenu median
# col_rev = 'rev_dec1' # Decile le moins aise

revenu_brut[col_rev] = revenu_brut[col_rev].apply(to_decimal)

# Recodage spécialités du fichier consolidé des remboursements CPAM
depasst2ParSpecDept['agreg'] = depasst2ParSpecDept[
    'l_pre_spe'].apply(recodage_R)
depasst2ParSpecDept2 = depasst2ParSpecDept.groupby(('dpt', 'agreg')).sum()
depasst2ParSpecDept2.taux = depasst2ParSpecDept2.dep_mon / \
    depasst2ParSpecDept2.rec_mon
depasst2ParSpecDept2 = depasst2ParSpecDept2.unstack()

# Boucle sur les analyses par spécialité (sous-ensemble)
for specialite_brute in mapping_R.keys():
    if mapping_R[specialite_brute] != 'KO':
        specialite = mapping_R[specialite_brute]
        densite = pd.DataFrame(densite_spec[specialite])
        taux = pd.DataFrame(depasst2ParSpecDept2[('taux', specialite)])
        matrice = taux.join(densite, how='inner')
        matrice = matrice.join(revenu_brut[col_rev], how='inner')
        matrice.columns = ('taux', 'densite', 'Rev')

        # Traduction en np arrays et centrage / réduction
        taux = np.zeros(matrice.shape[0])
        X = np.zeros((matrice.shape[0], 2))
        taux[:] = matrice.taux
        X[:, 0] = matrice.densite
        X[:, 1] = matrice.Rev
        scalerX = preprocessing.StandardScaler().fit(X)
        X_cr = scalerX.transform(X)  # cr pour centré réduit...

        # Draw chart
        fig = plt.figure(figsize=(15, 10))
        plt.scatter(matrice.taux, X_cr[
                    :, 0], marker='o', color='red', label='Densité ' + specialite, s=100)
        plt.scatter(matrice.taux, X_cr[:, 1], marker='o',
                    color='green', label='Revenu Dpt', s=100)
        plt.legend(loc='upper left', fontsize=20)
        plt.xlabel("Tx Depassement " + specialite, fontsize=18)
        plt.title(
            "taux de dépassement vs densité spécialistes et niveau de vie\n", fontsize=25)

        plt.show()

		# Regressions sur les deux variables
        model_cr = sm.OLS(taux, sm.add_constant(X_cr))
        model_cr.data.ynames = ('Tx Depassement')
        model_cr.data.xnames = ('Constante', 'Densite', 'Niveau de Vie Dpt')
        results = model_cr.fit()

        print("\n\n\n" + "-" * 78)
        print(specialite.upper())
        print("-" * 78)
        print("=" * 78)
        print(results.summary())
        print("=" * 78 + "\n")
