# coding: utf8
import requests
# import re
from bs4 import BeautifulSoup
# import ipdb
import pandas as pd
import ipdb


def get_data_for_brand(methode="get", brand="acer"):
    url = "http://www.cdiscount.com/search/10/ordinateur+portable+" + brand + \
        ".html?NavigationForm.CurrentSelectedNavigationPath%3Df%2F1%2F0k%2" + \
        "F0k%7C0k0c%7C0k0c01#_his_"
    # filters = {}
    if methode == "get":
        request = requests.get(url)
    elif methode == "post":
        request = requests.post(url)
    else:
        pass
    html = request.text
    soup = BeautifulSoup(html, "html.parser")
    ipdb.set_trace()
    ordinateurs = soup_to_data(soup, brand)
    return ordinateurs


def soup_to_data(soup, brand):
    resultul = soup.find(id="lpBloc")
    ordinateurs = []
    try:
        for li in resultul:
            # ipdb.set_trace()
            nom = li.find(class_="prdtBTit").contents[0]
            # description =
            prix = li.div.form.div.find(class_="price").contents[0]
            prix = float(prix)
            remise = li.div.form.div.find(class_="prdtPrSt")
            remise = remise.contents[0].replace(",", ".")
            remise = float(remise) - prix
            # ipdb.set_trace()
            ordinateur = Ordinateur(
                nom=nom, marque=brand, remise=remise, prix=prix)
            ordinateurs.append(ordinateur)
    except IndexError:
        pass
    return ordinateurs


class Ordinateur:

    def __init__(self, nom="", prix="", description="", marque="", remise=""):
        self.nom = nom
        self.description = description
        self.prix = prix
        self.remise = remise
        self.marque = marque

    def __str__(self):
        resultat = "------------\n"
        resultat += "Marque: " + str(self.marque) + "\n"
        resultat += "Ordinateur " + str(self.nom) + "\n"
        resultat += "Description " + str(self.description) + "\n"
        resultat += "Prix: " + str(self.prix) + "\n"
        resultat += "Remise: " + str(self.remise) + "\n"
        return resultat

    def to_df(self):
        columns = ["Nom", "Marque", "Description", "Prix", "Remise"]
        data = [
            self.nom,
            self.marque,
            self.description,
            self.prix,
            self.remise,
        ]
        df = pd.DataFrame([data], columns=columns)
        return df


def ordi_list_to_df(ordi_list):
    columns = ["Nom", "Marque", "Description", "Prix", "Remise"]
    df = pd.DataFrame(columns=columns)
    for ordi in ordi_list:
        print(ordi.nom)
        df = df.append(ordi.to_df(), ignore_index=True)
    return df
