import requests
from bs4 import BeautifulSoup





def getInfostrateParis (param):
    resultat =requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(param))
    soup = BeautifulSoup(resultat.text, 'html.parser')
    list_resultat =soup.find_all(class_='libellepetit G')
    list_resultat_ABCD=list_resultat[0:2]+list_resultat[3:5]

    print("Donneés relatives à l'année: ", param)
    for resultat in list_resultat_ABCD :
        parent_resutat = resultat.find_parent("tr")
        euro_par_habitat= parent_resutat.find_all(class_='montantpetit')[1]
        moyenne_de_la_strat= parent_resutat.find_all(class_='montantpetit')[2]
        label = parent_resutat.find_all(class_='montantpetit')[3]

        print("label", resultat.text)
        print("   euro_par_habitat :", euro_par_habitat.text)
        print("   moyenne_de_la_strat :", moyenne_de_la_strat.text)
    print("******************************")


list=[2009,2010,2011,2012,2013]
for year in list:
    getInfostrateParis(year)

""""
label =resultat.text

print("label",label)
print("euro_par_habitat :",euro_par_habitat.text)
print("moyenne_de_la_strat :",moyenne_de_la_strat.text)
#print ("parent_resutat",parent_resutat)
#print("euro_par_habitat",euro_par_habitat)

#print(resultat)
#print(parent_resutat)
#print(type(parent_resutat))

"""




