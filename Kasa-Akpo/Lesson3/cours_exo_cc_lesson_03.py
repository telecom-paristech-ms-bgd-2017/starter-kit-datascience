import requests
from bs4 import BeautifulSoup
import sys

###Acer
result = requests.get('http://www.cdiscount.com/search/10/ordinateur+acer.html#_his_')
soup = BeautifulSoup(result.text, 'html.parser')
prix_acer = []
prix_acer = soup.find_all(class_='prdtBZPrice')
prix = []
rabais = []
taux_remise = []
montant = []

### Dell
result_1 = requests.get('http://www.cdiscount.com/search/10/ordinateur+dell.html#_his_')
soup_1 = BeautifulSoup(result_1.text, 'html.parser')
prix_dell = []
prix_dell = soup.find_all(class_='prdtBZPrice')
prix_1 = []
rabais_1 = []
taux_remise_1 = []
montant_1 = []

### Acer
for i in range(len(prix_acer)):
    prix = prix_acer[i].get_text()
    if(len(prix) > 5):
        for elt in prix:
            if elt == ')':
                indice = prix.index(')')
                indice+=1   
                prix = prix[indice:] 
                for elt in prix:
                    if elt == ',':
                        indice = prix.index(',')
                        prix_initial = prix[0:indice]
                        if prix[indice + 1] == '0':                            
                            #print('Prix sur site', prix_acer[i].get_text())
                            #print('prix initial',prix_initial)
                            prix_rabais = prix[indice+1:len(prix)]
                            prix_rabais = prix_rabais.replace("€",".")
                            #print('Prix rabais',prix_rabais)
                            taux_remise = (float(prix_initial) - float(prix_rabais)) / float(prix_initial) * 100
                            montant.append(taux_remise)
                        elif prix[indice + 1] != '0':
                            reste = prix[indice+1 : indice +3]
                            prix_initial = prix[0:indice] + '.' + reste
                            #print('Le chiffre avec virgule:', prix_initial)
                            prix_rabais = prix[indice+4: len(prix)]
                            prix_rabais = prix_rabais.replace("€",".")
                            #print('prix rabais avec virgule:', prix_rabais)
                            taux_remise = (float(prix_initial) - float(prix_rabais)) / float(prix_initial) * 100
                            montant.append(taux_remise)

### Dell
for i in range(len(prix_dell)):
    prix_1 = prix_dell[i].get_text()
    if(len(prix_1) > 5):
        for elt in prix_1:
            if elt == ')':
                indice = prix_1.index(')')
                indice+=1   
                prix_1 = prix_1[indice:] 
                for elt in prix_1:
                    if elt == ',':
                        indice = prix_1.index(',')
                        prix_initial_1 = prix_1[0:indice]
                        if prix_1[indice + 1] == '0':                            
                            #print('Prix sur site', prix_acer[i].get_text())
                            #print('prix initial',prix_initial)
                            prix_rabais_1 = prix_1[indice+1:len(prix_1)]
                            prix_rabais_1 = prix_rabais_1.replace("€",".")
                            #print('Prix rabais',prix_rabais)
                            taux_remise_1 = (float(prix_initial_1) - float(prix_rabais_1)) / float(prix_initial_1) * 100
                            montant_1.append(taux_remise_1)
                        elif prix_1[indice + 1] != '0':
                            reste_1 = prix_1[indice+1 : indice +3]
                            prix_initial_1 = prix_1[0:indice] + '.' + reste_1
                            #print('Le chiffre avec virgule:', prix_initial)
                            prix_rabais_1 = prix_1[indice+4: len(prix_1)]
                            prix_rabais_1 = prix_rabais_1.replace("€",".")
                            #print('prix rabais avec virgule:', prix_rabais)
                            taux_remise_1 = (float(prix_initial_1) - float(prix_rabais_1)) / float(prix_initial_1) * 100
                            montant_1.append(taux_remise_1)                            

### Acer
remise = 0          
for elt in montant:
    remise = remise + elt;
    remise_acer = remise / len(montant)
print('Remise sur Acer:' +str(remise_acer))                            
###Dell
remise_1 = 0          
for elt in montant:
    remise_1 = remise + elt;
    remise_dell = remise_1 / len(montant)
print('Remise sur Dell:' +str(remise_dell))                            
