# ibuprofène, levothyroxine
# base-donnees-publique.medicaments.gouv.fr

import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
from _overlapped import NULL


def data(medicament, page, x, y):
    return {'page': page,
            'affliste': '0',
            'affNumero': '0',
            'isAlphabet': '0',
            'inClauseSubst': '0',
            'typeRecherche': '0',
            'choixRecherche': 'medicament',
            'paginationUsed': '0',
            'txtCaracteres': medicament,
            'btnMedic.x': x,
            'btnMedic.y': y,
            'btnMedic': 'Rechercher',
            'radLibelle': '2',
            'radLibelleSub': '4'}


def crawl(medicament, pages, x, y):

    df = pd.DataFrame()

    for page in pages:

        r = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php',
                          data=data(medicament, page, x, y))

        soup = bs(r.text, 'html.parser')
        standarts = soup.find_all(class_='standart')
        texts = list(standart.text for standart in standarts)

        medocs = []
        for text in texts:
            found = (re.findall("(" + str.upper(medicament) +
                                ")\s(.+)\s([0-9]+)\s*(\w+|%\/*\w*),*\s([\w\s,éà]+)", text))
            if found:
                medocs.append(found)

        if df.empty:
            df = pd.DataFrame(list(medoc[0] for medoc in medocs), columns=[
                              'medoc', 'labo', 'quantite', 'unite', 'type'])
        else:
            df = pd.concat((df, pd.DataFrame(list(medoc[0] for medoc in medocs), columns=[
                           'medoc', 'labo', 'quantite', 'unite', 'type'])), ignore_index=True)

    df['type'] = df['type'].str.strip()
    print(df)


crawl('ibuprofene', ['1', '2', '3'], '8', '12')
crawl('levothyroxine', ['1'], '10', '9')
