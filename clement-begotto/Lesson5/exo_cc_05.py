import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


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
            '\t', '').replace(',', '').replace("", ''), test))
        page_data += test
    return list(map(lambda x: clear_data(x), page_data))


def clear_data(expression):
    pattern = r'(IBUPROFENE|LEVOTHYROXINE)\s+([A-Z\s]+)\s+([0-9]+)\s+([a-z%µ]+)\s([a-zé\s]+)'
    regex_medoc = re.compile(pattern, flags=re.IGNORECASE)
    version = regex_medoc.findall(expression)
    return list(version[0]) if len(version) > 0 else [None, None, None, None, None]


# Main
columns = ["Medicament", "Marque", "Dosage", "Unite", "Forme medicamenteuse"]
medicament_type = ["Ibuprofene", "Levothyroxine"]
medoc_database = []

for curr_medoc in medicament_type:
    medoc_database += load_medics(curr_medoc, 4)

medoc_dataframe = pd.DataFrame(medoc_database, columns=columns)
medoc_dataframe.to_csv("trimedoc.csv")
