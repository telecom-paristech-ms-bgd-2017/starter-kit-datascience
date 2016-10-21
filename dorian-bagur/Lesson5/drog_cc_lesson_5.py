import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import os


URL = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
DROGNAME = "Levothyroxine"
PATH = os.path.dirname(os.path.realpath(__file__))


def extractData(drog):
    pattern = r'(\w+)\s(\w+)\s(\d{2,})\s.+,\s(.+\s.+)\t'
    regex_name = re.compile(pattern)
    return regex_name.findall(drog)[0]


def compose(drog):
    return extractData(drog)


def getDrog(drog):
    return drog.text


def getDrogsList(url, drog):
    payload = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0,
               'inClauseSubst': 0, 'nomSubstances': None, 'typeRecherche': 0,
               'choixRecherche': 'medicament', 'paginationUsed': 0,
               'txtCaracteres': drog, 'radLibelle': 1,
               'txtCaracteresSub': None, 'radLibelleSub': 4}
    res = requests.post(url, data=payload)
    print(url)
    return BeautifulSoup(res.text, "html.parser").find(
        class_="result").find_all(class_="standart")

uncleaned_drog_list = map(getDrog, getDrogsList(URL, DROGNAME))
df = pd.DataFrame.from_records(map(compose, uncleaned_drog_list),
                               columns=['name', 'factory', 'quantity', 'type'])
df.to_csv(PATH + "/" + DROGNAME + ".csv")
