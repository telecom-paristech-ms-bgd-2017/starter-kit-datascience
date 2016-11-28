import requests
from bs4 import BeautifulSoup
import numpy as np
import json
from multiprocessing import Pool
import time


# ###############################

url = requests.get('http://base-donnees-publique.medicaments.gouv.fr/index.php#result' + 'href="extrait.php?specid=64025557"')
soup = BeautifulSoup(url.text, 'html.parser')


 #href="extrait.php?specid=64025557"

print(soup)

molecule = 'levothyroxine' # molecule

classe = 'standart'
medicaments = soup.find_all(class_=classe)
for med in medicaments: 
      print(med.text)
      #childer = el.findChildren(class_=classe)
      
      

print (medicaments.text)
