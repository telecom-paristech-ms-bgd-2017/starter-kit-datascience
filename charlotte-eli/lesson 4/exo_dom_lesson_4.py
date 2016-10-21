import requests
from bs4 import BeautifulSoup
import urllib2
import numpy as np
import pandas as pd
import re
# coding: utf-8

#https://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&q=renault%20zoe

def get_phone(commentaire):
    patterns = ['(\d\d-\d\d-\d\d-\d\d-\d\d)', '(\d\d \d\d \d\d \d\d \d\d)','(\d\d\d\d\d\d\d\d\d\d)'] # on précise exactement ce qu'on souhaite! 
    for pat in patterns:
        if re.findall(pat, commentaire):
            phoneNumRegex = re.compile(pat)
            mo = phoneNumRegex.search(commentaire)
            return str(mo.group()) 
    else:
        return 'phone number unknown'

def findNbPage(lien) :
    r3 = requests.get(lien)
    soup = BeautifulSoup(r3.text, 'html.parser')
    div = soup.find(id="last")
    if div != None:
        textPage = div.get('href')
        numPage = int(textPage.split('?')[1].split('=')[1].split('&')[0])
        return numPage
    else:
        return '1'
    
def get_url(region,page):
    return "https://www.leboncoin.fr/voitures/offres/"+region+"/?th="+str(page) +"&q=Renault%20Zoe&parrot=0"
 

def get_infos(link):
    r_auto = requests.get(link) 
    soup = BeautifulSoup(r_auto.text.encode("utf8").decode('ascii', 'ignore'), 'html.parser')
    title = soup.find('header',{'class':'adview_header clearfix'}).find('h1').text.replace('\t','').replace('\n','')
    prix = soup.find_all('span',{'class':'value'})[0].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','')
    modele = soup.find_all('span',{'class':'value'})[3].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','')  
    year =  soup.find_all('span',{'class':'value'})[4].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','')  
    if (soup.find_all('span',{'class':'value'})[5].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','').replace('KM','') == 'Electrique') or (soup.find_all('span',{'class':'value'})[5].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','').replace('KM','') == 'Automatique '): 
        km = soup.find_all('span',{'class':'value'})[4].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','').replace('KM','')
    else:
        km = soup.find_all('span',{'class':'value'})[5].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','').replace('KM','')
    commentaire = soup.find('div',{'class':'line properties_description'}).text.encode("utf8").decode('ascii', 'ignore')
    if commentaire is not None:
        phone = get_phone(commentaire)    
    else:
        phone = 'phone number unknown'
    #km = soup.find_all('span',{'class':'value'})[5].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','').replace('KM','')
    return title, prix, modele, year, km, phone

def get_price_centrale(version,year):
    url = "http://www.lacentrale.fr/cote-auto-renault-zoe-{}+charge+rapide-{}.html".format(version, year)
    r = requests.get(url) 
    soup = BeautifulSoup(r.text.encode("utf8").decode('ascii', 'ignore'), 'html.parser')
    temp = soup.find('div',{'class':'txtC mT60 f20 flexCont flexCenter'})
    prix = temp.findChildren()[2].text.encode("utf8").decode('ascii', 'ignore').replace('\n','').replace(' ','')
    return str(prix)

links = []
pro_or_not=[]
title=[]
prix=[]
modele=[]
year=[]
km =[]
lieu=[]
phone=[]

regions = ['ile_de_france','provence_alpes_cote_d_azur','aquitaine']
#regions = ['aquitaine']

for region in regions:
    pages = range(1,int(findNbPage(get_url(region,1)))+1)
    for page in pages:
        url = get_url(region,page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text.encode("utf8").decode('ascii', 'ignore'), 'html.parser')
        content = soup.find_all('section', {'class' : "tabsContent block-white dontSwitch"})
        table = content[0].find_all('li')
        for line in table:
            link =  'https:' + line.find('a').get('href')
            temp =  line.find('a').get('data-info')
                
            if get_infos(link)[0].find('zoe')==-1 and get_infos(link)[0].find('Zoe')==-1 and get_infos(link)[0].find('ZOE')==-1:
                pass
            else:
                links.append(link)
                title.append(get_infos(link)[0])
                prix.append(get_infos(link)[1])
                year.append(get_infos(link)[3])
                km.append(get_infos(link)[4])
                phone.append(get_infos(link)[5])
                lieu.append(region)
                if temp[temp.find("ad_offres")+14:temp.find("ad_offres")+17]=='pro':
                    pro_or_not.append('pro')
                else:
                    pro_or_not.append('particulier')

    


# clean data
# modeles : intens, life, zen

cleaned_title = []    

for i in range(len(title)):   
    if (title[i].find('Life')!=-1) or (title[i].find('life')!=-1) or (title[i].find('LIFE')!=-1):
        cleaned_title.append('Renault Zoe Life')
    elif (title[i].find('Intens')!=-1) or (title[i].find('intens')!=-1) or (title[i].find('INTENS')!=-1):
        cleaned_title.append('Renault Zoe Intens')
    else : 
        cleaned_title.append('Renault Zoe Zen')


argus = []

for i in range(len(cleaned_title)):
    if year[i]=='2016':
        argus.append(prix[i])
    else:
        if cleaned_title[i].find('Life')!=-1:
            argus.append(get_price_centrale('life',year[i]))
        elif cleaned_title[i].find('Zen')!=-1:
            argus.append(get_price_centrale('zen',year[i]))
        else:
            argus.append(get_price_centrale('intens',year[i]))
 
        

diff_prix = [int(prix[i])-int(argus[i]) for i in range(len(prix))]

d = {'lien' : links ,'region' : lieu ,'modele' : cleaned_title, 'prix' : prix,'km' : km,'year' : year,'type vendeur' : pro_or_not,'numero' : phone,'argus':argus,'delta prix vs argus' : diff_prix}
results = pd.DataFrame(d,columns=['lien','modele','year','km','region','type vendeur','numero','prix','argus','delta prix vs argus'])

print results

results.to_csv('out.csv', sep=';', encoding='utf-8')




