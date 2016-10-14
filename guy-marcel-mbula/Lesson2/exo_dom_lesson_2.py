# 1. les librairies utilies

import requests
from bs4 import BeautifulSoup


def extractDataFrom(url, annee):
    result = requests.get(url + str(annee))
    soup = BeautifulSoup(result.text, 'html.parser')
    test = soup.find_all(class_="bleu")
    if len(test)<=3 :
        print("------", annee, "------")
        print("No data for this year")
        return
    else :

        A_1 = soup.find_all(class_="bleu")[3].find_all(class_="montantpetit G")[1].text.replace(u'\xa0', '')
        A_2 = soup.find_all(class_="bleu")[3].find_all(class_="montantpetit G")[2].text.replace(u'\xa0', '')
        A_1 = int(A_1.replace(" ", ""))
        A_2 = int(A_2.replace(" ", ""))

        B_1 = soup.find_all(class_="bleu")[7].find_all(class_="montantpetit G")[1].text.replace(u'\xa0', '')
        B_2 = soup.find_all(class_="bleu")[7].find_all(class_="montantpetit G")[2].text.replace(u'\xa0', '')
        B_1 = int(B_1.replace(" ", ""))
        B_2 = int(B_2.replace(" ", ""))

        C_1 = soup.find_all(class_="bleu")[15].find_all(class_="montantpetit G")[1].text.replace(u'\xa0', '')
        C_2 = soup.find_all(class_="bleu")[15].find_all(class_="montantpetit G")[2].text.replace(u'\xa0', '')
        C_1 = int(C_1.replace(" ", ""))
        C_2 = int(C_2.replace(" ", ""))

        D_1 = soup.find_all(class_="bleu")[20].find_all(class_="montantpetit G")[1].text.replace(u'\xa0', '')
        D_2 = soup.find_all(class_="bleu")[20].find_all(class_="montantpetit G")[2].text.replace(u'\xa0', '')
        D_1 = int(D_1.replace(" ", ""))
        D_2 = int(D_2.replace(" ", ""))

        print("------", annee,"------" )
        print('A_euros_par_habitant : ', A_1)
        print('A_moyenne_de_la_strate :', A_2)
        print('B_euros_par_habitant : ',B_1)
        print('B_moyenne_de_la_strate : ',B_2)
        print('C_euros_par_habitant : ',C_1)
        print('C_moyenne_de_la_strate : ', C_2)
        print('D_euros_par_habitant : ', D_1)
        print('D_moyenne_de_la_strate : ', D_2)

        data = {}
        data['A_euros_par_habitant'] = A_1
        data['A_moyenne_de_la_strate'] = A_2
        data['B_euros_par_habitant'] = B_1
        data['B_moyenne_de_la_strate'] = B_2
        data['C_euros_par_habitant'] = C_1
        data['C_moyenne_de_la_strate'] = C_2
        data['D_euros_par_habitant'] = D_1
        data['D_moyenne_de_la_strate'] = D_2
    return data



def storeData(debut):
    for annee in range(debut,2014):

        all_data=[]
        data=extractDataFrom('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=',str(annee))
        all_data.append(data)

    return all_data
storeData(2009)






