import requests
from bs4 import BeautifulSoup


def getStatsByYear(year):
    print "\n\n========================================== ANNEE "+str(year)+" =========================================="
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + \
        str(year)
    finances_page = requests.get(url)
    soup_finances = BeautifulSoup(finances_page.text, 'html.parser')

    print "\nOPERATIONS DE FONCTIONNEMENT: \n\n"
    print "\tTOTAL DES PRODUITS DE FONCTIONNEMENT = A:\n"
    soup_PRODUITS_FONCTIONNEMENT = soup_finances.find(
        string="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent
    soup_Infos = soup_PRODUITS_FONCTIONNEMENT.find_previous_siblings()
    print "\t\tEn milliers d'Euros: "+soup_Infos[2].string
    print "\t\tEuros par habitant: "+soup_Infos[1].string
    print "\t\tMoyenne de la strate: "+soup_Infos[0].string
    print
    print "\tTOTAL DES CHARGES DE FONCTIONNEMENT = B:\n"
    soup_PRODUITS_FONCTIONNEMENT = soup_finances.find(
        string="TOTAL DES CHARGES DE FONCTIONNEMENT = B").parent
    soup_Infos = soup_PRODUITS_FONCTIONNEMENT.find_previous_siblings()
    print "\t\tEn milliers d'Euros: "+soup_Infos[2].string
    print "\t\tEuros par habitant: "+soup_Infos[1].string
    print "\t\tMoyenne de la strate: "+soup_Infos[0].string
    print
    print "\tRESULTAT COMPTABLE = A - B = R:\n"
    soup_PRODUITS_FONCTIONNEMENT = soup_finances.find(
        string="RESULTAT COMPTABLE = A - B = R").parent
    soup_Infos = soup_PRODUITS_FONCTIONNEMENT.find_previous_siblings()
    print "\t\tEn milliers d'Euros: "+soup_Infos[2].string
    print "\t\tEuros par habitant: "+soup_Infos[1].string
    print "\t\tMoyenne de la strate: "+soup_Infos[0].string

years = range(2010, 2014)
for year in years:
    getStatsByYear(year)
