from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import URLError
import pandas as pd
import numpy as np

for date in range(2010, 2014):
    try:
        html = urlopen(
            "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(date))
    except URLError as e:
    	print(e)

    obj = BeautifulSoup(html, "lxml")
    print(date)
    for k in [0, 1, 3, 4]:
        res = obj.findAll(class_="libellepetit G")[k].parent()[1:]
        lst = list()
        for name in res:
            u = name.get_text().replace('\xa0', ' ')
            lst.append(u)
            reverse_lst = lst[::-1]
            ar = np.asarray(reverse_lst[1::])
        print(ar)
        

