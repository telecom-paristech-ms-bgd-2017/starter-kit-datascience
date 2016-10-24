import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import re
from functools import partial
import sys

sys.setrecursionlimit(100000)

def getSearchPageByRegion(url, region, num_page):
    #print("*"*60,"Page de recherche","*"*60)
    #print("Page Number : ", num_page)
    data = {'q':'zoe', 'it':1, 'o':num_page}
    request = requests.get(url+region, params = data)
    result_soup = BeautifulSoup(request.text,'html.parser')
    return result_soup

def getLastPage(soup):
    lastpage = soup.find("a", {"id": "last"})
    pattern = "(?<=o=)(.*?)(?=&)"
    lastpage_id = re.search(pattern, str(lastpage))
    return lastpage_id.group(0)


def getLinksbyItem(soup):
    #print("*"*60,"Récupération des URL des annonces","*"*60)
    items = soup.find_all(class_ = 'list_item clearfix trackable')
    links = []
    pattern = "w{3}\.leboncoin.fr\/voitures\/(.*)\htm"
    for item in items:
        href = re.search(pattern, str(item))
        try :
            links.append("http://"+str(href.group(0)))
        except:
            return links
            break
    return links

def getLinksFromSearchPage(url, region):
    data = {'q': 'zoe', 'it': 1, 'o':1}
    firstpage = getSearchPageByRegion(url, region, 1)
    try:
        maxPage = getLastPage(firstpage)
    except:
        maxPage = 1
        # #print("Only one page")
    # #print(maxPage)
    p = Pool(5)
    func = partial(getSearchPageByRegion, url, region)
    searchPages = p.map(func, range(1, int(maxPage)+1))# OK
    linkslist = p.map(getLinksbyItem, searchPages)
    return linkslist

def extractInfoFromAd(link):
    offre = {}
    request = requests.get(link)
    result = BeautifulSoup(request.text,'html.parser')
    #print("Ad ID : ")
    offre['ID'] = int(re.search("(?<=voitures\/)\d*(?<=)", link).group(0))
    #print(offre['ID'])
    #print("Price")
    offre['Prix'] = int(re.search('(?<=content=")(.*?)(?=\")', str(result.find(class_ = "item_price clearfix"))).group(0))
    #print(offre['Prix'])
    #print("KM")
    offre['Kilométrage'] = int(re.search('(?<=value\">)(.*?)(?= KM)', str(result)).group(0).replace(" ",""))
    #print(offre['Kilométrage'])
    #print("year")
    offre['Année'] = int(re.search('20[0-1][0-9]', str(result),flags = re.DOTALL ).group(0))
    #print(offre['Année'])
    #print("Pro ou particulier  ?")
    try :
        re.search("SIREN", str(result)).group(0)
        #print('SIREN Found')
        offre['Pro'] = 1
        offre['Particulier'] = 0
    except :
        #print("SIREN not Found")
        offre['Pro'] = 0
        offre['Particulier'] = 1
    #print('Type Vendeur : ', "Pro ? : ", offre['Pro'], "Particulier ? : ", offre['Particulier'])
    #print("*"*60,"Récupération du numéro","*"*60)
    offre['Numéro'] = ""
    try :
        #print("Getting phone number in description")
        offre['Numéro'] = re.search("0{1}\d{9}|(\d\d\s){4}\d\d|(\d\d\.){4}(\d\d)",str(result)).group(0).replace(" ","").replace(".","")
        #print("Number Found ! : ", offre['Numéro'])
    except :
        try :
            post_data = {'key' : '54bb0281238b45a03f0ee695f73e704f', 'app_id':'leboncoin_web_utils', 'text' : 1, 'list_id' : offre['ID']}
            post = requests.post("https://api.leboncoin.fr/api/utils/phonenumber.json",post_data)
            offre["Numéro"] = re.search("0\d{9}", post.text).group(0)
            #print("Numéro : ", offre['Numéro'])
        except :
            print("Unable to retrieve phone number ... Maybe kicked by the API")
    #print("Retrieving Model Version")
    offre['Version'] = ""
    try :
        offre['Version'] = re.search("life|intens|zen", str(result).lower()).group(0)
    except :
        offre['Version'] = "inconnu"
    #print("Version : ", offre['Version'])
    #print("***********Retrieving Argus***********")
    offre['Argus'] = getArgus(offre['Version'],offre['Année'])
    #print("Prix Argus : ", offre['Argus'])
    offre['Sous-Evalué'] = 'inconnu'
    if offre['Argus'] != 'inconnu':
        offre['Sous-Evalué'] = 1 if offre['Prix'] < offre['Argus'] else 0
    return offre


def getArgus(modele, annee):
    # baseURL :'http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2014.html'
    URL = 'http://www.lacentrale.fr/cote-auto-renault-zoe-'+modele+'+charge+rapide-'+str(annee)+'.html'
    result = BeautifulSoup(requests.get(URL).text,'html.parser')
    #print("URL",URL)
    argus = 'inconnu'
    try :
        argus = re.search("\d+\s.\d*\s*€",result.find(class_ = 'f24 bGrey9L txtRed pL15 mL15').text).group(0).replace(" ","").replace("€","")
        #print("Found Argus : ", argus)
        return int(argus)
    except :
        #print("Pas d'argus trouvé")
        return argus

def scrapLeBonCoin():
    url = 'https://www.leboncoin.fr/voitures/offres/'
    regions = ['ile_de_france/', 'aquitaine/', 'provence_alpes_cote_d_azur/']
    links = []
    for region in regions:
        #print("Processing : ", region)
        links.append(getLinksFromSearchPage(url, region))
        # #print("Dans boucle : ", links)
    links = [x for sublist in links for x in sublist]
    links = [x for sublist in links for x in sublist]
    #print("Links : ", len(links))
    offres = []
    # for link in links[:1]:
        # #print(link)
    print("Processing")
    p = Pool(5)
    offres.append(p.map(extractInfoFromAd, links))
    print("...")
    offres = [x for sublist in offres for x in sublist]
    #print(offres)
    print()
    pd.DataFrame(offres, columns = ['ID','Prix','Kilométrage','Année','Pro','Particulier','Numéro','Version','Argus','Sous-Evalué']).to_csv("zoe.csv",sep = "\t")
    

scrapLeBonCoin()
