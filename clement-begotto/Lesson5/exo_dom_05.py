import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def liens_voitures(soup_recherche):
    return list(map(lambda x: x, soup_recherche.find_all(class_='list_item clearfix trackable')))


def type_vendeur(link):
    return "Particulier" if link.find('span', class_="ispro") == None else "Professionnel"


def extract_prix_kilometrage_date(soup_recherche, data_storage):
    return [value.find('span', class_="value").text.replace('\xa0', '').strip().
            replace(' ', '').replace('€', '').replace('KM', '')
            for value in soup_recherche.find_all('h2', class_='clearfix')
            if value.find('span', class_="property").text in data_recherche.keys()]


def extract_version(soup_recherche):
    title = soup_recherche.find(class_="no-border").text
    pattern = r'LIFE|INTENS|ZEN'
    regex_title = re.compile(pattern, flags=re.IGNORECASE)
    version = regex_title.findall(title)

    pattern = r'(type\s2)'
    regex_title = re.compile(pattern, flags=re.IGNORECASE)
    type_2 = regex_title.findall(title)

    version_complete = version[0].lower() if len(version) > 0 else "NOT FOUND"

    return (version_complete,  '+' + type_2[0].lower().replace(' ', '+')) if len(type_2) > 0 else (version_complete, '')


def extract_tel(soup_recherche):
    description = recherche_curr_leboncoin.find(
        class_="line properties_description").text
    pattern = r'([0|\\+33|0033][1-9][0-9]{8})'
    regex_description = re.compile(pattern, flags=re.IGNORECASE)
    numero = regex_description.findall(description)
    return numero[0] if len(numero) > 0 else "NOT FOUND"


def cote_argus(version_complete, type_2, date):
    type_2 = '+type+2' if date == "2016" else type_2
    url_cotation = 'http://www.lacentrale.fr/cote-auto-renault-zoe-<version>+charge+rapide+<type>-<date>.html'
    recherche_curr_cote = BeautifulSoup(requests.get(url_cotation.replace(
        '<version>', version_complete).replace('+<type>', type_2).replace('<date>', date)).text, 'html.parser')
    cote = recherche_curr_cote.find(
        'strong', class_='f24 bGrey9L txtRed pL15 mL15')
    return float(cote.text.strip()[:-1].replace(' ', '')) if version_complete != "NOT FOUND" else "NOT FOUND"

# Main
url = u'https://www.leboncoin.fr/voitures/offres/<region>/?th=1&q=Renault%20Zoé&parrot=0'
data_recherche = {'Version': [], 'Année-modèle': [], 'Kilométrage': [],
                  'Prix': [], 'Téléphone': [], 'Vendeur': [], 'Argus': [], 'Région': []}
regions = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']

for region in regions:
    req_general_leboncoin = requests.get(url.replace('<region>', region))
    recherche_general_leboncoin = BeautifulSoup(
        req_general_leboncoin.text, 'html.parser')

    for link in liens_voitures(recherche_general_leboncoin):

        recherche_curr_leboncoin = BeautifulSoup(
            requests.get("https:" + link['href']).text, 'html.parser')
        table_extract = extract_prix_kilometrage_date(
            recherche_curr_leboncoin, data_recherche)

        version_complete, type_2 = extract_version(recherche_curr_leboncoin)

        data_recherche['Version'].append(version_complete)
        data_recherche['Prix'].append(float(table_extract[0]))
        data_recherche['Année-modèle'].append(table_extract[1])
        data_recherche['Kilométrage'].append(float(table_extract[2]))
        data_recherche['Région'].append(region.replace("_", ' '))
        data_recherche['Vendeur'].append(type_vendeur(link))
        data_recherche['Argus'].append(cote_argus(
            version_complete, type_2, table_extract[1]))
        data_recherche['Téléphone'].append(
            extract_tel(recherche_curr_leboncoin))

pd.DataFrame(data_recherche).to_csv('test.csv', sep=';')
