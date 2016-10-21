#!/usr/bin/env python3

# standard library imports

# related third party imports
import requests
import pandas
import re
from bs4 import BeautifulSoup


class Scraping:
    FILE = 'data.csv'
    URL = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

    def __init__(self):
        pass

    class Medicament:
        def __init__(self):
            self.name = None
            self.description = None
            self.quantity = None
            self.unity = None

    # public methods

    @staticmethod
    def get(medicament):
        url = Scraping.URL
        data = {
            'page': 1,
            'affliste': 0,
            'affNumero': 0,
            'isAlphabet': 0,
            'inClauseSubst': 0,
            'nomSubstances': '',
            'typeRecherche': 0,
            'choixRecherche': 'medicament',
            'paginationUsed': 0,
            'txtCaracteres': medicament,
            'btnMedic.x': 0,
            'btnMedic.y': 0,
            'btnMedic': 'Rechercher',
            'radLibelle': 2,
            'txtCaracteresSub': '',
            'radLibelleSub': 4
        }
        result = requests.post(url, data=data)
        bs = BeautifulSoup(result.text, 'html.parser')
        meds = []
        for link in bs.find_all('a', class_='standart'):
            med = Scraping.Medicament()
            text = link.contents[0].strip()
            regex = r'([A-Z]+) (\d+) ([a-z]+),(.*)'
            match = re.search(regex, text)
            if match:
                med.name = match.group(0)
                med.quantity = match.group(1)
                med.unity = match.group(2)
                med.description = match.group(3)
                meds.append(med)
        return bs, meds


    @staticmethod
    def persist(item):
        if len(item) == 0:
            return pandas.DataFrame()
        item_dicts = [item.__dict__ for item in item]
        columns = list(item_dicts[0].keys())
        df = pandas.DataFrame(item_dicts, columns=columns)
        df.to_csv(Scraping.FILE, index=False)
        return df


if __name__ == "__main__":
    bs, meds = Scraping.get('doliprane')
    Scraping.persist(meds)
