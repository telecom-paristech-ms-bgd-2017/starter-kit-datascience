# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine

"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


# Get users name from GitHub
GITHUB_URL = 'https://gist.github.com/paulmillr/2657075'

def extractDataForPage(soup):  

  body_ = []
  row_ = []
  users_name = []

  all_table = soup.find_all(class_= 'readme blob instapaper_body')
  for table_ in all_table:
      body_.extend(table_.find_all('tbody'))

  for b in body_:
      row_= b.select('a[href^="https://github.com/"]') #CSS selector that gets href starting with "https://github.com/"
  
  for item in row_: 
      users_name.append(item.text)
 
  print ("There are %s famous users" %len(users_name))
  return users_name

# Extract Top contributors by using crawling
def getFamousGithubContributorsFromDOM(url):

    results = requests.get(url)
    soup = BeautifulSoup(results.text,'html.parser')
    users_name = extractDataForPage(soup)
    return users_name

# Get stars count for each user
myTOKEN = '9d6c2ac83fce8ee1f72722f28bac1e26a0b4e1b2'
PAGE = 1
  

def getStarsNumberForAllUser():
    
    user_repoCount_starCount = []
    star_count = 0
    repo_count = 0
    temp = []

    users_name = getFamousGithubContributorsFromDOM(GITHUB_URL)
    print("[user name, " + "number of repositories, "+ "number of stars, "+ "mean stars per repo]")
    if(len(users_name) > 0):
        for user in users_name[0:]:
            results = requests.get("https://api.github.com/users/" + user + "/repos?page=" + str(PAGE), auth=(user, myTOKEN))
            user_repos_list = json.loads(results.text)   
            
            if(len(user_repos_list) > 0):
                for repo in user_repos_list:
                    star_count += repo['stargazers_count']
                    repo_count += 1
                
                temp = [user, repo_count, star_count]
                if(repo_count > 0):
                    temp.append(star_count / repo_count)
                else:
                    temp.append(0)
                print(temp)
                user_repoCount_starCount.append(temp)

    top_contributors_df = pd.DataFrame(user_repoCount_starCount)
    top_contributors_df.columns = ["user name","number of repositories", "number of stars", "mean stars per repo"]
    print(top_contributors_df)
    top_contributors_df.to_csv('top_contributors_github_metrics_API_TOKEN_'+myTOKEN+'.csv')    
    
getStarsNumberForAllUser()  
