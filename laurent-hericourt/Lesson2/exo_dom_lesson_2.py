import urllib.request as req
from bs4 import BeautifulSoup
import operator

# Position des cellules "Euros par habitant" qui nous intéressent
position_abcd = {
    "A": 1,
    "B": 20,
    "C": 53,
    "D": 77
}


def get_soup(year):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=118&dep=014&type=BPS&param=5&exercice=" + str(
            year)
    html = req.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_values_abcd(soup):
    values_abcd = {}

    for key, value in position_abcd.items():
        values_abcd["Euros par habitant pour " + key] = soup.select("tr.bleu > td.montantpetit")[value].text.replace(
            u'\xa0', '')
        values_abcd["Moyenne de la strate pour " + key] = soup.select("tr.bleu > td.montantpetit")[
            value + 1].text.replace(
                u'\xa0', '')

    return sorted(values_abcd.items(), key=operator.itemgetter(0))


def display_result(period):
    for year in range(period[0], period[1] + 1):
        print("\nVoici les résultat de l'année : " + str(year))
        print("-------------------------------------")
        results = get_values_abcd(get_soup(year))
        for result in results:
            print(result[0] + " : " + result[1])


def main():
    display_result([2009, 2013])


if __name__ == '__main__':
    main()
