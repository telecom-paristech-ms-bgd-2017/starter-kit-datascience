import requests
import urllib.request
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

#OAuth for Github
auth = {'Authorization': 'token %s' % '1427a26e96ed8edd9575d22d760f68a4fd2a6c93'}
url ="https://gist.github.com/paulmillr/2657075"
url_read = urllib.request.urlopen(url).read()
soup = BeautifulSoup(url_read, 'html.parser')

tbl_url = []
tbl_name = []
tbl = soup.find("table")
tags = tbl.find_all("tr")

#get the github links associated to each user
for tag in tags[1:]:
    sub_url = tag.find('a').text
    sub_url2 = 'https://api.github.com/users/'+sub_url+'/repos'
    tbl_name.append(sub_url)
    tbl_url.append(sub_url2)

star_tabl = []
for el in tbl_url:
    el_read = requests.get(el, headers=auth)
    res = json.loads(el_read.text)
    star = []
    for i in range(len(res)):
        sum_res = res[i]['stargazers_count']
        star.append(sum_res)
    mean_star = np.mean(star)
    star_tabl.append(mean_star)
d = {'Names': tbl_name, 'Average Stars': star_tabl}
df = pd.DataFrame(data = d, index=None)
result = df.sort_values('Average Stars',ascending=False)

print(result)
