import requests
from bs4 import BeautifulSoup
import pandas as pd

# Crawling 256 top Github contributors
active_github = BeautifulSoup(requests.get('https://gist.github.com/paulmillr/2657075').text, 'html.parser')
row_lists = active_github.find_all('tbody')[0].find_all('tr')

# Extracting Contributors' name
users = [row.find_all('a')[0].text.replace(u'\xa0', '') for row in row_lists]

# Reading token to access Github API
myFile = open('github_key.txt')
params = {'access_token': myFile.readlines()[0], 'type': 'owner'}
myFile.close()

# Extracting mean stars for every user
mean_stars = pd.DataFrame()
mean_stars['name'] = users
mean_stars_list = []
for user in users:
    print('Exploring ' + user + '...')
    curr_github_repositories = requests.get('http://api.github.com/users/' + user + '/repos', params=params)
    i, curr_mean_stars = 0, 0
    
    for repos in curr_github_repositories.json():
        curr_mean_stars += repos['stargazers_count']
        i += 1
    if(i != 0):
        mean_stars_list.append("%.2f" % (curr_mean_stars / i))
    else:
        mean_stars_list.append("0.0")

mean_stars['mean star'] = mean_stars_list

# Saving data in a csv file
mean_stars.to_csv('Mean_star_per_users.csv')
