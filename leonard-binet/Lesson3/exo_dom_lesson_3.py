"""
githubUsers
  .filter(user => user.followers > 635)
  .sortBy('contributions')
  .slice(0, 256)
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import ipdb
import numpy as np
from requests.auth import HTTPBasicAuth

auth_user = "Leonardbinet"
auth_token = "e72fd38150c9aaa6100c420f531a59d2fc6226b0"


def get_github_token():
    with open('token.txt') as f:
        return f


def get_df_best_contributors(number):
    url = "https://gist.github.com/paulmillr/2657075"
    rq = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_token)).text
    soup = BeautifulSoup(rq, "html.parser")
    df = soup_to_contributors_df(soup)
    return df


def soup_to_contributors_df(soup):
    """ Prend en argument la soupe, et renvoie un dataframe des utilisateurs"""
    columns = ["Classement", "Contribs", "Location"]
    # index = "Classement"
    df = pd.DataFrame(columns=columns)
    # df = df.set_index("Classement")
    result = soup.find("tbody")
    result = result.find_all("tr", recusive=False)
    for el in result:
        eltd = el.find_all("td")
        classement = el.th.string
        user = eltd[0].contents[0].string
        contribs = eltd[1].string
        location = eltd[2].string
        # ipdb.set_trace()
        liste = [
            classement,
            contribs,
            location
        ]
        dfel = pd.DataFrame([liste], columns=columns, index=[user])
        df = df.append(dfel)
    return df


def add_github_info_to_df(df):
    """
    Prend pour argument un dataframe ayant pour index le nom des utilisateurs, et
    renvoie le dataframe avec le reste des infos github
    """
    df["moyenne_stars"] = np.nan
    df["nombre_repo"] = np.nan
    for user in df.index.tolist():
        print(user)
        url_base = "https://api.github.com"
        url_add = "/users/"
        url_end = "/repos"
        url = url_base + url_add + user + url_end
        rq = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_token)).text
        df_user = pd.read_json(rq)
        # à partir de la donnée extraite, rajouter les infos
        try:
            repo_star_mean = df_user.stargazers_count.mean()
            repo_count = df_user.stargazers_count.count()
        except AttributeError:
            print("Apparemment pas de repo pour %s" % user)
        df.set_value(col='moyenne_stars', index=user, value=repo_star_mean)
        df.set_value(col='nombre_repo', index=user, value=repo_count)
        # ipdb.set_trace()
    return df
