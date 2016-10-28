from urllib.request import urlopen
from lxml.html import parse
import pandas as pd
from pandas.io.parsers import TextParser
import requests
import json

url = 'https://gist.github.com/paulmillr/2657075'
parsed = parse(urlopen(url))
doc = parsed.getroot()
tables = doc.findall('.//table')
rows = tables[0].findall('.//tr')


def _unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text_content() for val in elts]


header = _unpack(rows[0], kind='th')
data = [_unpack(r) for r in rows[1:]]
data_ = TextParser(data, names=header[1:]).get_chunk()
clean_data = pd.DataFrame(data_, columns=['User', 'Contribs', 'Location'])
clean_data.to_csv('256_Top_Contributors.csv')
print('First part: List of 256 Top contributors saved to 256_Top_Contributors.csv')

###############
# Second part #
###############

token = '4efc542dfb9e2fb1756529dfe242b46d92455362'
API = 'https://api.github.com'
myHeaders = {'Authorization': 'token 4efc542dfb9e2fb1756529dfe242b46d92455362'}
listUsers = []
for i in range(clean_data['User'].size):
    listUsers.append(clean_data['User'][i].split(" ")[0])
# print(listUsers)


# returns list of repos of 'user'
def get_user_repos(user):
    # user = 'fabpot'
    res = []
    API_user = API + '/users/' + user + '/repos'
    r = requests.get(API_user, headers=myHeaders)
    J = json.loads(r.text)
    for i in range(len(J)):
        res.append({key: J[i][key] for key in ['id', 'full_name', 'stargazers_count']})
    return res


# average stars number of repos in list of dicts containig id, full_name & stargazers_count of each repo
def get_average_stars(listOfRepos):
    numStarsList = []
    for i in range(len(listOfRepos)):
        numStarsList.append(listOfRepos[i]['stargazers_count'])
    if len(numStarsList) == 0:
        return 0
    else:
        return (sum(numStarsList) / float(len(numStarsList)))


listNotes = []
for i in range(len(listUsers)):
    print(str(i) + ' getting note of user ' + listUsers[i])
    listNotes.append(get_average_stars(get_user_repos(listUsers[i])))
clean_data['Average note'] = listNotes
clean_data.sort(columns='Average note', ascending=False).to_csv('Sorted_256_Top_Contributors.csv')
print('Second part: List of 256 Top contributors saved to Sorted_256_Top_Contributors.csv')
