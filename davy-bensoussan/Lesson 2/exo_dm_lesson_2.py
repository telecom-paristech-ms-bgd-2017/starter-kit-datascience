import requests
from bs4 import BeautifulSoup


def getMetrics(commune, dep, annee):
    if get_url(commune, dep, annee) == 'erreur':
        return ("Erreur sur les paramètres : la commune et le département doivent être sur 3 chiffres \
        (ex: pour Paris le département est 075) et l'année est au format 20XX")

    soup = BeautifulSoup(requests.get(get_url(commune, dep, annee)).text, 'html.parser')
    hab = []
    strate = []
    info = []
    info.append(soup.select(css_req(2, 1))[0].text)  # département
    info.append(soup.select(css_req(2, 2))[0].text)  # commune
    info.append(soup.select(css_req(1, 3))[0].text)  # année de l'exercice

    for i in [8, 12, 20, 25]:  # numéros des lignes du tableau qui nous intéressent
        buff1 = soup.select(css_req(i, 2))  # colonne euros par habitant
        hab.append(int(buff1[0].text.replace(u'\xa0', '').replace(' ', '')))
        buff2 = soup.select(css_req(i, 3))  # colonne moyenne de la strate
        strate.append(int(buff2[0].text.replace(u'\xa0', '').replace(' ', '')))
    return [info, hab, strate]


def css_req(tr, td):  # pour condenser l'écriture du css selector
    return "table:nth-of-type(3) tr:nth-of-type(" + str(tr) + ") " + "td:nth-of-type(" + str(td) + ")"


def get_url(commune, dep, annee):
    if len(str(commune)) != 3 or len(str(dep)) != 3 or len(str(annee)) != 4:
        return 'erreur'
    else:
        return 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' + str(commune) + '&dep=' + str(dep) + '&type=BPS&exercice=' + str(annee)


def printMetrics(commune, dep, annee):  # affiche de façon lisible le résultat de getMetrics
    m = getMetrics(commune, dep, annee)
    print(", ".join(m[0]))
    print("Euros par habitant (catégories A, B, C, D) : " + ", ".join([str(m) for m in m[1]]))
    print("Moyenne de la strate (catégories A, B, C, D) : " + ", ".join([str(m) for m in m[2]]))


def printCommunes(departement, annee, first_com=1, last_com=1000):
    count = 0
    errno = 0
    dep = (2 * '0' + str(departement))[-3:]  # on convertit au format 00X
    for i in range(first_com, last_com + 1):
        try:
            com = (2 * '0' + str(i))[-3:]
            print(str(i) + " ==================================")
            printMetrics(com, dep, annee)
            count += 1
            errno = 0
        except:
            print('Commune introuvable')
            errno += 1
            if errno > 9:  # si 10 codes de communes d'affilée n'existent pas on arrête l'exécution
                break
    print('')
    print(str(count) + ' communes analysées dans le département ' + str(int(dep)) + " pour l'année " + str(annee))
    return


def printAnnees(commune, departement, start_year=2015):
    count = 0
    errno = 0
    com = (2 * '0' + str(commune))[-3:]  # on convertit au format 00X
    dep = (2 * '0' + str(departement))[-3:]  # on convertit au format 00X

    for i in range(start_year, 2000, -1):
        try:
            print(str(i) + " ==================================")
            printMetrics(com, dep, i)
            count += 1
            errno = 0
        except:
            print('Exercice introuvable')
            errno += 1
            if errno > 1:  # si 2 exercices d'affilée n'existent pas on arrête l'exécution
                break
    print('')
    print(str(count) + ' exercices analysés')
    return

printCommunes(76, 2014, 80, 90) # boucle sur les communes du 76 entre les numéros 80 et 90, pour l'année 2014
print('')
printAnnees(56, 75, 2015)  # boucle sur les exercices 2015 et antérieurs de la commune 56 du département 75