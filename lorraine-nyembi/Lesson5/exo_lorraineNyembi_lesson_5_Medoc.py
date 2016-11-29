# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:42:48 2016

@author: lorraine
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np


#URL = 'http://base-donnees-publique.medicaments.gouv.fr/'
URL = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
def displayMedocInDataFrame(nbPages, nomMedoc):
    moleculeMedoc = []
    dosageMedoc = []
    typeMedoc = []
    
    for i in range(1, nbPages):
        parametresPost = {'page':str(i),
        'affliste':'0',
        'affNumero':'0',
        'isAlphabet':'0',
        'inClauseSubst':'0',
        'nomSubstances':'',
        'typeRecherche':'0',
        'choixRecherche':'medicament',
        'paginationUsed':'0',
        'txtCaracteres': nomMedoc,#https://www.google.fr/#q=banque+de+m%C3%A9dicaments
        'btnMedic.x':'0',
        'btnMedic.y':'0',
        'btnMedic':'Rechercher',
        'radLibelle':'2',
        'txtCaracteresSub':'',
        'radLibelleSub':'4'}
        
        resultsPost = requests.post(URL, data = parametresPost)
        resultsParser = BeautifulSoup(resultsPost.text, 'html.parser')
        listMedocs = resultsParser.find_all(class_="standart")


        for medoc in listMedocs:
            #print(medoc.get_text())
        
            #(\AIBUPROFENE\s\w+\s)([0-9]+)(\s\w+)(,\s)([a-zA-Z]+)
            #(^IBUPROFENE\s\w+\s)([0-9]+)(\s\w+)(,\s)([a-zé]+)\s\w+é
            #my_reg = re.compile('(^IBUPROFENE\s\w+\s)([0-9]+)(\s\w+)(,\s)([a-zé]+)\s\w+é')
            
            my_reg = re.compile('(^IBUPROFENE)\s+(\D[A-Z]+\s)+')
            resultMatch  = my_reg.search(medoc.text)
            if(resultMatch):
                print(resultMatch.group(0))
                moleculeMedoc.append(resultMatch.group(0))
            else:
                moleculeMedoc.append("")
                
            my_reg = re.compile('((\d+\s)|(\d))(%|\w+[^a-zA-Z0-9,]\w+)')
            resultMatch  = my_reg.search(medoc.text)
            if(resultMatch):
                dosageMedoc.append(resultMatch.group(0))
            else:
                dosageMedoc.append("")     
        
            my_reg = re.compile(',\s(.)+')
            resultMatch  = my_reg.search(medoc.text)
            if(resultMatch):
                typeMedoc.append(resultMatch.group(0).replace(",", ""))
            else:
                typeMedoc.append("")     
            
    df = pd.DataFrame({"Molecule":moleculeMedoc ,  "dosage": dosageMedoc, "type":typeMedoc})
    df['Molecule'] = df['Molecule'].replace("", np.nan)
    df = df.dropna(axis=0)
    df = df.set_index(np.arange(df.shape[0]))
    print(df)
    
    df.to_csv("Medicaments_Regex.csv", sep=',')
    
displayMedocInDataFrame(5, "ibuprofene")
    
    
    
