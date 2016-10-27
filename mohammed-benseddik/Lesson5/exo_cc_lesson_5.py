# @ Author : BENSEDDIK Mohammed
# Version : 0.0.2

# Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Define the url for the post request
url_medics = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

# Our array for all the 'medicaments'
medicaments = []

# Loop over the pages of the HTML web site, we work here on the first 3 pages
for page in range(3):

    # Update the form data for the post resquest. We are here interrested just
    # by the 'txtCaracters' field which holds the medication name.
    form_data = {
        "page": page,
        "affliste": 0,
        "affNumero": 0,
        "isAlphabet": 0,
        "inClauseSubst": 0,
        "nomSubstances": '',
        "typeRecherche": 0,
        "choixRecherche": 'medicament',
        "txtCaracteres": 'ibuprofene',
        "btnMedic.x": '20',
        "btnMedic.y": '20',
        "btnMedic": 'Rechercher',
        "radLibelle": 2,
        "txtCaracteresSub": '',
        "radLibelleSub": 4}

    # Initialize the post request with the library requests and appending to
    # the BeautifulSoup variable 'soup'
    r = requests.post(url_medics, form_data)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract all the medications for the 'table'
    rows = soup.findAll('a', {'class': 'standart'})

    # We loop over each row of the medications array
    for row in rows:
        text_medics = row.get_text()

        # Using the regex here to get each field of the medication
        data_medic = re.findall(
            r'(.*)\s(\d{2,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)', text_medics)

        # Try catch here to avoid the Nan values in the soup
        try:
            # We use here a 2D array with the fields medicament, dose, unite and
            # type to get the Dataframe we want
            medicament = (data_medic[0][0] + ' ' + data_medic[0][3])
            dose = int(data_medic[0][1])
            unite = data_medic[0][2]
            type = data_medic[0][4]
            medicaments.append([medicament, dose, unite, type])
        except IndexError:
            None

# Initialize the Dataframe with columns names
df = pd.DataFrame(medicaments, columns=['Medicament', 'Dose', 'Unite', 'Type'])

# Encoding UTF-8 for accents
df.to_csv('medicaments.csv', index=False, encoding='utf-8')
