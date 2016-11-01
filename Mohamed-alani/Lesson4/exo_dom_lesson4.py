import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URLBASE = "https://www.leboncoin.fr/voitures/offres/"
URLLACENTRALE = "http://www.lacentrale.fr/cote-auto-renault-zoe-"


def getCarsInfo(region, pages):

    df = pd.DataFrame(columns = ["price","year","km","num", "pro", "argus", "version"])
    dico = {"life"}
    URLregion = URLBASE+region+"/?o="

    typeZoe = ["intens", "life", "zen"]

    price = []
    km = []
    year = []
    pro = []
    num = []
    argus = []
    version = []

    for page in range(pages):
        resultats = requests.get(URLregion+str(page)+"&q=Renault%20Zo%E9")
        soup_voiture = BeautifulSoup(resultats.text, 'html.parser')
        voitures = soup_voiture.main.findAll("li")

        for voiture in voitures:
            try :
                voitureDetailURL = voiture.findAll('a', href=True)[0]['href']

                resultats = requests.get("https:"+voitureDetailURL)
                soup_voitureDetail = BeautifulSoup(resultats.text, 'html.parser')

                if(voiture.find("span", {"class": "ispro"}) == None):
                    pro.append(0)
                else :
                    pro.append(1)
                price.append((float(soup_voitureDetail.findAll("span", {"class" : "value"})[0].text.replace(" ","").strip()[:-2])))
                year.append(int(soup_voitureDetail.findAll("span", {"class" : "value"})[4].text.replace(" ","").strip()))
                km.append(float(soup_voitureDetail.findAll("span", {"class" : "value"})[5].text.replace(" ","").strip()[:-2]))

                description = soup_voitureDetail.findAll("p", {"itemprop" : "description"})[0].text
                if(re.search('[0-9]{10}', description) == None):
                    num.append("")
                else:
                    num.append(re.search('[0-9]{10}', description).group(0))

                urlArgus = URLLACENTRALE
                m = re.search('zen|life|intens', description.lower())
                if(m != None):
                    m2 = m.group(0).strip()
                    urlArgus = urlArgus + m2
                    m = re.search('charge\srapide', description.lower())
                    version.append(m2)

                    if (m !=None):
                        urlArgus =  urlArgus + "+charge+rapide"

                    m = re.search('type\s1|type\s2', description.lower())
                    if(m != None):
                        urlArgus = urlArgus +"+"+ m.group(0).replace(" ","+")
                    urlArgus = urlArgus+"-"+str(year[-1])+".html"
                else :
                    urlArgus = urlArgus +"life+charge+rapide+type+2-"+str(year[-1])+".html"
                    version.append("NA")

                try:
                    resultats = requests.get(urlArgus)
                    soup_argus = BeautifulSoup(resultats.text, 'html.parser')
                    argus.append(float(soup_argus.find("strong",{"class":"f24 bGrey9L txtRed pL15 mL15"}).text.replace(" ","").strip()[:-1]))
                except Exception as e:
                    argus.append("NA")
            except Exception as e:
                continue

    df["price"] = price
    df["pro"] = pro
    df["year"] = year
    df["km"] = km
    df["num"] = num
    df["argus"] = argus
    df["version"] = version

    return df


# soup_voiture = BeautifulSoup(requests.get("https://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&q=Renault%20Zo%E9").text, 'html.parser')
#
# print(soup_voiture.main.findAll("li")[0].find("h3", {"class": "item_price"}).text.replace(" ","")[:-4])
# #print("(pro)"==soup_voiture.main.findAll("li")[0].find("span", {"class": "ispro"}).text)
# a = (soup_voiture.main.findAll("li")[1].find("h2", {"class":"item_title"}).text.strip().lower())
# print(re.search("zoe", a).group(0))
# test = (BeautifulSoup(requests.get("https:"+soup_voiture.main.findAll("li")[0].\
# findAll('a', href=True)[0]['href']).text, 'html.parser'))

#print( BeautifulSoup(requests.get("https:"+soup_voiture.main.findAll("li")[0].findAll("h2", {"class":"item_title"})[0].text.strip())))

# description = test.findAll("p", {"itemprop" : "description"})[0].text
# m = re.search('[0-9]{10}', description)
# print(m.group(0))

print(getCarsInfo("ile_de_france", 2))
print(getCarsInfo("provence_alpes_cote_d_azur", 2))
print(getCarsInfo("aquitaine", 2))
