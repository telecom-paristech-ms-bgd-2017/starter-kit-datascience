from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import html2

regions = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']

def search_argus(modele, year):
    url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + modele + '+charge+rapide-' + year + '.html'
    answer = requests.get(url)
    soup = BeautifulSoup(answer.text)

    argus = int(soup.find('span', class_='Result_Cote').get_text()[:-2].replace(" ", ""))
    
    return argus


def scrap_annonce(url):
    answer = requests.get(url)
    soup = BeautifulSoup(answer.text)

    price = float(soup.find('span', class_='price').get('content'))
    print('price', price)
    
    text = soup.find('div', itemprop='description').get_text()
    reg = "(0[1-9][0-9]{8}|0[1-9]([ .-/][0-9]{2}){4}|0[1-9](.[0-9]{2}){4})"
    regex = "(0[1-9]([ .-/]?[0-9]{2}){4})"

    try:
        tel = max(re.findall(regex, text)[0]).replace(" ", "").replace(".", "")
        print(re.findall(regex, text))
    except IndexError:
        tel = '...'

    print('tel', tel)

    year = int(soup.find('td', itemprop='releaseDate').get_text())
    print('year', year)

    table = soup.select('.criterias table')[0].findAll('tr') 
    km = int(table[2].select('td')[0].get_text()[:-3].replace(" ", ""))
    print('km', km)

    return year, km, price, tel


def scrap(regions):
    columns = ['region', 'model', 'km', 'prix', 'tel', 'argus']
    models = ['zen', 'life', 'intens']
    data = pd.DataFrame(columns=columns)

    for region in regions:
        url = "https://www.leboncoin.fr/voitures/offres/" + region + "/?q=renault%20zo%E9&f="
        answer = requests.get(url)
        soup = BeautifulSoup(answer.text)

        for a in soup.findAll(lambda tag: tag.name == "a" and "title" in tag.attrs):

            try:

                annonce = a.get('href')
                title = a.select('.lbc .detail .title')[0].get_text().lower().strip()

                if 'zoe' in title:
                    print(region, title)
                    year, km, price, tel = scrap_annouce(announce_url)
                    annoncedat = {'region': region}
                    annoncedat.update({'année': year, 'km': km, 'prix': price, 'tel': tel})
                    annoncedat.update({'model': model for model in models if model in title})

                    try:
                        argus = search_argus(annoncedat['model'], str(annoncedat['année']))
                    except KeyError, ValueError
                        argus = 0
                    announce_data.update({'argus': argus})
                    data = data.append(annoncedat, ignore_index=True)

            except IndexError:
                print('erreur')
                pass
    #Check sur 10            
    print data.head(10)

#Exit
scrap(regions)
#toCSV
pd.to_csv("renaultZoe.csv", index=False)

