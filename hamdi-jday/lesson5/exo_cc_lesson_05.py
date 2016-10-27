import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

url = 'http://base-donnees-publique.medicaments.gouv.fr/'  # url où chercher les molecules
liste_recherche = ['ibuprofene', 'levothyrox', 'doliprane']  # liste des molecules à chercher
columns = ['molecule', 'qte', 'unite', 'galenique']  # colonnes de la DataFrame résultat
pattern = "(LEVOTHYROX|IBUPROFENE|DOLIPRANE)(?:[A-Z ]+)? (\d+) ([a-z ]+), ?([\w%]+)"  # regex matchant les attributs des colonnes de la DF resultat
max_page = 5  # nombre de pages resultats à scrapper

def get_data_page(molecule, page):
    data = {'page':page, 'affliste':0, 'affNumero':0, 'isAlphabet':0, 'inClauseSubst':0, 'typeRecherche':0, 'choixRecherche':'medicament', 'paginationUsed':0, 'txtCaracteres':molecule, 'btnMedic.x':16, 'btnMedic.y':12, 'btnMedic':'Rechercher', 'radLibelle':2, 'radLibelleSub':4}
    r = requests.post(url, data)
    soup = BeautifulSoup(r.text, 'html.parser')
    # data = soup.find_all(class_='ResultRowDeno')
    raw_result = soup.find_all(text=re.compile(pattern))
    result = [[re.compile(pattern).search(el).group(1), re.compile(pattern).search(el).group(2), re.compile(pattern).search(el).group(3), re.compile(pattern).search(el).group(4)] for el in raw_result]
    return result


def global_result_molecule(molecule, nombre_pages):
    result = []
    for i in range(1, nombre_pages+1):
        result = result + get_data_page(molecule, i)
    return result


resultat = []
for i in range(len(liste_recherche)):
    resultat = resultat + global_result_molecule(liste_recherche[i], max_page)
    
# resultat = global_result_molecule("LEVOTHYROX", max_page) + global_result_molecule("IBUPROFENE", max_page)
df = pd.DataFrame(resultat, columns=columns)
df.to_csv('medicaments_galenique.csv')
print(df)
