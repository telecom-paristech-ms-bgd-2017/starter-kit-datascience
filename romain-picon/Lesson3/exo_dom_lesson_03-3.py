# coding: utf8

"""

L'exercice pour le cours prochain est le suivant:
- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075
- En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens
de stars des repositories qui leur appartiennent. Pour finir classer ces 256 contributors par leur note moyenne.﻿
"""

import json

import pandas
import requests
from bs4 import BeautifulSoup

debug_this_sh = True

"""
githubUsers
  .filter(user => user.followers > 635)
  .sortBy('contributions')
  .slice(0, 256)
"""


def view_tag(tag, n=0):
    """
    For debug, display tag content.
    """

    print(n * '\t' + '--------Tag--------')
    print(n * '\t', tag)
    print(n * '\t', '--------Tag Attributes--------')
    print(n * '\t', tag.attrs)
    print(n * '\t', '--------Tag String--------')
    print(n * '\t', tag.string)


def to_integer(tag):
    """
    To convert a string into integer and remove tricky chars from utf8.
    """

    return int(tag.text.replace('\xa0', '').replace(' ', ''))


def clean_string_to_float(in_string):
    """
    :param in_string: the string to clean, like "13€32" or "13,32"
    :return: 13.32
    """
    if len(in_string) > 0:
        out_string = in_string.replace(',', '.')
        out_string = out_string.replace('€', '.')
    else:
        out_string = '0'

    return out_string


def create_rank_table():
    """
    Crawl through https://gist.github.com/paulmillr/2657075 and create a
    data frame containing best contributors
    :return: dataframe
    """

    # The base of the url
    url_full = 'https://gist.github.com/paulmillr/2657075'

    # Create soup
    soup = BeautifulSoup(requests.get(url_full).text, "html.parser")

    # Find the table in the page
    for tag_table in soup.find_all('table'):

        df_head = []

        # First create agnostically the DF and the header
        for tag_head in tag_table.find_all('thead'):
            for tag_th in tag_head.find_all('th'):
                if tag_th.get_text() in {'#', 'User', 'Contribs'}:
                    df_head.append(tag_th.get_text())
            df = pandas.DataFrame(columns=df_head)
            df_line_nb = -1

        for tag_body in tag_table.find_all('tbody'):
            # Then go through every line
            for tag_tr in tag_body.find_all('tr'):
                # A new line
                df_line_nb = df_line_nb + 1

                # Then go through every cells
                tag_th = tag_tr.find_all('th')
                df.loc[df_line_nb, '#'] = tag_th[0].get_text()

                tag_td = tag_tr.find_all('td')
                df.loc[df_line_nb, 'User'] = tag_td[0].get_text()
                df.loc[df_line_nb, 'Contribs'] = tag_td[1].get_text()

    return df

def git_get_average_stars(user_name):
    """
    Will parse all the user's repos and build the mean of stars.
    :param user_name: user name on github or complete user name like weierophinney (Matthew Weier O'Phinney)
    :return: mean of stars, for all user's project
    """

    # Clean weierophinney (Matthew Weier O'Phinney) to get weierophinney
    split_user_name = user_name.split(' ')

    # Git authentication tuple (shall not be in the code)
    # Fill with you user / token
    auth_tuple = ('dokteurwho','XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


    # User main profile
    url_full = 'https://api.github.com/users/' + split_user_name[0]

    # Get the user description
    r = requests.get(url_full, auth=auth_tuple)
    data = json.loads(r.text)

    # print(data['repos_url'])

    # Get the url centralizing all the repo
    url_full = data['repos_url']

    # Get the repo list
    r = requests.get(url_full, auth=auth_tuple)
    data = json.loads(r.text)

    # Display result
    print(split_user_name[0])

    # Get stars per project
    stars_mean = 0
    item_nb = 0
    for item_nb, datum in enumerate(data):
        stars_mean = int(datum['stargazers_count']) + stars_mean
        # print(item_nb + 1, '\t\t', datum['name'], '\t\t', datum['stargazers_count'])

    return stars_mean / (item_nb + 1)



def main():
    """

    Crawl through https://gist.github.com/paulmillr/2657075 and create a
    data frame containing best contributors.

    For every contributors, list their repo and calculate the mean of stars per repo

    :return: returning nothing is already returning something
    """


    df = create_rank_table()

    print('A list of geeks.')
    print(df)

    # brands = pd.Series(car_names.str.split().str.get(0))

    df['Stars'] = df['User'].apply(git_get_average_stars)

    print(df.sort_values('Stars'))

if __name__ == '__main__':
    main()