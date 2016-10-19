# @ Author : BENSEDDIK Mohammed

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import json

versions = []
annees = []
kilometrage = []
prix = []
telephones = []
descriptions = []

salesman_type = ['p', 'c']

true_annees = []
true_kilometrage = []
true_prix = []
telephones = []
pro = []
argus = []

zones = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']
url_begining = "https://www.leboncoin.fr/voitures/offres/"
url_end = "/?q=renault%20zo%E9&f="

url_begining_page = "https://www.leboncoin.fr/voitures/offres/"
url_end_page = "q=renault%20zo%E9&f="


for zone in zones:
    url = url_begining + zone + url_end

    for stype in salesman_type:

        url_leboncoin = url + stype
        request_page = requests.get(url_leboncoin)
        soup_page = BeautifulSoup(request_page.text, 'html.parser')

        total_pages = soup_page.find("span", {"class", "total_page"})
        if(not total_pages):
            total_pages = 1
        else:
            total_pages = int(total_pages.text)

        for page in range(1, total_pages + 1):
            url_page = url_begining_page + zone + \
                "?o=" + str(page) + "&" + url_end_page
            url_leboncoin_page = url_page + stype
            request = requests.get(url_leboncoin_page)
            soup = BeautifulSoup(request.text, 'html.parser')
            block_lbc = soup.find(
                "section", {"class": "tabsContent block-white dontSwitch"})

            articles = block_lbc.find("ul").find_all("li")

            titles = []

            for article in articles:
                if(stype == 'p'):
                    pro.append('Particulier')
                if(stype == 'c'):
                    pro.append('Professionnel')
                titles.append(article.find("h2", {"class": "item_title"}).text)

            for title in titles:
                ver = re.findall("(?i)intens|zen|life", title)
                if(not ver):
                    versions.append(None)
                else:
                    versions.append(ver[0].capitalize())

            for article in articles:
                url_ref = article.find("a").get("href")
                url_ref = "https:" + url_ref
                req_article = requests.get(url_ref)
                soup_article = BeautifulSoup(req_article.text, 'html.parser')

                properties_article = soup_article.find_all(
                    "h2", {"itemprop", "clearfix"})
                prix.append(properties_article[0].text)
                annees.append(properties_article[4].text)
                kilometrage.append(properties_article[5].text)
                descriptions.append(soup_article.find(
                    "p", {"class", "value"}, {"itemprop", "description"}).text)


for price in prix:
    pr = re.findall("[0-9]*\s?[0-9]*\s?€", price)
    if(not pr):
        true_prix.append(None)
    else:
        true_prix.append(
            int(pr[0].replace(u'\xa0', '').replace('€', '').replace(' ', '')))


for km in kilometrage:
    kil = re.findall("(?i)[0-9]*\s?[0-9]*\s?km", km)
    if(not kil):
        true_kilometrage.append(0)
    else:
        true_kilometrage.append(int(kil[0].replace('KM', '').replace(' ', '')))

for annee in annees:
    an = re.findall("[0-9]{4}", annee)
    if(not an):
        true_annees.append(None)
    else:
        tmp = int(an[0].replace(u'\xa0', ''))
        if((tmp > 2016 or tmp < 2013)):
            true_annees.append(None)
        else:
            true_annees.append(tmp)


versions = pd.Series(versions, name='Version')
prix = pd.Series(true_prix, name="Prix")
kilometrage = pd.Series(true_kilometrage, name="Kilometrage")
annees = pd.Series(true_annees, name="Annee")
profpart = pd.Series(pro, name="TypeVendeur")

final_data = pd.concat([versions, annees, prix, kilometrage, profpart], axis=1)

final_data.to_csv('voitures.csv', float_format='%.12g')

final_data_clean = final_data.dropna()
final_data_clean.to_csv('voitures_sans_vide.csv', float_format='%.12g')
final_data_clean = pd.read_csv('voitures_sans_vide.csv')

annee_and_km = final_data_clean[['Version', 'Annee', 'Kilometrage']].values
s = requests.Session()
argus = []
for ver, annee, km in annee_and_km:
    if(annee == 2016):
        url = "http://www.lacentrale.fr/cote-auto-renault-zoe-" + \
            ver.lower() + "+charge+rapide+type+2-" + str(annee) + ".html"
    else:
        url = "http://www.lacentrale.fr/cote-auto-renault-zoe-" + \
            ver.lower() + "+charge+rapide-" + str(annee) + ".html"
    r = s.get(url)
    url_argus = "http://www.lacentrale.fr/cote_proxy.php?km=" + \
        str(km) + "&month=01"
    req = s.post(url_argus)
    j = json.loads(req.text)
    argus.append(j['cote_perso'])

final_data_clean['Argus'] = pd.DataFrame(argus)
print(final_data_clean)
final_data_clean.to_csv('voitures_sans_vide.csv', float_format='%.12g')
