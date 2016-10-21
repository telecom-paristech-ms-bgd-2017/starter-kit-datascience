import requests
from bs4 import BeautifulSoup
import re

pattern_ibu = "(IBUPROFENE)\s([\w\s]+)\s(\d+)(\smg|\s%), ([a-zA-Zé ]{1,20})"
re_ibu = re.compile(pattern_ibu, flags=re.IGNORECASE)
pattern_levo = "(levothyroxine)"

url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"

dico_post = {
    "page": 1,
    "affliste": 0,
    "affNumero": 0,
    "isAlphabet": 0,
    "inClauseSubst": 0,
    "choixRecherche": "medicament",
    "paginationUsed": 0,
    "txtCaracteres": "IBUPROFENE",
    "btnMedic.x": 12,
    "btnMedic.y": 8,
    "btnMedic": "Rechercher",
    "radLibelle": 2,
    "radLibelleSub": 4,
}

post = requests.post(url, dico_post)

list_medic = re_ibu.findall(post.text)

