import requests
from bs4 import BeautifulSoup


def getElementWithId(soup, id):
    return soup.find("div", id=id)


def getListContributors(soup):
    return [contributorCell.find_next('td').find("a").text for contributorCell in
        getElementWithId(soup, "readme").find_all('tr')]

def getTopContributors():
    url = "https://gist.github.com/paulmillr/2657075"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return getListContributors(soup)


def displayContributors(contributors):
    [print(contributor) for contributor in contributors]

displayContributors(getTopContributors())
