import requests
from bs4 import BeautifulSoup

# PARAMETERS
column_per_hab_number = 1 #Colonne moyenne de la strate
column_per_layer_number = 2 #Colonne euros par habitant

figure_names = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
                    "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
                    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
                    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]


def getFiguresForCityWithURL(year, base_url):
    """
    Returns all the metrics for a city given a base URL (not containing year value) and a year
    """
    figures_city = {}
    data = []

    figures_city_page = requests.get(base_url)# + str(year) + "")
    soup_city = BeautifulSoup(figures_city_page.text, 'html.parser')

    html_table_rows = soup_city.find_all('tr')

    for html_table_row in html_table_rows:
        for figure_name in figure_names: #A, B, C, D
            if(figure_name in html_table_row.text):
                cols = html_table_row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                figures_city[figure_name] = [cols[column_per_hab_number], cols[column_per_layer_number]]
                data.append([cols[column_per_hab_number], cols[column_per_layer_number]])

    return figures_city

def getFiguresForCity(year_min, year_max, id_commmune, id_departement):
    # Getting values for city
    for year in range(year_min, year_max + 1):
        print("*** Résultats pour l'année " + str(year) + " en euros/hab, et en moyenne de la strate")
        figures_city = getFiguresForCityWithURL(year,
              "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=" + str(id_commmune)
              + "&dep=" + str(id_departement) + "&type=BPS&param=5&exercice=" + str(year))

        # Printing values for city
        for key, val in figures_city.items():
            print(key + "\t\t\t\t" + val[0] + " | "+ val[1])
        print("")


def getFiguresForParis():
    """
    Returns figures for Caen city
    """
    print("------------------------Ville de Paris------------------------\n")
    getFiguresForCity(2010, 2015, "056", "075");


def getFiguresForCaen():
    """
    Returns figures for Caen city
    """
    print("------------------------Ville de Caen------------------------\n")
    getFiguresForCity(2000, 2015, "118", "014");

# Test
getFiguresForParis()
getFiguresForCaen()