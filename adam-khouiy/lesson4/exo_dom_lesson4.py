import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.leboncoin.fr/voitures/offres/{}/?o={}&q=renault%20zo%E9&it=1&f={}"

#reccuperer l id de l'annonce
#essayer les try except


def list_renault_zoe_bon_coin(region, page, proprietere):
    resultat = requests.get(url.format(region, str(page), proprietere))
    html = resultat.content
    soup = BeautifulSoup(html, 'lxml')
    url_list = []
    for element  in  soup.findAll('section', attrs={'class': 'tabsContent block-white dontSwitch'}):
        for lien in element.find_all('a', href=True):
            url_list.append("https:"+lien['href'])


    return url_list,proprietere

#list_renault_zoé_bon_coin("ile_de_france", "1", "c")


list_url ,proprietere = list_renault_zoe_bon_coin("ile_de_france", "1", "c")
#url_list =["https://www.leboncoin.fr/voitures/1035061660.htm?ca=12_s"]

def detail_voiture (list_url,proprietere):
     df =pd.DataFrame()
     if proprietere == "c":
         proprietere ="Professionnel"
     else :
         proprietere= "Particulier"
     for lien in list_url:
          resultat1 = requests.get(lien)
          soup = BeautifulSoup(resultat1.content, 'lxml')
          list_detail = soup.find_all('h2' ,attrs={'class':'clearfix'})
          #list_detail = soup.select("#adview ")
          list_propriet= []
          for detail in list_detail:
              detail =soup.find_all("span",attrs={'class':'value'})
              title =soup.find("h1",attrs={'class':'no-border'}).text.lower()
              description = soup.find("div" ,attrs={'class':'line properties_description'}).findChildren('p')[1].text
              telephone = re.search(r'(\d{10})',description)


              #if re.search('(ZEN|INTENS|LIFE) *(TYPE *2)?',description.upper()):
                  #version = description.group(0)


              if re.search("zen",title):
                  version= "zoe zen"
              elif re.search("intens",title):
                  version = "zoe intens"
              elif re.search("life",title):
                  version ="zoe life"
              else :
                  version ="NA"


              prix =detail[0].text.replace(' ','').replace(u'\n','').replace(u'\t','').replace(u'\xa0','').replace('€','')
              annee = detail[4].text.replace(' ','').replace(u'\n','').replace(u'\t','').replace(u'\xa0','')
              kilometrage = detail[5].text.replace(' ','').replace(u'\n','').replace(u'\t','').replace(u'\xa0','').replace('KM','')

          df = df.append({"prix" : prix, "annee" : annee, "kilométrage" : kilometrage ,"proprietaire" :proprietere,"version" :version,"telephone" :("NA" if telephone == None  else telephone.group(0))},ignore_index=True)

     return df
#print (detail_voiture (list_url,'p'))

df = detail_voiture (list_url,'p')


def recherche_central(df):
    df['version'] = df['version'].str.replace(' ','-')
    annees = df.annee
    versions = df['version']
    price_argus = pd.DataFrame()

    for annee , version in zip(annees,versions):

        if annee == 2016:
             url ="http://www.lacentrale.fr/cote-auto-renault-"+version.lower()+"+charge+rapide+type+2-"+str(annee)+".html"
        else :
             url ="http://www.lacentrale.fr/cote-auto-renault-"+version.lower()+"-"+str(annee)+".html"

        resultat = requests.get(url)
        soup = BeautifulSoup(resultat.text, 'html.parser')

        element_price = soup.find('strong', attrs={'class': 'f24 bGrey9L txtRed pL15 mL15'})
        if element_price is not None:
            price = element_price.text.replace(u'\n', '').replace(u'\t', '').replace(u'\xa0', '').replace('€', '').replace(' ','')
        else :
            price ="NA"

            price_argus = price_argus.append({"price argus": price},ignore_index=True)





    return pd.concat([df, price_argus], axis=1)




print(recherche_central(detail_voiture (list_url,'p')))






