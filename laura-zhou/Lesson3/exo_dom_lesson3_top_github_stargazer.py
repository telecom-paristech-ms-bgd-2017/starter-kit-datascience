# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup 
import requests
import json 
import pandas as pd


def get_top_github():   
    #read file
    url = "https://gist.github.com/paulmillr/2657075"
    s = urllib.request.urlopen(url).read()
    #make soup
    soup = BeautifulSoup(s,"html.parser")
    res=soup.find_all("td") 
    l=[]
    #nom et pseudo apparaisse 1 ligne sur 4
    for i in range(0,len(res),4): 
        pseudo=res[i].find("a").text
        l.append(pseudo)

    return l


def get_stargazers_count(pseudo):
    access_token="TOKEN"
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get('https://api.github.com/users/' + pseudo + '/repos', headers=headers)
    me_json = response.json() #permet de lire le Json dans une liste
    count=0
    try:
        for i in range(len(me_json)):
            count+=me_json[i]['stargazers_count']
        return (count/len(me_json))
    #jfrazelle profile is private, the count is null
    except ZeroDivisionError:
        return None
        
#save in a list        
ccl1=get_top_github()  
ccl2=[]

#for top in get_top_github():
#    print(top,get_stargazers_count(top))

for top in get_top_github():
    ccl2.append(get_stargazers_count(top))
 
df=pd.DataFrame(ccl1) 
df.columns=['github_name']
df["avg_stargazer_per_repo"]=ccl2
 
df_sorted=df.sort_values(by="avg_stargazer_per_repo", ascending=False)
print(df_sorted)
df_sorted.to_csv("github_stargazers.csv", sep=";", header = True)