import requests
from bs4 import BeautifulSoup


#liste des années à traiter
annees_traitees = ['2010','2011','2012','2013','2014','2015']


for annee in annees_traitees:
    #On récupere les données de l'année passée en param
    donneesgouvernement = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+annee)
    soup_gouv = BeautifulSoup(donneesgouvernement.text, 'html.parser')
    res = soup_gouv.find_all('table')

    print('                                               ')
    print('***************ANNEE'+annee+'******************')
    print('                                               ')
    ligne = res[2].find_all(class_ = 'bleu')

    for elem in ligne:

        titre = elem.find_all(class_ = 'libellepetit G')
        if titre:

            libelle = str(titre[0].text)
            #colonne A
            if ("TOTAL DES PRODUITS DE FONCTIONNEMENT = A" == libelle.strip()):
                print('    ***********************************************************')
                #On selectionne les trois premières balise TD du TR
                par_habitant    = elem.select('td:nth-of-type(2)')
                par_strat       = elem.select('td:nth-of-type(3)')
                print(libelle)
                print('    arg par habit: ' + par_habitant[0].text)
                print('    arg par start: ' + par_strat[0].text)
            #colonne B
            if ("TOTAL DES CHARGES DE FONCTIONNEMENT = B" == libelle.strip()):
                print('    ***********************************************************')
                #On selectionne les trois premières balise TD du TR
                par_habitant    = elem.select('td:nth-of-type(2)')
                par_strat       = elem.select('td:nth-of-type(3)')
                print(libelle)
                print('    arg par habit: ' + par_habitant[0].text)
                print('    arg par start: ' + par_strat[0].text)
            #colonne C
            if ("TOTAL DES RESSOURCES D'INVESTISSEMENT = C" == libelle.strip()):
                print('    ***********************************************************')
                #On selectionne les trois premières balise TD du TR
                par_habitant    = elem.select('td:nth-of-type(2)')
                par_strat       = elem.select('td:nth-of-type(3)')
                print(libelle)
                print('    arg par habit: ' + par_habitant[0].text)
                print('    arg par start: ' + par_strat[0].text)
            #colonne D
            if ("TOTAL DES EMPLOIS D'INVESTISSEMENT = D" == libelle.strip()):
                print('    ***********************************************************')
                #On selectionne la deuxiemme  premières balise TD du TR
                par_habitant    = elem.select('td:nth-of-type(2)')
                par_strat       = elem.select('td:nth-of-type(3)')
                print(libelle)
                print('    arg par habit: ' + par_habitant[0].text)
                print('    arg par start: ' + par_strat[0].text)