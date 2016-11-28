from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import json
from pandas import DataFrame, Series


medicines = ['ibuprofene']

# URL
url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

# Max. number of pages, alt. max_nb_pages = int(list(map(lambda x: x.text, soup.select('.navBar > li')))[-1])
max_nb_pages = 2


def get_infos(medicine):
    # POST request parameters
    params_post = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0, 'inClauseSubse': 0, 'nomSubstances': '',
                   'typeRecherche': 0, 'choixRecherche': 'medicament', 'paginationUsed': 0,
                   'txtCaracteres': medicine, 'btnMedic.x': 0, 'btnMedic.y': 0, 'btnMedic': 'Rechercher',
                   'radLibelle': 2, 'txtCaracteresSub': '', 'radLibelleSub': 4}
    # POST request
    response = requests.post(url, data=params_post)

    # Building of the parser
    soup = BeautifulSoup(response.text, 'html.parser')

    infos = get_infos_medicine(soup, medicine)

    return infos


def get_infos_medicine(soup, medicine):
    # Name of the medicines
    selector = soup.select('.standart')

    # Dictionary containing all medicines' specifications
    info_medicament = {'nom': [], 'laboratoire': [], 'dosage': []}

    # Iterate over the list of medicines
    for sel in selector:
        medicament_desc = sel.text
        groups = re.findall(r'({})\s([\w\s]+)\s([\d]+\s?[a-zA-Z%]+)'.format(medicine), medicament_desc, flags=re.IGNORECASE)
        try:
            info_medicament['nom'].append(groups[0][0])
            info_medicament['laboratoire'].append(groups[0][1])
            info_medicament['dosage'].append(groups[0][2])
        except:
            print('Feature extraction issue')

    return info_medicament


def get_all_infos(medicines):
    res = list(map(get_infos, medicines))
    print(res)

get_all_infos(medicines)


# Utilisation des reg-ex pour extraire ces données (compile, search)
# re.findall(r"", )

#url = 'https://www.vidal.fr/Substance/ibuprofene-1844.htm'

#response = requests.get(url)

#soup = BeautifulSoup(response.text, 'html.parser')

#chn_reg = r"(ibuprofene){1}"
#ex_reg = re.compile(chn_reg, flags=re.IGNORECASE)
#med = []
#for s in selector:
#    name_medoc = s.text
#    res = ex_reg.search(name_medoc)
#    if res is not None:
#        med.append(name_medoc.strip())

#dict = {'Molecule': [], 'Laboratoire': [], 'Dosage': [], 'Secable': []}

# chn_ex_type = r"(pellic | enr | gel)"
#ex_reg_type = re.compile(chn_ex_type, flags=re.IGNORECASE)

#chn_ex_volume = r"[0-9]{3,4} * mg"
#ex_reg_volume = re.compile(chn_ex_volume, flags=re.IGNORECASE)

#for m in med:
#    type_res = ex_reg_type.search(m)
#    if type_res is not None:
#        type =
#    if
# reg_ex_name = r"[ibuprofene]{1} * ]"