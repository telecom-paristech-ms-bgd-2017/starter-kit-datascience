import requests
import urllib2, base64
import operator, json, re, sys

URL_GIT_USERS = 'https://gist.github.com/paulmillr/2657075'
URL_GIT_API_REPOS_BY_USER = 'https://api.github.com/users/%USER%/repos'
GIT_LOGIN = 'Sbargaoui'
AUTH_KEY = '47474e4ee531c426e91b3708c8b90b0830359a77'
NB_USERS = 256

def getJson (user):
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

htmlText = requests.get(URL_GIT_USERS).text.encode('utf-8')
allUsers = re.findall('<td><a href="https://github.com/(.*?)">', htmlText, re.S) or None
if not allUsers:
	print 'No users found'
	sys.exit()

#L'utilisatrice 'jfrazelle' n'a plus de repos sur son Git, elle cree une erreur
allUsers = allUsers[0:111]+allUsers[113:NB_USERS]

Mean = {}
for user in allUsers:
	allReposJson = getJson(user)
	if allReposJson:
		allRepos = json.loads(allReposJson)
		sum = 0.0
		for repo in allRepos:
			sum += repo['stargazers_count']
		Mean[user] = sum / len(allRepos)
		print str(user) + " : " + str(Mean[user])

sortedMean = sorted(Mean.items(), key=operator.itemgetter(1), reverse=True)
print sortedMean