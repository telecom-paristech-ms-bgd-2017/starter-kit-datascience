import requests
from bs4 import BeautifulSoup

for year in range(2010, 2016):
    req = requests.get("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(year))

    soup = BeautifulSoup(req.text,'html.parser')

    lignes = soup.find_all(class_ = 'bleu')

    print("Resultats des comptes de la ville de Paris de l'annee : " + str(year))

    for ligne in lignes:
        title_gen = (ligne.find_all(class_ = 'libellepetit G'))
        if title_gen:
            title = title_gen[0].text
            if title == "TOTAL DES PRODUITS DE FONCTIONNEMENT = A":
                per_habitant = ligne.select('td:nth-of-type(2)')[0].text.replace(u'\xa0','')
                mean_strat = ligne.select('td:nth-of-type(3)')[0].text.replace(u'\xa0','')

                print( "******************* TOTAL DES PRODUITS DE FONCTIONNEMENT = A")
                print("Moyenne par habitant :" + str(per_habitant))
                print("Moyenne de la strat :" + str(mean_strat))

            if title == "TOTAL DES CHARGES DE FONCTIONNEMENT = B":
                per_habitant = ligne.select('td:nth-of-type(2)')[0].text.replace(u'\xa0','')
                mean_strat = ligne.select('td:nth-of-type(3)')[0].text.replace(u'\xa0','')

                print( "******************* TOTAL DES CHARGES DE FONCTIONNEMENT = B")
                print("Moyenne par habitant :" + str(per_habitant))
                print("Moyenne de la strat :" + str(mean_strat))

            if title == "TOTAL DES RESSOURCES D'INVESTISSEMENT = C":
                per_habitant = ligne.select('td:nth-of-type(2)')[0].text.replace(u'\xa0','')
                mean_strat = ligne.select('td:nth-of-type(3)')[0].text.replace(u'\xa0','')

                print( "******************* TOTAL DES RESSOURCES D'INVESTISSEMENT = C")
                print("Moyenne par habitant :" + str(per_habitant))
                print("Moyenne de la strat :" + str(mean_strat))

            if title == "TOTAL DES EMPLOIS D'INVESTISSEMENT = D":
                per_habitant = ligne.select('td:nth-of-type(2)')[0].text.replace(u'\xa0','')
                mean_strat = ligne.select('td:nth-of-type(3)')[0].text.replace(u'\xa0','')

                print( "******************* TOTAL DES EMPLOIS D'INVESTISSEMENT = D")
                print("Moyenne par habitant :" + str(per_habitant))
                print("Moyenne de la strat :" + str(mean_strat))

    print("\n\n\n")
