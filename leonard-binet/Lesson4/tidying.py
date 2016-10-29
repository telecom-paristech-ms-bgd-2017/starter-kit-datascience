import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re

csv = 'John, 47 rue Barrault, 36 ans'

# strip
texte_cb = "Je vous remercie pour votre paiement avec 1234-3323-1444-3443"

liste_id = map(lambda x: x.strip(), csv.split(','))
cred = re.compile(r'\d{4}-\d{4}-\d{4}')

test = re.sub(cred, "XXXX-XXXX-XXXX", texte_cb)
