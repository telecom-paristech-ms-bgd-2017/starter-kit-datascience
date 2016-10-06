import requests
from bs4 import BeautifulSoup


def all_balise(url, balise):
    lien = requests.get(url)
    soup = BeautifulSoup(lien.text, 'html.parser')
    return soup.find_all(balise)


def ExtractFromTd(td_all):
    param = {}
    for i in range(0, len(td_all)):
        try:
            if td_all[i]['class'] == ['libellepetit', 'G']:
                param[td_all[i].text] = td_all[i - 1].text.replace('\xa0')
                print("\n  " + td_all[i].text + " est de " + td_all[i - 1].text.replace('\xa0',
                                                                                        '') + " euros par habitant\n")

            if td_all[i]['class'] == ['libellepetit']:
                param[td_all[i].text] = td_all[i - 1].text.replace('\xa0')
                print("     " + td_all[i].text + " est de " + td_all[i - 1].text.replace('\xa0',
                                                                                         '') + " euros par habitant")

            if (td_all[i]['class'] == ['libellepetitIi']) or (td_all[i]['class'] == ['libellepetitiI']):
                param[td_all[i].text] = td_all[i - 1].text.replace('\xa0')
                print("            " + td_all[i].text + " est de " + td_all[i - 1].text.replace('\xa0',
                                                                                                '') + " euros par habitant")

        except KeyError:
            continue
    return param


def sample_extract_dom(years):
    for year in years:
        print("                           Exercice : " + str(year))
        try:
            url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(
                year)
            ExtractFromTd(all_balise(url, 'td'))
        except IndexError:
            print('\n Lien non valide')


if __name__ == "__main__":
    sample_extract_dom(range(2009, 2015))


