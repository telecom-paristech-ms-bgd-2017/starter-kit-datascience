import re

import pandas as pd
import requests
import unicodedata
from bs4 import BeautifulSoup

Url = "https://www.data.gouv.fr/storage/f/2013-11-28T11%3A43%3A25.672Z/medicaments.json"

#Ibuprofene
#Levothyroxine
#base-donnees-publique.medicaments.gouv.fr
#nom, dosage, forme, marque

def get_med_base():
    data = requests.get(Url)
    return data.json()

# Borrowed from http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
def strip_accents(string, accents=('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT', 'COMBINING TILDE')):
    accents = set(map(unicodedata.lookup, accents))
    chars = [c for c in unicodedata.normalize('NFD', string) if c not in accents]
    return unicodedata.normalize('NFC', ''.join(chars))


def get_med(med_base, *names):
    med_details = []
    print(med_base)
    for name in names:
        name = name.lower()
        for med in med_base:
            re_name = re.match(".*" + name + ".*", med['title'].lower())
            if not re_name is None:
                details = {}
                title = med['title']
                #s = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode() # Not good enough the mu character gets unfotunately stripped out
                s = strip_accents(title)
                re_details = re.match("([a-zA-Z]+)\s+(([a-zA-Z]+|\s+)+)\s+((\d+\s+(mg/ml|l|%|mg|microgrammes|µg|milligrammes|mg))[^,]*)?(,\s+(([a-zA-Z]+|\s+)+))?", s)
                details['Nom'] = re_details.group(1)
                details['Forme'] = re_details.group(8)
                details['Marque'] = re_details.group(2)
                details['Dosage'] = re_details.group(5)
                med_details.append(details)
    return pd.DataFrame(med_details)


df = get_med(get_med_base(), "ibuprofen", "Levothyroxine")
print(df)