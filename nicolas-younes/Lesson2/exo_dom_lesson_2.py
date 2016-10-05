import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurlparis = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
baseurl = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom="
urldep = "&dep="
urlexercice = "&type=BPS&param=5&exercice="


years = [2010, 2011, 2012, 2013, 2014, 2015]
lines = [3, 7, 15, 20]
position_total = 1
position_moyenne = 2

result = requests.get(baseurlparis)
soup = BeautifulSoup(result.text, 'html.parser')


def get_string_from_int(i):
    s = ""
    if i < 10:
        s = "00" + str(i)
    else:
        if i < 100:
            s = "0" + str(i)
        else:
            s = str(i)
    return s


def printdico(dico):
    print(dico["Date"])
    print(dico["A"])
    print(dico["B"])
    print(dico["C"])
    print(dico["D"])
    print("\n")


def get_datas_from_lines_and_position(soup, lines, position):
    results = {}
    produit_fonctionnement = soup.find_all(class_="bleu")[lines[0]].find_all(class_="montantpetit G")[position].text.replace(u'\xa0', '')
    results["A"] = produit_fonctionnement
    charge_fonctionnement = soup.find_all(class_="bleu")[lines[1]].find_all(class_="montantpetit G")[position].text.replace(u'\xa0', '')
    results["B"] = charge_fonctionnement
    ressource_investissement = soup.find_all(class_="bleu")[lines[2]].find_all(class_="montantpetit G")[position].text.replace(u'\xa0', '')
    results["C"] = ressource_investissement
    emploi_investisstement = soup.find_all(class_="bleu")[lines[3]].find_all(class_="montantpetit G")[position].text.replace(u'\xa0', '')
    results["D"] = emploi_investisstement
    return results


def get_datas_for_years(url, years, lines, position):
    resultsperyear = []
    for d in years:
        finalurl = url + str(d)
        results_from_request = requests.get(finalurl)
        soup = BeautifulSoup(results_from_request.text, 'html.parser')
        datas_for_year_d = get_datas_from_lines_and_position(soup, lines, position)
        datas_for_year_d["Date"] = str(d)
        resultsperyear.append(datas_for_year_d)
        print(datas_for_year_d)
    return resultsperyear


def get_datas_for_years_for_dep(dep, years, lines, position):
    n = 2000
    i = 1
    resultsfordep = []
    while i < n:
        finalurl = baseurl + get_string_from_int(i) + urldep + "0" + str(dep) + urlexercice
        try:
            resultsfordep.append(get_datas_for_years(finalurl, years, lines, position))
            #produit_fonctionnement = soup.find_all(class_="bleu")[3].find_all(class_="montantpetit G")[1].text.replace(
            #    u'\xa0', '')
        except IndexError:
            print("no city at this url")
        i += 1
        if i == 10:
            i = i + 1
    return resultsfordep


print("Legend : ")
print("A : Total des produits "
      "de fonctionnement")
print("B : Total des charges de fonctionnement")
print("C : Total des ressources d'investissement")
print("D : Total des emplois d'investissement")
print("\n")

#test = get_datas_for_years(baseurlparis, years, lines, position_moyenne)

test2 = get_datas_for_years_for_dep(14, years, lines, position_moyenne)
print(len(test2))

