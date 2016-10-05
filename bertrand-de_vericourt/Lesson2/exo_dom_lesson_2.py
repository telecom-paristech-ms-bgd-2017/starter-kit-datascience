
# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup
years = range(2009,2014)
dict_comptes = {}
rowsToParse = (10,14,22,27)
colToParse = (2,3,4)

for year in years:
  try:
    page_year = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(year))
    soup_years = BeautifulSoup(page_year.text, 'html.parser')

    # initialize list of data for the year
    list_comptes_year = []

    for rows in rowsToParse:
      for col in colToParse:
        list_comptes_year.append(soup_years.select('tr:nth-of-type(' + str(rows) + ')')[0].select('td:nth-of-type(' + str(col) + ')')[0])

    # Add the accounts of current year to the dictionary
    dict_comptes[year] = list_comptes_year

    print('=====')
    print('year ' + str(year) + ' :')
    print('=====')
    for el in dict_comptes[year]:
      print(el.text)
  except:
    print('=====')
    print('error for year ' + str(year))
    print('=====')