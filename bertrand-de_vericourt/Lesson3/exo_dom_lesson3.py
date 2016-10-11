
###  SCRZAP GITHUB biggest users ###

# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup

devs_list = []

url = 'https://gist.github.com/paulmillr/2657075'
page_developers = requests.get(url)
soup = BeautifulSoup(page_developers.text, 'html.parser')
soup.prettify()
devs = soup.select('tbody tr')


# Loop over 256 developers of the table body
for idx, dev in enumerate(devs[:256]):

  try:
    #print(dev.select('td:nth-of-type(1) a')[0].text + ' : ' + str(idx+1))
    #devs_list.append(dev.select('td:nth-of-type(1) a')[0].text)

  except Exception as e:
    #print(str(e) + '    ####################################################################')
    #print('error caused by : ' + str(dev.select('td:nth-of-type(1)')))


############################ CONNECTING TO THE API ############################
# get library for API OAuth2
from requests_oauthlib import OAuth2Session

# open a session
github = OAuth2Session(client_id)

# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
github.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

############################ EXPLOITING THE API ############################
for pseudo in devs_list

  urlUser = 'https://api.github.com/users/' + pseudo + '/repos'
  auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')

  # Fetch a protected resource, here: repos data from the developer account
  r = requests.get(urlUser, auth=auth)
  print(r.content)



# stargazers_count



###########################
"""

SOURCE : https://requests-oauthlib.readthedocs.io/en/latest/examples/github.html
Setup credentials following the instructions on GitHub. When you have obtained a client_id and a client_secret you can try out the command line interactive example below.

# Credentials you get from registering a new application
client_id = '<the id you get from github>'
client_secret = '<the secret you get from github>'

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

from requests_oauthlib import OAuth2Session
github = OAuth2Session(client_id)

# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
github.fetch_token(token_url, client_secret=client_secret,
        authorization_response=redirect_response)

# Fetch a protected resource, i.e. user profile
r = github.get('https://api.github.com/user')
print r.content

"""