# coding: utf8

# Script crawling githbu contributors through API
# Course INFMDI 721 - Lesson 3
# Author : Malik OUSSALAH

#Package Importation############

import requests
from bs4 import BeautifulSoup
import urllib2, base64
import operator
import json
from Tkinter import *


################################



#Configuration####################################################

GIT_LOGIN = 'pmanolov'
# Get your token there : https://github.com/settings/tokens/new
AUTH_KEY = '37f896dde6c1bd776037e5d8c1ff667aea4d6c54'

def start(auth):
    users = {}
    r = requests.get(url='https://gist.github.com/',
            auth=auth)
    soup = BeautifulSoup(r.text,'html.parser')
    starsMean = {}
    for tr in soup('tbody')[0].select('tr'):
        user_name = tr.select('td')[0].text
        user_contrib = tr.select('td')[1].text
        users[user_name] = user_contrib
        user_repo = tr.select('td')[0].text.split(" ")[0]
        user_json = GetJson(user_repo)
        if user_json:
            allrepos = json.loads(user_json)
            sumstars = 0.0
            for el in allrepos:
                sumstars += el['stargazers_count']
            starsMean[user_repo] = sumstars / len(allrepos)
        #print user_name + " " + user_contrib
        print user_name, user_contrib, starsMean[user_repo]
        sortedMean = sorted(starsMean.items(), key=operator.itemgetter(1), reverse=True)
    print sortedMean

def GetJson (user):
    """function that get you the Json format of a user repo"""
    URL_GIT_API_REPOS_BY_USER = 'https://api.github.com/users/%USER%/repos'
    request = urllib2.Request(URL_GIT_API_REPOS_BY_USER.replace('%USER%', user))
    base64string = base64.encodestring('%s:%s' % (GIT_LOGIN, AUTH_KEY)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        response = urllib2.urlopen(request)
        return response.read().strip()
    except urllib2.HTTPError, err:
        if err.code == 404:
            print str(user) + " : repos not found"
        else:
            print "Error " + str(err.code) + " : " + str(err.reason)


master = Tk()

def makeentry(parent, caption, width=None, **options):
    """create an entry login/password"""
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=LEFT)
    return entry

def getinfo():
    """launch the crawling of user and password"""
    return start((user.get(), password.get()))


user = makeentry(master, "Login: ", 10)
password = makeentry(master, "Password: ", 10, show="*")
content = StringVar()
entry = Entry(master)


text = content.get()
content.set(text)
b = Button(master, text="start", width=10, command=getinfo)
b.pack()

master.mainloop()
