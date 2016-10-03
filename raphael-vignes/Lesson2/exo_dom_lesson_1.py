#Crawling French cities accounts
import requests
from bs4 import BeautifulSoup
import csv

def extractValueFromSoup(soup,classparent,classchild,positionParent,positionChild):
    result = soup.findAll(class_=classparent)[positionParent].findAll(class_=classchild)[positionChild].text.replace('\xa0','')
    return result

def getAccountsByYear(years,idcommune,dep):
    accounts = []
    for year in years :
        account = {}
        inconnues =[]
        if len(inconnues) > 5 : break
        account_year = requests.get("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom="+idcommune+"&dep="+dep+"&type=BPS&param=5&exercice="+str(year))
        soup_account = BeautifulSoup(account_year.text,'html.parser')
        try :
            account['Id Commune'] = idcommune
            account['dept'] = dep
            account['year'] = year
            account['eurohabA'] = extractValueFromSoup(soup_account,'bleu','montantpetit G',3,1)
            account['moyennestrateA'] = extractValueFromSoup(soup_account,'bleu','montantpetit G',3,2)
            account['eurohabB'] = extractValueFromSoup(soup_account, 'bleu', 'montantpetit G', 7, 1)
            account['moyennestrateB'] = extractValueFromSoup(soup_account, 'bleu', 'montantpetit G', 7, 2)
            account['eurohabC'] = extractValueFromSoup(soup_account, 'bleu', 'montantpetit G', 15, 1)
            account['moyennestrateC'] = extractValueFromSoup(soup_account, 'bleu', 'montantpetit G', 15, 2)
            account['eurohabD'] = extractValueFromSoup(soup_account, 'bleu', 'montantpetit G', 20, 1)
            account['moyennestrateD'] = extractValueFromSoup(soup_account, 'bleu', 'montantpetit G', 20, 2)
            accounts.append(account)
        except :
            print("ID de ville: "+idcommune+" inconnu")
            inconnues.append(idcommune)
    return accounts

def prettyPrintAccounts(accounts):
    for account in accounts:
        print("=====Année: "+str(account.get('year'))+"=====")
        print("Commune: "+account.get('Id Commune'))
        print("Produit de fonctionnement en euro par habitant: "+account.get('eurohabA'))
        print("Produit de fonctionnement en moyenne de la strate: "+account.get('moyennestrateA'))
        print("Charge de fonctionnement en euro par habitant: " + account.get('eurohabB'))
        print("Charge de fonctionnement en moyenne de la strate: " + account.get('moyennestrateB'))
        print("Ressource d'investissement en euro par habitant: " + account.get('eurohabC'))
        print("Ressource d'investissement en moyenne de la strate: " + account.get('moyennestrateC'))
        print("Emploi d'investissement en euro par habitant: " + account.get('eurohabD'))
        print("Emploi d'investissement en moyenne de la strate: " + account.get('moyennestrateD'))
        print("=====FIN=====")


def exportCsv(commune):
    try:
        with open("accounts" + dep+".csv", "a") as f:
            w = csv.DictWriter(f, fieldnames=["Id Commune","dept","year","eurohabA","moyennestrateA","eurohabB", "moyennestrateB", "eurohabC", "moyennestrateC","eurohabD","moyennestrateD"],
                        extrasaction='ignore', delimiter = ';')
            w.writerow(commune)
    except IOError :
        print("I/O error")
    return

#paris = getAccountsByYear([X for X in range(2010,2016)],'056','075')
#prettyPrintAccounts(paris)
#caen = getAccountsByYear([X for X in range(2010,2016)],'118','014')
#prettyPrintAccounts(caen)

idcommunesducalvados = [Y for Y in range(1,764)]
dep = '014'
for id in idcommunesducalvados:
    commune_du_calvados = getAccountsByYear([X for X in range(2015, 2016)], str(id).zfill(3), dep)
    prettyPrintAccounts(commune_du_calvados)
    for commune in commune_du_calvados :
        print(commune)
        exportCsv(commune)



