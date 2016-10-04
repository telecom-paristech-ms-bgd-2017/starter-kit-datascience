
import requests
from bs4 import BeautifulSoup

page2013 = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013')
soup_years = BeautifulSoup(page2013.text, 'html.parser')
list_comptes = soup_years.find_all(class_='G')

for el in list_comptes:
  print(el)