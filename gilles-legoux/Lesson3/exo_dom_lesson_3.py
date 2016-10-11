#!/usr/bin/env python3
"""
Get the mean number of stars among the most active GitHub users.
Persist data in two files:
- data.csv: all repositories for each GitHub contributor
- data-sorted.csv: sorted contributors by mean number of stars by repository.

Run this script without and with -m option, to compare the execution with and
without multiprocessing:

with multiprocessing:
$ time python3 exo_dom_lesson_3.py
real    0m20.682s
user    0m9.668s
sys     0m0.932s

without multiprocessing:
$ time python3 exo_dom_lesson_3.py -m
real    2m3.338s
user    0m4.560s
sys     0m0.648s

With multiprocessing, it is 6 times faster than without.
(with 8 cores and 8 processes)
"""

# standard library imports
import sys
import multiprocessing
import itertools
import json

# related third party imports
import requests
import pandas
from bs4 import BeautifulSoup
from functools import reduce


class ScrapingContributors:
    """
    A utility class to scrap a particular web page to get a set of GitHub
    contributors (the most active users of this year 2016).

    References
    ----------
    https://gist.github.com/paulmillr/2657075.

    """

    def __init__(self):
        pass

    # public methods

    @staticmethod
    def get_contributors():
        """
        Get the list of GitHub Contributors.

        Returns
        -------
        res : list of str
            Several contributor names, precisely theirs GitHub identifiers.

        """
        contributors = []
        url = 'https://gist.github.com/paulmillr/2657075'
        soup = ScrapingContributors._get_soup(url)
        tbody = ScrapingContributors._extract_tbody_elt(soup)
        for tr in ScrapingContributors._extract_tr_elts(tbody):
            contributors.append(ScrapingContributors._get_contributor(tr))
        return contributors

    # private methods

    @staticmethod
    def _get_soup(url):
        text = requests.get(url).text
        return BeautifulSoup(text, 'html.parser')

    @staticmethod
    def _extract_tbody_elt(soup):
        return soup.find('div', {'id': 'readme'}) \
            .find('table') \
            .find('tbody')

    @staticmethod
    def _extract_tr_elts(tbody):
        return tbody.find_all('tr', recursive=False)

    @staticmethod
    def _get_contributor(tr):
        return tr.find_all('td', recursive=False)[0] \
            .find('a').contents[0]


class GitHubAPIv3Client:
    """
    A class to create a client for GitHub API v3.

    References
    ----------
    https://developer.github.com/v3/

    """

    def __init__(self):
        self.login = 'glegoux'
        with open('TOKEN', 'r') as token:
            self.token = token.read()

    # public methods

    def get_repos(self, username):
        """
        Get information about all repositories of one GitHub username
        under raw format.

        Parameters
        ----------
        username : str
            A username, precisely its GitHub identifier.

        Returns
        -------
        raw_data : list of dict objects
            Information about all repositories of this GitHub username.

        References
        ----------
        https://developer.github.com/v3/repos/#list-user-repositories

        """
        return json.loads(
            requests.get(
                'https://api.github.com/users/{}/repos'.format(username),
                auth=(self.login, self.token)
            ).text
        )


class InfoRepo:
    """
    A class to map the raw data from a GitHub repository to python object.

    """

    def __init__(self, all_stars, number_of_repos, mean_of_stars_by_repo):
        self.owner = None
        self.repo_name = None
        self.stars = None
        self.all_stars = all_stars
        self.repos = number_of_repos
        self.mean_of_stars_by_repo = mean_of_stars_by_repo

    # public methods

    def set_info_repo(self, repo):
        self.owner = str(repo['owner']['login'])
        self.repo_name = str(repo['name'])
        self.stars = int(repo['stargazers_count'])


