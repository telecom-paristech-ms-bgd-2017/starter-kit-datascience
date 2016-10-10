from bs4 import BeautifulSoup
import requests
import pandas as pd

# Variable
url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
years = range(2010, 2016)
ind_dic = {'A': 6, 'B': 10, 'C': 18, 'D': 23}


def commune_stat(url, years):
    stat = []
    for num, year in enumerate(years):
        response = requests.get(url + str(year))
        soup = BeautifulSoup(response.text, 'html.parser')
        stat.append(determine_statistics(soup))
        print('\n---------Year ' + str(year) + ' ---------')
        print(stat[num])
        print()
    return stat


def determine_statistics(soup):
    dic = {}
    for letter, ind in ind_dic.items():
        tup = soup.select("body > table:nth-of-type(3) > tr:nth-of-type(%d) > .montantpetit.G" % ind)
        dic[letter] = (int(tup[1].text.replace('\xa0', '').replace(' ', '')), int(tup[2].text.replace('\xa0', '').replace(' ', '')))
    return dic


stat = commune_stat(url, years)
df = pd.DataFrame(stat)
print(df)
df.to_csv('commune_paris_years.csv')