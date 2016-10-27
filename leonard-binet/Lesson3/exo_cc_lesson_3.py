# coding: utf8
import requests
# import re
from bs4 import BeautifulSoup
# import ipdb
import pandas as pd
# import ipdb


def get_data_for_brand(methode="get", brand="acer", page="2"):
    url = "http://www.cdiscount.com/search/10/ordinateur+"\
        + brand \
        + ".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=15&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=ordinateur%2B"\
        + brand \
        + "&page="\
        + str(page) \
        + "&_his_"

    # filters = {}
    if methode == "get":
        request = requests.get(url)
    elif methode == "post":
        request = requests.post(url)
    else:
        pass
    html = request.text
    soup = BeautifulSoup(html, "html.parser")
    ordinateurs = soup_to_data(soup, brand)
    return ordinateurs


def soup_to_data(soup, brand):
    resultul = soup.find(id="lpBloc")
    li_list = resultul.find_all("li", recursive=False)
    print(" ----- %d éléments" % len(li_list))

    # on créé le dataframe qui renverra les résultats
    columns = ["Marque", "Description", "Prix_apres_resise", "Remise"]
    df_ordinateurs = pd.DataFrame(columns=columns)
    # ipdb.set_trace()
    saved = 0
    for i, li in enumerate(li_list):
        try:
            # ipdb.set_trace()
            nom = li.find(class_="prdtBTit").contents[0]
            # description =
            try:
                prix = li.find(class_="price").contents[0]
                prix = float(prix)
            except:
                prix = np.nan
            try:
                remise = li.div.form.div.find(class_="prdtPrSt")
                remise = remise.contents[0].replace(",", ".")
                remise = float(remise) - prix
            except (IndexError, AttributeError):
                remise = 0
            # ipdb.set_trace()
            ordinateur = Ordinateur(
                nom=nom, marque=brand, remise=remise, prix=prix)
            dfordi = ordinateur.to_df()
            df_ordinateurs = df_ordinateurs.append(dfordi)
            saved += 1
        except AttributeError:
            continue
    print(" ----- %d ordinateurs enregistrés." % saved)
    return df_ordinateurs


class Ordinateur:

    def __init__(self, nom="", prix="", description="", marque="", remise=""):
        self.nom = nom
        self.description = description
        self.prix_apres_resise = prix
        self.remise = remise
        self.marque = marque

    def __str__(self):
        resultat = "------------\n"
        resultat += "Marque: " + str(self.marque) + "\n"
        resultat += "Ordinateur " + str(self.nom) + "\n"
        resultat += "Description " + str(self.description) + "\n"
        resultat += "Prix (après remise): " + \
            str(self.prix_apres_resise) + "\n"
        resultat += "Remise: " + str(self.remise) + "\n"
        return resultat

    def to_df(self):
        columns = ["Marque", "Description", "Prix_apres_resise", "Remise"]
        data = [
            self.marque,
            self.description,
            self.prix_apres_resise,
            self.remise,
        ]
        df = pd.DataFrame([data], columns=columns, index=[self.nom])
        return df


def ordi_list_to_df(ordi_list):
    columns = ["Marque", "Description", "Prix_apres_resise", "Remise"]
    df = pd.DataFrame(columns=columns)
    for ordi in ordi_list:
        print(ordi.nom)
        df = df.append(ordi.to_df())
    return df


def get_pages_brand(pages, brand):
    df = pd.DataFrame()
    for page in pages:
        print("### Page %d de la marque %s ###" % (page, brand))
        dfel = get_data_for_brand(brand=brand, page=page)
        df = df.append(dfel)
        df["pct_remise"] = df.apply(
            lambda x: x.Remise / (x.Remise + x.Prix_apres_resise) * 100, axis=1)
    return df

page_range = list(range(1, 15))


def compare_brand_discounts(brand1="acer", brand2="asus", pages=list(range(1, 5))):
    print("#### COMPARAISON DES MARQUES %s ET %s #######" %
          (brand1.capitalize(), brand2.capitalize()))
    df_brand1 = get_pages_brand(pages, brand1)
    df_brand2 = get_pages_brand(pages, brand2)
    if df_brand1.pct_remise.mean() > df_brand2.pct_remise.mean():
        winner = brand1
        winner_score = df_brand1.pct_remise.mean()
        loser = brand2
        loser_score = df_brand2.pct_remise.mean()
    else:
        winner = brand2
        winner_score = df_brand2.pct_remise.mean()
        loser = brand1
        loser_score = df_brand1.pct_remise.mean()
    print("La marque %s propose les meilleures remises avec un remise moyenne de %.2f pourcents." % (
        winner, winner_score))
    print("Tandis que la marque %s propose une remise moyenne de %.2f pourcents." %
          (loser, loser_score))
    return(df_brand1, df_brand2)
