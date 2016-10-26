from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = 'http://base-donnees-publique.medicaments.gouv.fr' # Set destination URL here
post_fields = {'txtCaractersSub': 'levothyrox'}     # Set POST fields here

request = Request(url, urlencode(post_fields).encode())
# json = urlopen(request).read().decode()

