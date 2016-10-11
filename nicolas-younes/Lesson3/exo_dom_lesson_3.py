import requests
from bs4 import BeautifulSoup
from github import Github
import json
from operator import itemgetter
from pprint import pprint

token = "e9d5cdc35b57e949fe272f7f3651217ad78522af"
login = "NicoYouyou"
apiurl = "https://api.github.com/users/"
url = "https://gist.github.com/paulmillr/2657075"
tokenurl = "?access_token=" + token
dict_token = {"access_token": "e9d5cdc35b57e949fe272f7f3651217ad78522af"}

g = Github(login_or_token=token)

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
list_tr = soup.find_all("tr")
list_contributors = []

i = 1
while i <= 256:
    list_contributors.append(list_tr[i].find_all("td")[0].find("a").text)
    i += 1

print(list_contributors)


def get_average_star(user):
    url = apiurl + user + "/repos" + tokenurl
    req = requests.get(url, params=dict_token).text
    js = json.loads(req)
    count_stars = 0.0
    n_repo = 0.0
    average_star = 0.0
    for repo in js:
        count_stars += repo["stargazers_count"]
        n_repo += 1
    print(user)
    try:
        average_star = count_stars / n_repo
    except ZeroDivisionError:
        average_star = 0.0
        print("error")
    return(average_star)

print(get_average_star("GrahamCampbell"))


def stars_for_user_list(users):
    results = {}
    for u in users:
        results[u] = get_average_star(u)
    return results

contributors = stars_for_user_list(list_contributors)
sorted_contributors = sorted(contributors.items(), key=itemgetter(1),
                             reverse=True)
pprint(sorted_contributors)
