############################ SCRAP GITHUB biggest users ##############################

# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup

def getDevs(maxUsers):
  devs_list = []
  url = 'https://gist.github.com/paulmillr/2657075'
  page_developers = requests.get(url)
  soup = BeautifulSoup(page_developers.text, 'html.parser')
  #soup.prettify()
  devs = soup.select('tbody tr')

  # Loop over 256 developers of the table body
  for idx, dev in enumerate(devs[:maxUsers]):

    try:
      #print(dev.select('td:nth-of-type(1) a')[0].text + ' : ' + str(idx+1))
      devs_list.append(dev.select('td:nth-of-type(1) a')[0].text)

    except Exception as e:
      print(str(e) + '    ####################################################################')
      print('error caused by : ' + str(dev.select('td:nth-of-type(1)')))

  return devs_list

#print(getDevs(256))

############################ GITHUB API SCRAPING ##############################

# get User profile
def get_Profile(access_token, urlUser):
  headers = {"Authorization": "token " + access_token}
  response = requests.get(urlUser, headers=headers)
  me_json = response.json()
  return me_json

def get_DevScore(usersList):
  # get devs' mean of stars for their repos
  for idx, pseudo in enumerate(usersList):

    my_token = 'WRITE YOUR TOKEN HERE'
    urlUser = 'https://api.github.com/users/' + pseudo + '/repos'
    starsCount = 0
    devData = {}
    profile = get_Profile(my_token, urlUser)

    # count stars total
    for val in profile:
      starsCount += val['stargazers_count']

    # register mean
    StarsMean = starsCount / len(profile)
    devData['pseudo'] = pseudo
    devData['rank'] = idx + 1
    devData['meanStars'] = StarsMean
    print('this dev has these data : ')
    print(devData)

  return

# print out devs data (scores included)
ListOfDevs = getDevs(256)
get_DevScore(ListOfDevs)

