import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#result = requests.get('http://www.cdiscount.com/search/10/ordinateur.html#_his__')
def getSoup(url) :
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pc = soup.find_all(class_='prdtBloc')
    return pc

def getReductions(url):
    pc = getSoup(url)
    marques = []
    prix_org = []
    prix_red = []
    for i in range(1, len(pc)):
        prix_origin = pc[i].find(class_="prdtPrSt")
        if prix_origin :
            prix_origin = prix_origin.text.replace(u'\xa0', '')
            prix_origin = prix_origin.replace(',', '.')
            if prix_origin :
                prix_reduit = pc[i].find(class_="price").text.replace(u'\xa0', '')
                prix_reduit = prix_reduit.replace('€', '.')
                prix_reduit = float(prix_reduit)
                prix_org.append(float(prix_origin))
                prix_red.append(prix_reduit)
                all_marque = pc[i].find(class_='prdtBTit')
                marque = all_marque.text.replace(u'\xa0', '')
                marques.append(marque)
        df_marque = pd.DataFrame(marques, columns=['Marques'])
    reductions_origin = pd.DataFrame(prix_org, columns=['Prix_Origine'])
    reductions_reduit = pd.DataFrame(prix_red, columns=['Prix_Réduit'])
    reductions_dataFrame = df_marque.join(reductions_origin)
    reductions_dataFrame = reductions_dataFrame.join(reductions_reduit)


    return reductions_dataFrame


def getcompare(marque1, marque2, url) :
    reductions_dataFrame = getReductions(url)
    liste_marque = reductions_dataFrame['Marques']
    df1 = reductions_dataFrame.copy()
    df2 = reductions_dataFrame.copy()

    df1['marque'] = df1.loc[df1['Marques'].str.contains(marque1), 'test'] = marque1
    df2['marque'] = df2.loc[df2['Marques'].str.contains(marque2), 'test'] = marque2
    df1 = df1.dropna(axis=0)
    df2 = df2.dropna(axis=0)
    df1 =  df1.drop('test', axis =1)
    df2 =  df2.drop('test', axis =1)
    df1['Reduction'] = ((df1['Prix_Origine'] - df1['Prix_Réduit'])/df1['Prix_Origine'])*100
    df2['Reduction'] = ((df2['Prix_Origine'] - df2['Prix_Réduit']) / df2['Prix_Origine'])*100


    print('Première Marque : '+ marque1)
    print(df1)

    print('Seconde Marque : '+ marque2)
    print(df2)
    return

for i in (range(1,5)):
    print(2*'------------------', 'Page' , i, 2*'------------------')
    getcompare('LENOVO', 'HP', 'http://www.cdiscount.com/search/10/ordinateur.html?page='+str(i)+'#_his__')


