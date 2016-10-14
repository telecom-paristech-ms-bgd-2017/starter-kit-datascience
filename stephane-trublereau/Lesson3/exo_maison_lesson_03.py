import numpy
import requests
import operator
from bs4 import BeautifulSoup

# Base url for listing top GitHub contributors.
github_url = 'https://gist.github.com/paulmillr/2657075'
github_base_url = "https://github.com/"
github_user_starred_url = 'https://api.github.com/users/<user>/repos'

# Initialisation du Header requête get
Headers = {}

# Récupération du Token dans fichier local, renvoi en retour token
def load_token(filename):
    with open(filename, 'r') as file:
        token = file.readline().strip()
        return token

# Chargement de la list des users
def load_user_list_page():
    url = github_url
    return requests.get(url)

def get_user_names():
    data = load_user_list_page()
    # Liste des users récupérer dans le tableau resultat de l'html
    results = []
    print("Attente du résultat dans une minute, requêtes envoyées ")
    parser = BeautifulSoup(data.text, 'html.parser')
    article_node = parser.find("article")
    if article_node:
        table_node = article_node.find("table")
        if table_node:
            for a_node in table_node.findAll("a"):
                url = a_node.attrs['href']
                if url.startswith(github_base_url):
                    results.append(url[len(github_base_url):])
                    #print(url)
    return results

def get_starred_repos(user, token):
    url = github_user_starred_url.replace('<user>', user)
    Headers['Authorization'] = 'token ' + token
    r = requests.get(url, headers=Headers)
    t = r.json()
    results = [0];
    for i in t:
        if isinstance(i, dict):
            results.append(i["stargazers_count"])
    # print(results)
    return numpy.mean(results)

def sort_users_starred(token):
    #print(get_user_names())
    results = {}
    stars = 0
    for user in get_user_names():
        Headers['Authorization'] = 'token ' + token
        stars = get_starred_repos(user, token)
        results[user] = stars
    # tri du resultats et affichage
    results_sorted = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    nb = 0
    for (result, count) in results_sorted:
        print(" nom : " + result + " stars : " + str(count))
        nb = nb + 1
        if nb > 256 :
            break
    print ("nombre de personnes affiché : " + str(nb))
    return

sort_users_starred(load_token('gitHubtoken.txt'))