class InfoRepoHelper:
    """
    A utility class to extract and persist information about GitHub repository.

    """

    def __init__(self):
        pass

    # public methods

    @staticmethod
    def get_all_stars(repos):
        """
        Get the total number of stars from raw data matching to a list of
        information about GitHub repository.

        Parameters
        ----------
        repos : raw data
            A list of raw data matching to information about GitHub repository.

        Returns
        -------
        raw_data : int
            Total number of stars.

        """

        def sum_star(repo1, repo2):
            return {
                'stargazers_count':
                    repo1['stargazers_count'] + repo2['stargazers_count']
            }

        all_stars = 0
        if len(repos) > 0:
            all_stars = reduce(sum_star, repos)['stargazers_count']
        return all_stars

    @staticmethod
    def get_mean_of_stars_by_repo(all_stars, number_of_repos):
        """
        Get the total number of stars from raw data matching to a list of
        information about GitHub repository.

        Parameters
        ----------
        all_stars : int
            Total number of stars.
        number_of_repos : int
             Number of repositories.

        Returns
        -------
        mean : floot
            Mean of stars by repository.

        """
        mean_stars_by_repo = 0
        if number_of_repos > 0:
            mean_stars_by_repo = all_stars / number_of_repos
        return mean_stars_by_repo

    @staticmethod
    def persist(info_repos):
        """
        Persist data in a csv file named 'data.csv'.

        Parameters
        ----------
        info_repos : list of dicts under the shape of InfoRepo object
            List of dicts under the shape of InfoRepo object.

        Returns
        -------
        df : pandas.DataFrame
            A data frame with its columns matching to attributs of InfoRepo
            object'.

        """
        if len(info_repos) == 0:
            return pandas.DataFrame()
        df = pandas.DataFrame(
            info_repos,
            columns=list(info_repos[0].keys())
        )
        df.to_csv('data.csv', index=False)
        return df

    @staticmethod
    def rank_contributors(df):
        """
        Sort data frame by 'mean_of_stars_by_repo' column in decreasing order.
        Then persist data in a csv file named 'data-sorted.csv'.

        Parameters
        ----------
        df : pandas.DataFrame
            A data frame matching with a list of InfoRepo objects.

        Returns
        -------
        df : pandas.DataFrame
            A copied data frame with this columns ['owner', 'all_stars',
            'repos', 'mean_of_stars_by_repo'] and saved into 'data.csv'.

        """
        dff = pandas.DataFrame.copy(df)
        dff.drop_duplicates(subset=['owner'], inplace=True)
        dff.sort_values(by=['mean_of_stars_by_repo'],
                        ascending=False,
                        inplace=True)
        dff = dff[['owner', 'all_stars', 'repos', 'mean_of_stars_by_repo']]
        dff.to_csv('data-sorted.csv', index=False)
        return dff


def get_info_users(usernames, is_multiprocessing=False):
    """
    Get information about all repositories of several GitHub contributors.

    Parameters
    ----------
    contributors : list of str
        Several contributor names, precisely theirs GitHub identifiers.
    multiprocessing :  bool
        If True run in multiprocessing (default False)

    Returns
    -------
    info_repos : list of dicts under the shape of InfoRepo object
        List of dicts under the shape of InfoRepo object.

    See Also
    --------
    InfoRepo, get_info_contributor

    """
    if is_multiprocessing:
        # BUG: Recursion Error: maximum recursion depth exceeded
        # for multiprocessing library, increase this limit
        # by default it was 1000
        recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(10 ** 6)
        num_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=num_cores)
        info_repos = pool.map(get_info_user, tuple(usernames))
        sys.setrecursionlimit(recursion_limit)
        return list(itertools.chain.from_iterable(info_repos))
    else:
        info_repos = []
        for username in usernames:
            info_repos.extend(get_info_user(username))
        return info_repos


def get_info_user(username, verbose=True):
    """
    Get information about all repositories of one GitHub contributor.

    Parameters
    ----------
    contributor : str
        A contributor name, precisely its GitHub identifier.
    verbose: bool
        if True display traces (default True).

    Returns
    -------
    info_repos : list of dicts under the shape of InfoRepo object
        List of dicts under the shape of InfoRepo object.


    See Also
    --------
    InfoRepo, get_info_contributors.

    """
    info_repos = []
    client = GitHubAPIv3Client()
    repos = client.get_repos(username)
    number_of_repos = len(repos)
    all_stars = InfoRepoHelper.get_all_stars(repos)
    mean_of_stars_by_repo = InfoRepoHelper. \
        get_mean_of_stars_by_repo(all_stars, number_of_repos)
    for repo in repos:
        info_repo = InfoRepo(all_stars,
                             number_of_repos,
                             mean_of_stars_by_repo)
        info_repo.set_info_repo(repo)
        info_repos.append(info_repo.__dict__)
        if verbose:
            print('#', end='')
    if verbose:
        print(username)
    return info_repos


if __name__ == "__main__":

    def print_usage():
        print('usage: python3 {} [-m|--multiprocessing]'.format(sys.argv[0]))
        sys.exit(1)

    args = sys.argv[1:]
    if len(args) > 1:
        print_usage()
    if len(args) == 1 and args[0] not in ['-m', '--multiprocessing']:
        print_usage()

    is_multiprocessing = False
    if len(args) == 1 and args[0] in ['-m', '--multiprocessing']:
        is_multiprocessing = True

    print('Get information about most active GitHub contributors')
    print('It takes a bit of time ....')
    contributors = ScrapingContributors.get_contributors()
    info_repos = get_info_users(contributors, is_multiprocessing)
    df = InfoRepoHelper.persist(info_repos)
    InfoRepoHelper.rank_contributors(df)
    print('It is over!')
