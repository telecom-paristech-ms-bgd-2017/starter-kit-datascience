import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

URL = 'http://base-donnees-publique.medicaments.gouv.fr/'

#inscpecter netork, index, headers
#il faut faire un regex pour obtenir un tableau "medoc", "dosage", "type comprimé
#+ ibuprofène"
def loadMedocs(page, nomMedoc):
    payload = {
        'page': page,
        'affliste':'0',
        'affNumero':'0',
        'isAlphabet':'0',
        'inClauseSubst':'0',
        'nomSubstances':'',
        'typeRecherche':'0',
        'choixRecherche':'medicament',
        'paginationUsed':'0',
        'txtCaracteres':nomMedoc,
        'btnMedic.x':'20',
        'btnMedic.y':'20',
        'btnMedic':'Rechercher',
        'radLibelle':'2',
        'txtCaracteresSub':'',
        'radLibelleSub':4
        }

    r = requests.post(URL,data = payload)
    r2 = BeautifulSoup(r.text, 'html.parser').find("table",{'class' : 'tablealigncenter'})
    medocs = r2.find_all(class_="ResultRowDeno")
    return medocs

def stuffMatrix(pages, nomMedoc):
    df = pd.DataFrame(columns = ["Molécule", "dose", "type"])
    ExprMol = re.compile("(IBUPROFENE)\s+([A-Z]+)")
    ExprDose = re.compile("[^\s]+[0-9]{2,3}\s(mg)")
    ExprType = re.compile(",\s(.)+")
    for page in range(pages):
        medocs = loadMedocs(page, nomMedoc)
        for medoc in medocs:
            print(medoc.text.strip())
            try:
                molecule = ExprMol.search(medoc.text.strip()).group().split(" ")[1]
                dose = ExprDose.search(medoc.text.strip()).group().replace("mg", "")
                typeM = ExprType.search(medoc.text.strip()).group().replace(",", "").strip()

            except Exception as e:
                molecule = ""
                dose = ""
                typeM = ""
            df = df.append({'Molécule': molecule, 'dose' : dose, 'type': typeM}, ignore_index = True)
    return(df)

stuffMatrix(3, "IBUPROFENE").to_csv('ibuprofene.csv', sep=',')
