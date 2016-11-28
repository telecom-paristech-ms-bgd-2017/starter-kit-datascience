import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import os


url = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
drugname = "Levothyroxine"
path = os.path.dirname(os.path.realpath(__file__))


def extractData(drug):
    pattern = r'(\w+)\s(\w+)\s(\d{2,})\s.+,\s(.+\s.+)\t'
    regex_name = re.compile(pattern)
    return regex_name.findall(drug)[0]


def getDrug(drug):
    return extractData(drug.text)


def getDrugsList(url, drog):
    params = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0,
               'inClauseSubst': 0, 'nomSubstances': None, 'typeRecherche': 0,
               'choixRecherche': 'medicament', 'paginationUsed': 0,
               'txtCaracteres': drog, 'radLibelle': 1,
               'txtCaracteresSub': None, 'radLibelleSub': 4}
    res = requests.post(url, data=params)
    print(url)
    return BeautifulSoup(res.text, "html.parser").find(class_="result").find_all(class_="standart")

drugs = map(getDrug, getDrugsList(url, drugname))
header = ['name', 'brand', 'quantity', 'kind']
df = pd.DataFrame.from_records(drugs,columns=header)
df.to_csv(path + "/" + drugname + ".csv")
