import requests
import re  # Module Regex
from bs4 import BeautifulSoup
import pandas as pd


def scan(region):
      print('Scanning ' + region + '...')
      i = 1
      prix = []
      annee = []
      km = []
      modele = []
      tel = []
      vendeur = []
      cote = []
      url = 'https://www.leboncoin.fr/voitures/offres/' + region + '/'
      while True:
            params = {'q': 'renault zoe', 'o': i}
            soup = BeautifulSoup(requests.get(url, params=params).text, 'html.parser')

            try:
                  annonces = soup.find_all(class_='tabsContent block-white dontSwitch')[0].find_all(
                        'a', class_='list_item clearfix trackable')
                  i += 1

                  for e in annonces: # on sonde chacune des annonces de la page
                        print('Analyzing ' + e.find(class_='item_title').text.strip())
                        tsoup = BeautifulSoup(requests.get('https://' + e['href'].replace('//', '')).text, 'html.parser')

                        prix.append(tsoup.find(itemprop='price')['content'])  # prix
                        annee.append(tsoup.find(itemprop='releaseDate').text.strip())  # année

                        km.append(tsoup.find_all('h2', class_='clearfix')[5].find(class_='value')
                                  .text.replace(' ', '').replace('KM', ''))  # kilométrage

                        try:
                              if 'pro' in e.find_all(class_='ispro')[0].text:
                                    vendeur.append('Professionnel')
                        except:
                              vendeur.append('Particulier')

                        if 'zen' in e.find(class_='item_title').text.strip().lower():
                              modele.append('Zen')
                        elif 'intens' in e.find(class_='item_title').text.strip().lower():
                              modele.append('Intens')
                        elif 'life' in e.find(class_='item_title').text.strip().lower():
                              modele.append('Life')
                        else:
                              modele.append('NA')

                        desc = tsoup.find(itemprop='description')
                        try:
                              m = re.search("0[0-9]{9}", desc.text.strip())  # numéro
                              tel.append(m.group())
                        except:
                              tel.append('NA')

                        type = ''
                        if 'charge rapide' in desc.text.lower():
                              type += '+charge+rapide'
                        if 'type' in desc.text.lower():
                              type += '+type+2'
                        page = 'http://www.lacentrale.fr/cote-auto-renault-zoe-'+ \
                               modele[-1] + type + '-' + annee[-1] + '.html'
                        # print(page)
                        centrale = BeautifulSoup(requests.get(page).text, 'html.parser')

                        try:
                              cote.append(centrale.find('strong', class_='f24 bGrey9L txtRed pL15 mL15'). \
                                          text.strip().replace('€', '').replace(' ',''))
                        except:
                              cote.append('NA')

            except:
                  break # on sort de la boucle si on dépasse la page maximum

      # Création du dataframe :
      df = pd.DataFrame()
      df['Modele'] = modele
      df['Annee'] = annee
      df['Km'] = km
      df['Prix'] = prix
      df['Cote'] = cote
      df['Type'] = vendeur
      df['Tel'] = tel
      df.to_csv(region + '.csv')

scan('provence_alpes_cote_d_azur')
scan('ile_de_france')
scan('aquitaine')