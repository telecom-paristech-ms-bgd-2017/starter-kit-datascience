from bs4 import BeautifulSoup
from pprint import pprint
import re, requests

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
post_data = {
    'choixRecherche':'medicament',
    'txtCaracteres':'IBUPROFENE',
    'action': 'show'
}

ids = []
for i in range(1, 5):
    post_data['page'] = i
    resp = requests.post(url, data=post_data).text
    soup = BeautifulSoup(resp, 'html.parser')
    print(soup.text)
    reg_id = re.compile('ibuprofene ([\w ]+) (\d+) ?([\w%]+), ([\w ]+)', re.IGNORECASE)
    ids.extend(reg_id.findall(soup.text))
pprint(ids)
open('out.txt', 'w+').write('\n'.join([str(k) for k in ids]))