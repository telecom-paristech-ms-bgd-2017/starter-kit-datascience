def gettotaleurosparhabitant(soup):
    results = {}
    total_produit_fonctionnement = soup.find_all(class_="bleu")[3].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["A"] = total_produit_fonctionnement
    total_produit_fonctionnement = soup.find_all(class_="bleu")[7].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["B"] = total_produit_fonctionnement
    total_ressource_investissement = soup.find_all(class_="bleu")[15].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["C"] = total_ressource_investissement
    total_emploi_investisstement = soup.find_all(class_="bleu")[20].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["D"] = total_emploi_investisstement
    return results


def gettotaleurosparhabitant2(soup):
    results = {}
    total_produit_fonctionnement = soup.find_all(class_="bleu")[3].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["A"] = total_produit_fonctionnement
    total_produit_fonctionnement = soup.find_all(class_="bleu")[7].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["B"] = total_produit_fonctionnement
    total_ressource_investissement = soup.find_all(class_="bleu")[15].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["C"] = total_ressource_investissement
    total_emploi_investisstement = soup.find_all(class_="bleu")[20].find_all(class_="montantpetit G")[0].text.replace(u'\xa0','')
    results["D"] = total_emploi_investisstement
    return results


def getmoyenneparstrateforyears(years):
    resultsperyear = []
    for d in years:
        finalurl = baseurl + str(d)
        results_from_request = requests.get(finalurl)
        soup = BeautifulSoup(results_from_request.text, 'html.parser')
        resultsperyear.append(getmoyenneparstrate(soup))
    return resultsperyear