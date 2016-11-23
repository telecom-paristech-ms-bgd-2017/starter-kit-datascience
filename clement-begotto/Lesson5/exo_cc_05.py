import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import math

def load_medics(medic_name, nb_page):
    page_data = []
    search_url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

    for i in range(nb_page):
        data = {'txtCaracteres': medic_name, 'choixRecherche': 'medicament',
                'btnMedic': 'Rechercher', 'page': str(i)}
        r = requests.post(search_url, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        test = soup.find('table', class_='result').find_all(
            'a', class_='standart')
        test = list(map(lambda x: x.text.replace(
            '\t', '').replace(',', '') , test))
        page_data += test
    return list(map(lambda x: clear_data(x), page_data))


def clear_data(expression):
    pattern = r'(IBUPROFENE|LEVOTHYROXINE)\s+([A-Z\s]+)\s+([0-9]+)\s+([a-z%µ]+)\s([a-zé\s]+)'
    regex_medoc = re.compile(pattern, flags=re.IGNORECASE)
    version = regex_medoc.findall(expression)
    return list(version[0]) if len(version) > 0 else [np.nan, np.nan, np.nan, np.nan, np.nan]


# Main
columns = ["Medicament", "Marque", "Dosage", "Unite", "Forme medicamenteuse"]
medicament_type = ["Ibuprofene", "Levothyroxine"]
medoc_database = []

for curr_medoc in medicament_type:
    medoc_database += load_medics(curr_medoc, 4)

medoc_dataframe = pd.DataFrame(medoc_database, columns=columns)
medoc_dataframe["nulldata"] = list(map(lambda x : math.isnan(float(x)), medoc_dataframe["Dosage"].tolist() ))
medoc_dataframe = medoc_dataframe[medoc_dataframe['nulldata'] == False]
medoc_dataframe = medoc_dataframe[["Medicament", "Marque", "Dosage", "Unite", "Forme medicamenteuse"]]
medoc_dataframe.to_csv("trimedoc.csv")
