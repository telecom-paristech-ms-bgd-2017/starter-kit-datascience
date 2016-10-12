"""
Déterminer si ce sont les ordinateurs Dell ou Acer qui ont le plus de reduction sur CDiscount (ie le taux de rabat)
Ce code ne fonctionne que pour les ordinateurs portables
"""

import urllib.request as req
from bs4 import BeautifulSoup


def get_soup(produit, numero_page):
    url = 'http://www.cdiscount.com/search/10/' + produit + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B2%5D=f%2F6%2F' + produit + '&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets%5B6%5D=f%2F8%2Fordinateur+portable&FacetForm.SelectedFacets.Index=7&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=' + produit +'&&page=' + numero_page + '_his_'
    html = req.urlopen(url).read()
    return BeautifulSoup(html, "html.parser")


def get_prix(produit, nombre_pages):
    liste_prix = []

    for i in range(1, nombre_pages + 1):
        soup = get_soup(produit, str(i))
        nombre_ordis = len(soup.select("div.prdtPrSt"))
        index = 0

        while (index < nombre_ordis):
            nom_ordi = soup.select("div.prdtBTit")[index].text
            ancien_prix = soup.select("div.prdtPrSt")[index].text.replace(",", ".")
            nouveau_prix = soup.select("span.price")[index].text.replace("€", ".")
            if not ancien_prix:
                ancien_prix = nouveau_prix
            ordi = {nom_ordi: {ancien_prix, nouveau_prix}}
            liste_prix.append((nom_ordi, float(ancien_prix), float(nouveau_prix)))
            index += 1
    return liste_prix


def calculate_reduction(liste_prix):

    montant_reduction_moyen_tout_portable = 0
    montant_reduction_moyen_portables_remises = 0

    prix_total_sans_reduction = 0
    prix_total_avec_reduction = 0
    nombre_ordis_total = 0
    nombre_ordis_remises = 0

    for prix in liste_prix:
        prix_total_sans_reduction += prix[1]
        prix_total_avec_reduction += prix[2]
        nombre_ordis_total += 1
        if prix[1] > prix[2]:
            nombre_ordis_remises += 1
    montant_reduction_moyen_tout_portable = (prix_total_sans_reduction - prix_total_avec_reduction) / nombre_ordis_total
    montant_reduction_moyen_portables_remises = (
                                              prix_total_sans_reduction - prix_total_avec_reduction) / nombre_ordis_remises

    return ({"Montant réduction moyen tout portable": montant_reduction_moyen_tout_portable,
             "Montant réduction moyen portables remises": montant_reduction_moyen_portables_remises})

if __name__ == '__main__':
    liste_prix_acer = get_prix("acer", 9)
    print("Pour acer voici les infos sur les réductions faites : {0}".format(calculate_reduction(liste_prix_acer)))

    liste_prix_acer = get_prix("dell", 20)
    print("Pour dell voici les infos sur les réductions faites : {0}".format(calculate_reduction(liste_prix_acer)))