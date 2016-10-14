import numpy
import requests
from bs4 import BeautifulSoup

# Base url for listing top GitHub contributors.
Gist_git_hub_url = 'https://gist.github.com/paulmillr/2657075'
Git_hub_base_url = "https://github.com/"
Git_hub_user_starred_url = 'https://api.github.com/users/<user>/repos'

# Common HTTP request query parameters, if any
Params = {
    # "access_token": '<token>'
}
# Common HTTP request headers, if any
Headers = {
    # "Authorization": 'token <token>'
}

# Retrieves the names of the top ranked GitHub contributors from Gist GitHub web site;
# returns a list of string names.
def get_user_names(token):
    url = Gist_git_hub_url
    data = requests.get(url)

    results = []
    parser = BeautifulSoup(data.text, 'html.parser')
    article_node = parser.find("article")
    if article_node:
        table_node = article_node.find("table")
        if table_node:
            for a_node in table_node.findAll("a"):
                url = a_node.attrs['href']
                if url.startswith(Git_hub_base_url):
                    results.append(url[len(Git_hub_base_url):])
    return results


# Retrieves the average 'stargazers_count' of the repositories the designated user is registered with (from the GitHub REST API);
# returns the average 'stargazers_count' as a float.
def get_starred_repos(user, token):
    url = Git_hub_user_starred_url.replace('<user>', user)
    # Params['access_token'] = token
    Headers['Authorization'] = 'token ' + token
    r = requests.get(url, params=Params, headers=Headers)
    data = r.json()

    results = [0];
    for i in data:
        if isinstance(i, dict):
            results.append(i["stargazers_count"])
    return numpy.mean(results)

# Retrieves and sorts the top rated GitHub contributors according to their average 'stargazers_count';
# returns a list of tuples <username, count>
def sort_users_by_starred_repos(token):
    results = {}
    for user in get_user_names(token):
        stars = get_starred_repos(user, token)
        # print("%f stars for user %s" % (stars, user))
        results[user] = stars
    return sorted(results.items(), key=lambda x: x[-1], reverse=True)

# Loads an oAuth token from the designated file;
# returns the token as a string.
# The oAuth token must, for example, be obtained via "https://github.com/settings/tokens" and saved in a file locally.
def load_oauth_token(filename):
    with open(filename, 'r') as file:
        token = file.readline().strip()
        return token

# Prints out the provided results (from sort_users_by_starred_repos).
def pretty_print(results):
    for username, average in results:
        print("User: %s = Average StarGazers: %2f" % (username, average))

# Test
pretty_print(sort_users_by_starred_repos(load_oauth_token('GitHub_API_OAuth_token.txt')))
