import requests
from bs4 import BeautifulSoup as bs


url_without_year = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
years = range(2010, 2016)
data_rows = {'A': 6, 'B': 10, 'C': 18, 'D': 23}
data = {}
per_hab = '_per_hab'
layer_mean = '_layer_mean'


for year in years:

    data[year] = {}
    request = requests.get(url_without_year + str(year))
    soup = bs(request.text, 'html.parser')

    for data_letter, data_row in data_rows.items():
        selected = soup.select(
            "table:nth-of-type(3) > tr:nth-of-type(%d) > .montantpetit.G" % data_row)
        data.get(year)[data_letter + per_hab] = selected[1].text.strip()
        data.get(year)[data_letter + layer_mean] = selected[2].text.strip()


for year in sorted(data.keys()):

    print('------------------------\n')
    print('Année ' + str(year) + ' :')
    print('\nEuros par habitant :')
    for data_letter in sorted(data_rows):
        print(' ' + data_letter + ' = ' + data[year][data_letter + per_hab])
    print('\nMoyenne de la strate :')
    for data_letter in sorted(data_rows):
        print(' ' + data_letter + ' = ' + data[year][data_letter + layer_mean])
