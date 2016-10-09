# coding: utf8

"""
Comme exercice pour jeudi je vous demande de crawler le résultat des comptes
de la ville de Paris pour les exercices 2009 à 2013.
Voici par exemple les comptes pour 2013 .
Je vous demande de récupérer les données A,B,C et D sur les colonnes Euros
par habitant et par strate.
"""

import requests
import sys
import pandas
from bs4 import BeautifulSoup

debug_this_sh = True

"""
For debug, display tag content.
"""
def view_tag(tag, n=0):
    print(n*'\t'+'--------Tag--------')
    print(n*'\t',tag)
    print(n*'\t','--------Tag Attributes--------')
    print(n*'\t',tag.attrs)
    print(n * '\t', '--------Tag String--------')
    print(n * '\t', tag.string)



"""
To convert a string into integer and remove tricky chars from utf8.
"""
def to_integer(tag):
    return int(tag.text.replace('\xa0', '').replace(' ', ''))

"""
Will save a DF as a CSV and return the DF
"""
def soup_the_page(arg_url, arg_year):

    # Get the soup object
    soup = BeautifulSoup(requests.get(arg_url).text, "html.parser")


    # This DF will contain the result of the crawl
    pd = pandas.DataFrame(columns=['Total','Per_Citizen', 'Per_Strate', 'Label','Type', 'City'])

    # Init th line counter in DF
    line = -1

    # This will be added on every line and will be our file name.
    city_and_year = 'A city' + arg_year

    # This contain
    for tag_tr in soup.find_all('tr'):

        if 'class' in tag_tr.attrs:

            if tag_tr.attrs['class'][0] == 'bleu':

                # Corresponds to a new line
                line = line +1
                pd.loc[line] = [0,0,0,'empty','empty','empty']
                row = -1

                # Cell per cell horizontally (row ++)
                for tag_td in tag_tr.find_all('td'):
                    # On each line we put the city name
                    pd.loc[line,'City'] = city_and_year

                    # As we started at -1
                    row = row + 1

                    # Check the class in the attribute
                    if 'class' in tag_td.attrs:

                        # Here is the city mame
                        if tag_td.attrs['class'][0] == 'G':
                            city_and_year = tag_td.get_text() + arg_year


                        if tag_td.attrs['class'][0] == 'montantpetit' or tag_td.attrs['class'][0] == 'montantpetit G':

                            if row == 0:
                                pd.loc[line, 'Total'] = to_integer(tag_td)

                            if row == 1:
                                pd.loc[line,'Per_Citizen'] = to_integer(tag_td)

                            if row == 2:
                                pd.loc[line, 'Per_Strate'] = to_integer(tag_td)

                        # Fill Label with the name of the line. Example: "dont : Emprunts bancaires et dettes assimilées"
                        if tag_td.attrs['class'][0].find('libelle') >= 0:
                            pd.loc[line, 'Label'] = tag_td.get_text()
                            pd.loc[line, 'Type'] = tag_td.attrs['class'][0]

    pd.to_csv(city_and_year+".csv", encoding='utf-8')
    print("File:", city_and_year+".csv", "saved.")

    field = ['TOTAL DES PRODUITS DE FONCTIONNEMENT = A',
             'TOTAL DES CHARGES DE FONCTIONNEMENT = B',
             'TOTAL DES RESSOURCES D\'INVESTISSEMENT = C',
             'TOTAL DES EMPLOIS D\'INVESTISSEMENT = D']
    # This DF will contain the result of the crawl
    for index, row in pd.iterrows():
        if row['Label'] in field:
            print(row['Label'], row['Total'], row['Per_Citizen'], row['Per_Strate'])



    return pd

def main():

    # Some definition for the URL
    url_finances_gouv = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?'
    url_param = 'icom=056&dep=075&type=BPS&param=5&exercice='
    url_year = '2013'
    url_full = url_finances_gouv + url_param + url_year

    if len(sys.argv) > 1:
        option_type = sys.argv[1]
        option_value = sys.argv[2]

        if option_type == '--url':
            url_full = option_value
            url_year = option_value[-4:]
        elif option_type == '--year':
            url_year = option_value
            url_full = url_finances_gouv + url_param + url_year
        else:
            print('no option for Paris 2013, or --year for Paris <year> or --url for the rest of the world')
            sys.exit(1)

    soup_the_page(url_full, url_year)

if __name__ == '__main__':
  main()