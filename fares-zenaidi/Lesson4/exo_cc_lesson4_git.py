from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL on which the crawling will be performed
url = 'https://gist.github.com/paulmillr/2657075'
# OAUTH-TOKEN SHA value
TOKEN = "d00a853188584ccb3eaa737df4b2f1a95da5e085"

auth_code = {'Authorization': 'token ' + TOKEN}


# Access the repository of every top contributor
def top_contributors_avg_nb_stars(names):
    dic = {}
    for name in names:
        sum_stars = 0
        user_repos_url = 'https://api.github.com/users/'+name+'/repos'
        r = requests.get(user_repos_url, headers=auth_code)
        user_repos = r.json()
        if len(user_repos) == 0:
            print(name)
        else:
            for i in range(len(user_repos)):
                sum_stars += user_repos[i]['stargazers_count']
            dic[name] = sum_stars / len(user_repos)
    return dic


def top_contributors_names(soup):
    # Get the list of 256 top contributors stocked in the URL, using CSS selectors
    contributors = soup.select('article > table > tbody > tr > td:nth-of-type(1) > a')
    # Return the user_names of the top contributors
    user_names = []
    for contributor in contributors[:7]:
        user_names.append(contributor.string)
    return user_names


def top_contributors_stars_ranking():
    # Construction of the corresponding HTML parser
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get the 256 top contributors user_names
    user_names = top_contributors_names(soup)
    # Get the average number of stars per for every top contributor
    avg_stars_per_top_contributor = top_contributors_avg_nb_stars(user_names[:7])
    # Store the result in a DataFrame and sort it afterwards
    df = pd.DataFrame(avg_stars_per_top_contributor, index=['Avg. Stars'])
    df = df.sort_index(axis=0, ascending=True)
    # df_sorted = df.sort(ascending=True)
    return df # _sorted


df_ranking = top_contributors_stars_ranking()
print(df_ranking)
#print(type(df_ranking['SamyPesse']))
#print(df_ranking['GrahamCampbell'])
# df_ranking.to_csv('top_contributors_stars_ranking.csv')