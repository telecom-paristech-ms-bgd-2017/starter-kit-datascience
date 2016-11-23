import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from multiprocessing import Pool
from functools import partial
import time
import numpy as np

numProcesses = 4 # my number of cores
run_type = 'Parallel' # Parallel or Sequential

medicament = 'IBUPROFENE'

regex_IBUPROFENE = medicament+' ([A-Z ]+) (\d+) ?([\w%]+),([ \w]+)'

requestURL = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'


def BuilParam(nomMedicament,page):
    paramMedoc = {
        'page':page,
        'affliste':0,
        'affNumero':0,
        'isAlphabet':0,
        'inClauseSubst':0,
        'nomSubstances':'',
        'typeRecherche':0,
        'choixRecherche':'medicament',
        'paginationUsed':0,
        'txtCaracteres': nomMedicament,
        'radLibelle':2,
        'txtCaracteresSub': '',
        'radLibelleSub':4
     
    }
    return paramMedoc 


def processPage(medicament,page):
    
    
    paramMedoc = BuilParam(medicament,1)
    requestResponse = requests.post(requestURL, paramMedoc).text
    soup = BeautifulSoup(requestResponse, 'html.parser')
    medicament_liste = soup.find_all("td", class_ = 'ResultRowDeno')
    #print len(medicament_liste)
    
    medocs_ByPage = []
    for med in medicament_liste:
        #print med.find("a", class_ = 'standart').text.strip()
        chaine_med = med.find("a", class_ = 'standart').text.strip()
        match = re.search(regex_IBUPROFENE, chaine_med)
        #print match.group(1), match.group(2), match.group(3), match.group(4)
        try:
            medocs = {}
            medocs['nom'] = match.group(1).strip()
            medocs['dose'] = match.group(2).strip()
            medocs['unite'] = match.group(3).strip().strip()
            medocs['forme'] = match.group(4).strip()
            medocs_ByPage.append(medocs)
        except AttributeError:
                    print "Matching regex False"
    return medocs_ByPage
        
        

def processMedicament(medicament):
    medicaments_feature = []
    
    page = 1
    paramMedoc = BuilParam(medicament,page)
    requestResponse = requests.post(requestURL, paramMedoc).text
    soup = BeautifulSoup(requestResponse, 'html.parser')
    page_liste = soup.find_all("a", class_ = 'standart', attrs={"onmouseover": "self.status='';return true"})
    #print len(page_liste)
    
    if (run_type == 'Sequential'):
        for page_number in np.arange(len(page_liste)+1)+1:
            print 'page_number '+str(page_number)
            medicaments_feature = medicaments_feature + processPage(medicament,page_number)
    else:
        pool = Pool(numProcesses)
        func = partial(processPage, medicament)
        medicaments_feature = pool.map(func, np.arange(len(page_liste)+1)+1)
        pool.close()
        pool.join()
        flattenned_medocs_feature = [val for sublist in medicaments_feature for val in sublist] #
        medicaments_feature = flattenned_medocs_feature
    
    print (len(medicaments_feature))
    return medicaments_feature
    


if __name__ == '__main__':
    
    start_time = time.time()

    medicaments_feature = processMedicament(medicament)
    df_medicaments = pd.DataFrame(medicaments_feature, columns=['nom', 'dose', 'unite', 'forme'])
    df_medicaments.to_csv('medicament_'+medicament+'.csv', index=False, encoding='utf-8')
    print(
        "--- Run type : {0}. Exec time (in s) : {1} ---".format(run_type, time.time() - start_time))