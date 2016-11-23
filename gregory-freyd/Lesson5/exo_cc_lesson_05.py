import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

base_url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
max_number_of_page = 5

def retrieve_meds(med_name, max_number_page):
    meds_gathered_info = []
    for i in range(max_number_page):
        post_request_data = {'btnMedic': 'Rechercher', 'choixRecherche': 'medicament',
                'txtCaracteres': med_name, 'page': str(i)}
        request = requests.post(base_url, data=post_request_data)
        soup = BeautifulSoup(request.text, 'html.parser')
        meds_item = soup.find('table', class_='result').find_all('a', class_='standart')
        meds_item_list = list(map(lambda x : x.text.replace(u'\xa0','')
                                  .replace("\t", '').replace(",", ''), meds_item))
        meds_gathered_info += meds_item_list

    return (map(lambda x: extractDataFromMedTextInfo(x), meds_gathered_info))

def extractDataFromMedTextInfo(raw_text):
    pattern = r'(IBUPROFENE|LEVOTHYROXINE)\s([a-z\s]*)\s(\d*)\s?(mg|µg|%|microgrammes|mg/ml)\s([\w\sé]*)'
    regex_med = re.compile(pattern, flags=re.IGNORECASE)
    med_product_info = regex_med.findall(raw_text)
    return list(med_product_info[0]) if len(med_product_info) > 0 else [None, None, None, None, None]



#Main
df_columns = ['Princeps', 'Marque', 'Dosage', 'Unite', 'Forme medicamenteuse']
med_type = ['Ibuprofene', 'Levothyroxine']
meds_list = []

for med in med_type:
    meds_list += (retrieve_meds(med, max_number_of_page))

med_df = pd.DataFrame(meds_list, columns=df_columns)
med_df.dropna()
print("Saved list to current dir")
med_df.to_csv("meds_list.csv")


