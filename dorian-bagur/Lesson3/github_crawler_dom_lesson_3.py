import numpy as np
import requests
from bs4 import BeautifulSoup


def getElementWithId(soup, id):
    return soup.find("div", id=id)


def getListContributors(soup):
    return [contributorCell.find_next('td').find("a").text for contributorCell
            in getElementWithId(soup, "readme").find_all('tr')]


def getTopContributors():
    url = "https://gist.github.com/paulmillr/2657075"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return getListContributors(soup)


def displayContributors(contributors):
    [print(contributor) for contributor in contributors]


def getStargazersMean(user):
    url = "https://api.github.com/" + "users/" + user + "/repos"
    print("Getting ", user, "'s repositories")
    res = requests.get(url, auth=('dorianb',
                                  '68d9c3daa088f68b62743a679dba8840e047b158'))
    repos = res.json()
    return np.array([repo['stargazers_count'] or 0 for repo in repos] or 0
                    ).mean()


def getContributorsByStargazersMean(contributors):
    return sorted({contributor: getStargazersMean(contributor) for contributor
                   in contributors}.items(), key=lambda d: d[1])


def displayContributorsWithStargazersMean(contributors):
    [print(contributor, " => ", starMean) for contributor, starMean in
     contributors]


# Get top contributors by scrawling
topContributors = getTopContributors()
displayContributors(topContributors)

# Get top contributors sorted by stargazers mean
topContributorsByStargazersMean = getContributorsByStargazersMean(
    topContributors)
displayContributorsWithStargazersMean(topContributorsByStargazersMean)
