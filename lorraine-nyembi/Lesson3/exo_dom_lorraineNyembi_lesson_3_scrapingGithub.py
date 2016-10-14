# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine
"""

#import urllib.request as ur
#from github3 import login, GitHub
#from getpass import getpass, getuser
#import sys

import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
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
#myTOKEN_old = '444b643ec7e9aba15ace4d1f3e89372155621d63' # let's get this in that url ==> https://github.com/settings/tokens/new
#fv4 = login(token=myTOKEN)
myTOKEN = '9b4f0745253b59146dedce03b922b97742d39c2e'
PAGE = 1

def getAllReposForASingleUser(user_name):    
  user_repos = json.loads(requests.get("https://api.github.com/users/" + user_name + "/repos?page=" + str(PAGE), auth=(user_name, myTOKEN)).text)
  
  return user_repos
  


def getStarsNumberForAllUser():
    
    user_repoCount_starCount = []
    star_count = 0
    repo_count = 0
    temp = []
    users_name = getFamousGithubContributorsFromDOM(GITHUB_URL)
    if(len(users_name) > 0):
        for user in users_name:
            user_repos_list = getAllReposForASingleUser(user)
            #print(len(user_repos_list))
            if(len(user_repos_list) > 0):
                for repo in user_repos_list:
                    star_count += repo["stargazers_count"]
                    repo_count += 1
                
                temp = [user, repo_count, star_count]
                if(repo_count > 0):
                    temp.append(star_count / repo_count)
                else:
                    temp.append(0)
                user_repoCount_starCount.append(temp)
    

    top_contributors_df = pd.DataFrame(user_repoCount_starCount)
    
    top_contributors_df.columns = ["user name","number of repositories", "number of stars", "mean stars per repo"]
    
    print(top_contributors_df.head())
    
    

getStarsNumberForAllUser()  
