import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import multiprocessing
import requests
import json


result = requests.get('https://gist.github.com/paulmillr/2657075')
soup = BeautifulSoup(result.text, 'html.parser')

def getContributors() :
    number = []
    user_name = []
    name = []
    contribs = []
    location = []
    for i in range (1,15) :
        contibutor_number = soup.find_all('tr')[i].find_all('th')[0].text.replace(u'\xa0', '')
        contibutor_user_name = soup.find_all('tr')[i].find_all('td')[0].find('a').text.replace(u'\xa0', '')
        contibutor_name = soup.find_all('tr')[i].find_all('td')[0].text.replace(u'\xa0', '')
        contibutor_contribs = soup.find_all('tr')[i].find_all('td')[1].text.replace(u'\xa0', '')
        contibutor_location = soup.find_all('tr')[i].find_all('td')[2].text.replace(u'\xa0', '')
        number.append(contibutor_number)
        user_name.append(contibutor_user_name)
        name.append(contibutor_name)
        contribs.append(contibutor_contribs)
        location.append(contibutor_location)

    number =  pd.DataFrame(number, columns=['Numbers'])
    user_name = pd.DataFrame(user_name, columns=['User_name'])
    name = pd.DataFrame(name, columns=['Name'])
    contribs = pd.DataFrame (contribs, columns =['Contribs'])
    location = pd.DataFrame (location, columns = ['Location'])

    Final_DF =number.join(user_name).join(name).join(contribs).join(location)

    #print (Final_DF['User_name'])
    return Final_DF
my_token = '5418b0c061f43826776d78cdbdb7504463bccd5e'
header = {'Authorization': 'token %s' % my_token}
stars = []
mean_stars = {}
Final_DF = getContributors()
user = Final_DF['User_name']
for i in range(len(user)):
    api_url = 'https://api.github.com/users/' + user[i] + '/repos'
    r = requests.get(api_url, headers = header)
    if r:
        repos_contents = json.loads(r.text)
        for content in repos_contents :
            stars.append(content['stargazers_count'])
            mean_stars ['%s' %user[i]] =  np.mean(stars)

data = pd.DataFrame.from_dict(mean_stars, orient='index', dtype=None )
data.columns = ['Stars']
data_sorted = data.sort_values(['Stars'], ascending=[False])
print (data_sorted)






