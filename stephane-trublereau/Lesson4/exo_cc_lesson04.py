import numpy
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base url pour récupérer les distances entre les 30 principales villes de France
Goole_url = 'https://maps.googleapis.com/maps/api/distancematrix/xml?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Vancouver+BC&mode=bicycling&l'

# Récupération des principales villes de France
villes_url = 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'
villes_base_url = "/wiki/"

# Common HTTP request query parameters, if any
Params = {
    # "access_token": '<token>'
}
# Common HTTP request headers, if any
Headers = {
    # "Authorization": 'token <token>'
}
def nettoie_ville(text):
    texts = text.replace(u'_', ' ').replace('%C3%89', 'E').replace('%C3%AE', 'i').replace('%C3%A9', 'é')
    return texts


# Loads an oAuth token from the designated file;
# returns the token as a string.
# The oAuth token must, for example, be obtained via "https://github.com/settings/tokens" and saved in a file locally.
def load_oauth_token(filename):
    with open(filename, 'r') as file:
        token = file.readline().strip()
        return token

def Distance(ville1, ville2, API_KEY) :
    url = 'https://maps.googleapis.com/maps/api/distancematrix/xml?origins='+ville1+'&destinations='+ville2+'&key=' + API_KEY
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
#    print(soup)
    a = soup.find_all('text')
    return a[1].text.replace('<text>','').replace('</text>',''),\
           a[0].text.replace('<text>','').replace('</text>','').\
               replace(u'hour','h').replace(u'hs','h').replace(u'min','mn').replace(u'mns','mn')

#https://maps.googleapis.com/maps/api/distancematrix/xml?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Vancouver+BC&mode=bicycling&language=fr-FR&key=YOUR_API_KEY
# Récupération du Token dans fichier local, renvoi en retour token
def load_token(filename):
    with open(filename, 'r') as file:
        token = file.readline().strip()
        return token

# Chargement de la list des villes
def load_villes_list_page():
    url = villes_url
    return requests.get(url)

def get_ville_names():
    data = load_villes_list_page()
    # Liste des villes récupérer dans le tableau resultat de l'html
    results = []
    print("Attente du résultat dans une minute, requêtes envoyées ")
    parser = BeautifulSoup(data.text, 'html.parser')
    table_node = parser.find("table")
#    print(article_node)
    if table_node:
#        table_node = article_node.find("table")
#        if table_node
        count = 3
        count_villes = 1
        for a_node in table_node.findAll("a"):
#           print(a_node)
            url = a_node.attrs['href']
            if url.startswith(villes_base_url):
                if count == 3 :
                    s= nettoie_ville(url[len(villes_base_url):])
 #                   print(s)
                    results.append(s)
                    count_villes = count_villes + 1
                    if count_villes > 90 :
                        break
                    count = 1
                else:
                    count = count + 1
 #       print(results)
    return results
#    return

tableau_ville = get_ville_names()
i = 0

#print(tableau_ville[0])

#ville_1 = tableau_ville[1]
c = []
col={}
nb_ville = 20
#df = pd.DataFrame({'ville/ville': tableau_ville[0:nb_ville]}, index=tableau_ville[0:nb_ville])
df_distance = pd.DataFrame({}, index=tableau_ville[0:nb_ville])
df_duree = pd.DataFrame({}, index=tableau_ville[0:nb_ville])
#print(df_distance)
#print(df_duree)
while i < nb_ville :
    colonne_distance = []
    colonne_duree =[]
    j = 0
    while j < nb_ville :
        if i == j :
            colonne_distance.append("0 km")
            colonne_duree.append("----")
        else :
    #for ville
    #print(Distance('Paris', 'Lille',load_oauth_token('Google_token.txt')))
            distance, duree = Distance(tableau_ville[i], tableau_ville[j],load_oauth_token('Google_token.txt'))
#            print(duree.replace('hours', 'h').replace('mins','mn'))
            colonne_distance.append(distance)
            colonne_duree.append(duree)
#            ligne.append(distance)
        j = j + 1
#    print(colonne)
    df_distance[tableau_ville[i]] = colonne_distance
    df_duree[tableau_ville[i]] = colonne_duree
    i = i + 1
#    print(type(colonne))
print(df_distance)
print(df_duree)
#df_distance.head(10)
df_distance.to_csv('distance.csv')
df_duree.to_csv('duree.csv')
