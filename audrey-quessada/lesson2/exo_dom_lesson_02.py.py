#Créé le 05/10/2016
#Version Python 3
#Pb pour comprendre les notions parent, enfant, node dans le contexte d'utilisation dans le programme:
#comment les implémente-t'on?: exemples sur internet pas suffisants
#Du coup, j'ai fait à ma maniere (pour récupérer les bons indices), c'est pas propre mais ça marche
#Pb pour tester si la page est blanche ou non (par exemple pour Paris en 2009, comment tester?)
#@author: audrey quessada

import requests
from bs4 import BeautifulSoup

#définir le nom de la classe
def get_the_class_name(classname):
    new_classname = classname + 'petit G'
    return new_classname

#en fonction du nom de la classe, récuperer les resultats de la page web
def get_the_result(soup, classname, position):
    new_classname = get_the_class_name(classname)
    if new_classname == 'libellepetit G':
        resultat = soup.find_all(class_=new_classname)[position].text.replace('<td class="'
                                                                              + new_classname + '">', '').replace('</td>','')
    elif new_classname == 'montantpetit G':
        resultat = soup.find_all(class_=new_classname)[position].text.replace('<td class="'
                                                                              + new_classname + '">','').replace('\xa0','').replace('</td>', '')
    return resultat

#récupérer la 2ème et 3ème colonne de la classe montantpetit G
def func_loop_class(soup, classname):
    liste_bilan = []
    el1 = str(get_the_result(soup,classname, 1))
    el2 = str(get_the_result(soup, classname, 2))
    liste_bilan.append(el1)
    liste_bilan.append(el2)
    el3 = str(get_the_result(soup, classname, 4))
    el4 = str(get_the_result(soup, classname, 5))
    liste_bilan.append(el3)
    liste_bilan.append(el4)
    el5 = str(get_the_result(soup, classname, 10))
    el6 = str(get_the_result(soup, classname, 11))
    liste_bilan.append(el5)
    liste_bilan.append(el6)
    el7 = str(get_the_result(soup, classname, 13))
    el8 = str(get_the_result(soup, classname, 14))
    liste_bilan.append(el7)
    liste_bilan.append(el8)
    return liste_bilan

#récupérer le numéro de département
def get_the_dpt(soup):
    dpt = soup.find(class_='libellepetit').text.replace('DEPARTEMENT : ', '')
    return dpt

#récupérer le nom de la ville classname 'G'
def get_the_city(soup):
    city = soup.find_all(class_='G')[1].text
    return city

#récupérer l'année du bilan financier
def get_the_year(soup):
    year = soup.find(class_="bleu G").text.replace('ANALYSE DES EQUILIBRES FINANCIERS FONDAMENTAUX', '').split('\n')
    return str(year[1])

#lire les url pour n'importe quel dpt et n'importe quelle annee
def read_url(annee,dpt,num_com):
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' +\
          num_com +'&dep=' + dpt + '&type=BPS&param=5&exercice=' + annee
    site_web = requests.get(url)
    soup = BeautifulSoup(site_web.text, 'html.parser')
    return soup

#Mise en forme du résultat
def shape_the_result(soup):
    #récupérer le titre, le nom du département et le nom de la ville
    title = soup.title.text
    city = get_the_city(soup)
    year = get_the_year(soup)
    dpt = get_the_dpt(soup)

    #création d'un dictionnaire pour stocker les résultats
    bilan_financier = {}
    bilan_financier['Année'] = year
    bilan_financier['Département'] = dpt
    bilan_financier['Ville'] = city
    bilan_financier['A_habitant'] = func_loop_class(soup, 'montant')[0]
    bilan_financier['A_strate'] = func_loop_class(soup, 'montant')[1]
    bilan_financier['B_habitant'] = func_loop_class(soup, 'montant')[2]
    bilan_financier['B_strate'] = func_loop_class(soup, 'montant')[3]
    bilan_financier['C_habitant'] = func_loop_class(soup, 'montant')[4]
    bilan_financier['C_strate'] = func_loop_class(soup, 'montant')[5]
    bilan_financier['D_habitant'] = func_loop_class(soup, 'montant')[6]
    bilan_financier['D_strate'] = func_loop_class(soup, 'montant')[7]

    #print le résultat
    print(title)
    print('================')
    print('Pour la ville de ' + city + ' dans le ' + dpt + ' en ' + year)
    print(str(get_the_result(soup,'libelle',0)) + ' est ' + str(
        func_loop_class(soup, 'montant')[0]) + ' en euros par habitant')
    print(str(get_the_result(soup, 'libelle', 0)) + ' est ' + str(
        func_loop_class(soup, 'montant')[1]) + ' en euros en moyenne de la strate')
    print(str(get_the_result(soup, 'libelle', 1)) + ' est ' + str(
        func_loop_class(soup, 'montant')[2]) + ' en euros par habitant')
    print(str(get_the_result(soup, 'libelle', 1)) + ' est ' + str(
        func_loop_class(soup, 'montant')[3]) + ' en euros en moyenne de la strate')
    print(str(get_the_result(soup, 'libelle', 3)) + ' est ' + str(
        func_loop_class(soup, 'montant')[4]) + ' en euros par habitant')
    print(str(get_the_result(soup, 'libelle', 3)) + ' est ' + str(
        func_loop_class(soup, 'montant')[5]) + ' en euros en moyenne de la strate')
    print(str(get_the_result(soup, 'libelle', 4)) + ' est ' + str(
        func_loop_class(soup, 'montant')[6]) + ' en euros par habitant')
    print(str(get_the_result(soup, 'libelle', 4)) + ' est ' + str(
        func_loop_class(soup, 'montant')[7]) + ' en euros en moyenne de la strate')
    print('================')
    return bilan_financier

#donner les résultats sur plusieurs années pour la même ville
#faudrait un moyen de tester si la page a des data sans qu'on ait un message d'erreur
def get_the_result_all_year(dpt, num_com, MIN, MAX):
    for i in range(MIN, MAX+1):
        if i < 10:
            year = '200' + str(i)
            soup = read_url(year, dpt, num_com)
            res = shape_the_result(soup)
        else:
            year = '20'+str(i)
            soup = read_url(year, dpt, num_com)
            res =shape_the_result(soup)
    return res

#donner les résultats pour toutes les villes d'un même département pour la même année
def get_the_result_all_dpt(year, dpt, MIN, MAX):
    # il faudrait tester si la commune existe
    for i in range(MIN, MAX+1):
        if i < 10:
            num_com = '00'+str(i)
            soup = read_url(year, dpt, num_com)
            res = shape_the_result(soup)
        elif i in (10, 100):
            num_com = '0' + str(i)
            soup = read_url(year, dpt, num_com)
            res = shape_the_result(soup)
        else:
            num_com = str(i)
            soup = read_url(year, dpt, num_com)
            res = shape_the_result(soup)
    return res

#tester si la commune existe
get_the_result_all_year('075', '056', 10, 15)
get_the_result_all_dpt('2013', '014', 1, 9)

