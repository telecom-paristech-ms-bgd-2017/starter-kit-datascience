# nom medicaments ibuprofene levothyroxine
# Faire un dataframe avec ces données
# site web : http://base-donnees-publique.medicaments.gouv.fr/

from bs4 import BeautifulSoup
import pandas as pd
import requests as req
import re

url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"
medicaments = ["ibuprofene", "levothyroxine"]


def get_details_info_med(nom_med):
    params = {"page": 1,
              "affliste": 0,
              "affNumero": 0,
              "isAlphabet": 0,
              "inClauseSubst": 0,
              "nomSubstances": "",
              "typeRecherche": 0,
              "choixRecherche": "medicament",
              "paginationUsed": 0,
              "txtCaracteres": nom_med,
              "btnMedic.x": 14,
              "btnMedic.y": 8,
              "btnMedic": "Rechercher",
              "radLibelle": 2,
              "txtCaracteresSub": "",
              "radLibelleSub": 4
              }

    html = req.post(url, data=params)
    soup = BeautifulSoup(html.text, "html.parser")

    liste_medicaments = [medic.text.replace('\t', "") for medic in soup.find_all('a', {"class": "standart"}) if
                         nom_med.upper() in medic.text]
    regex = re.compile(r"("+re.escape(nom_med.upper())+r")"+r"\s([A-Z\s]+)([0-9]+)\s?([a-zµ%]+),\s([a-zéèàêâùïüë ]+)")
    result = [re.findall(regex, medicament)[0] for medicament in liste_medicaments]
    return pd.DataFrame(result, columns=['Nom medoc', 'Société', 'Quantité', 'unité', 'Format'])


if __name__ == '__main__':
    [print(get_details_info_med(medicament)) for medicament in medicaments]

