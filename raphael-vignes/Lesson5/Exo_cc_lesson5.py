import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import re
from functools import partial
import sys


def getMedicineInfos(url, medoc, maxPage):
    for page in range(1,maxPage+1):
        data = {'choixRecherche': 'medicament', 'page': page, 'radLibelle': 2, 'radLibelleSub': 4, 'txtCaracteres': medoc,
                'typeRecherche': 0}
        request = requests.post(url, data)
        request = BeautifulSoup(request.text,"html.parser")
        page_results = getFormsofMedicine(request)
        medicine_list = []
        for result in page_results:
            medicine_list.append(getFormsofMedicine(result))
    return medicine_list

def getFormsofMedicine(soup):
    print("*",type(soup))
    results = soup.find_all(class_="ResultRowDeno")
    return results

def getInfos(results):
    medicine = []
    for result in results:
        med = {}
        extract = result.search("ibuprofene\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+),([\w\sé])", result)
        med["Name"] = extract.group(0)
        med["Forme"] = extract.group(1)
        med["Qté"] = extract.group(2)
        medicine.append(med)
    return  medicine

medocs = ['ibuprofene','levothyroxine']
url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#"
test = getFormsofMedicine(getMedicineInfos(url, medocs[0],5))
print(test)