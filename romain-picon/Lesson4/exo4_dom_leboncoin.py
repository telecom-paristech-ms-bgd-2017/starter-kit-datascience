# Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes :
# version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire,
# est ce que la voiture est vendue par un professionnel ou un particulier.
#
# Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez
# sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.
#
# Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
# Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿

import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

debug_this_sh = True

# The content of our DF.
COL_ARG_EDITION = "Edition"
COL_ARG_PRIX_NEUF = "Prix Neuf"
COL_ARG_COTE = "Cote Brut"
COL_ARG_KM_AN = "pour KM annuel"
COL_ARG_COMMENTAIRE = "Commentaire"
COL_ARG_YEAR = "Year"

COL_LBC_VERSION = "Description ZOE"
COL_LBC_KILOMETRAGE = "Kilometrage"
COL_LBC_PRIX_ANNONCE = "Prix"
COL_LBC_VENDEUR_PRO = "Pro"
COL_LBC_ANNEE = "Annee"
COL_LBC_REGION = "Region"
COL_LBC_TEL = "Telephone"
COL_LBC_ARGUS = "Argus 6920 KMAn"
COL_LBC_ARGUS_ADJUST = "Argus Ajuste"
COL_LBC_APPELATION = "Argus Appelation"

def adjust_argus(year, argus, km, kmyear):
    car_age = 2017-year
    theorical_km = car_age * kmyear
    delta_km = km - theorical_km

    if delta_km >= 200000:
        delta_km = 200000
    if delta_km <= -20000:
        delta_km = -200000

    if delta_km >= 0:
        ret = argus * (1 - 0.005 * delta_km / 1000)
    else :
        ret =  argus * (1 - 0.0025 * delta_km / 1000)

    return int(round(ret))


def score_version(annonce, cote):
    """
    :param annonce: an array of all words in the annonce description ['Zoe', 'Zen', 'Renault', 'Voiture']
    :param cote: an array of all words in the cote description ['Zoe', 'Zen']
    :return: the matching score (here it will be 2)
    """
    score = 0
    for word in annonce:
        if word in cote:
            score = score + 1

    return score

def match_words(cote, words_annonce):

    cote = cote.strip()
    words_cote = cote.split(' ')

    return score_version(words_annonce, words_cote)


def clean_string_to_float(in_string):
    """
    :param in_string: the string to clean, like "13€32" or "13,32" or "13 456 KM"
    :return: 13.32 or 13456 or 0 if the conversion failed.
    """
    if len(in_string) > 0:
        out_string = in_string.replace(',', '.')
        out_string = out_string.replace(' ', '')
        out_string = out_string.replace('€', '.')
        out_string = out_string.replace('KM', '')
        res = re.findall('\d+', out_string)
        if len(res) > 0:
            out_string = res[0]
        else:
            out_string = '0'
    else:
        out_string = '0'

    return out_string


def stamp_filename(filename, extension='.csv'):
    return filename + time.strftime('%d%m%y%H%M%S', time.localtime()) + extension


def remove_accent(text):
    """ supprime les accents du texte source """
    accent = {'é':'e', 'è':'e', 'ê':'e', 'à':'a', 'ù':'u', 'û':'u', 'ç':'c', 'ô':'o', 'î':'i', 'ï':'i', 'â':'a'}

    for key, value in accent.items():
        text = text.replace(key, value)

    return text

def view_tag(tag, n=0):
    """
    For debug, display tag content.
    """

    print(n * '\t' + '--------Tag--------')
    print(n * '\t', tag)
    print(n * '\t', '--------Tag Attributes--------')
    print(n * '\t', tag.attrs)
    print(n * '\t', '--------Tag String--------')
    print(n * '\t', tag.string)


def get_cote_zoe():

    # DF creation
    df_cote_zoe = pd.DataFrame(columns=[COL_ARG_EDITION, COL_ARG_PRIX_NEUF, COL_ARG_COTE, COL_ARG_KM_AN,
                                        COL_ARG_COMMENTAIRE, COL_ARG_YEAR])
    df_line_nb = -1

    # 2 URL
    URL_CENTRALE_YEAR = "http://www.lacentrale.fr/cote-voitures-renault-zoe--{}-.html"
    URL_CENTRALE_COTE = "http://www.lacentrale.fr/{}"

    # Create soup

    print("Connecting to La Centrale ...")

    for YEAR_PARSING in list(map(str, range(2012, 2017))):

        # Main page
        soup_main = BeautifulSoup(requests.get(URL_CENTRALE_YEAR.format(YEAR_PARSING)).text, "html.parser")

        # Find the table in the page
        for tag_table in soup_main.find_all("div", {"class": "listingResultLine f14 auto"}):

            for a in tag_table.find_all("a", href=True):
                # Create soup
                soup_alatomate = BeautifulSoup(requests.get(URL_CENTRALE_COTE.format(a['href'])).text, "html.parser")

                # Version of the car
                for h1 in soup_alatomate.find_all("h1", {"class": "mainTitle inlineBlock vTop mT30 mL10 lH20"}):
                    for span in h1.find_all("span", {"class": "txtGrey58 f14 noBold"}):
                        # As soon we have a name a create a new line
                        print("Getting information for ", span.get_text())
                        df_line_nb = df_line_nb + 1
                        df_cote_zoe.loc[df_line_nb, COL_ARG_EDITION] = span.get_text().strip()
                        df_cote_zoe.loc[df_line_nb, COL_ARG_YEAR] = int(YEAR_PARSING)
                        df_cote_zoe.loc[df_line_nb, COL_ARG_COMMENTAIRE] = "Renault, tous les jours un bruit nouveau."

                # Extract the current cote
                for div in soup_alatomate.find_all("div", {"class": "boxQuot clearPhone"}):

                    # First table
                    for div_txtC in div.find_all("div", {"class": "txtC"}):
                        # Cote brute
                        for h2_cote_brute in div_txtC.find_all("h2", {"class": "f24 inlineBlock"}):
                            if "brute" in h2_cote_brute.get_text():
                                for strong in div_txtC.find_all("strong", {"class": "f24 bGrey9L txtRed pL15 mL15"}):
                                    df_cote_zoe.loc[df_line_nb, COL_ARG_COTE] = float(
                                        clean_string_to_float(strong.get_text()))
                        # KM / An
                        for div_km in div_txtC.find_all("div", {"class": "f14 bold mT10 txtC"}):
                            df_cote_zoe.loc[df_line_nb, COL_ARG_KM_AN] = float(clean_string_to_float(div_km.get_text()))

                    # Prix neuf
                    for div_prix_neuf in div.find_all("div", {"class": "txtC mT60 f20 flexCont flexCenter"}):
                        for strong_prix_neuf in div_prix_neuf.find_all("strong", {"class": "mL15"}):
                            df_cote_zoe.loc[df_line_nb, COL_ARG_PRIX_NEUF] = float(
                                clean_string_to_float(strong_prix_neuf.get_text()))

    print("Cote des Renault ZOE")
#    print(df_cote_zoe)
    df_cote_zoe.to_csv(stamp_filename("renault_zoe_cote"))

    return df_cote_zoe


def get_list_zoe(df_cote):


    df_leboncoin = pd.DataFrame(
        columns=[COL_LBC_VERSION, COL_LBC_KILOMETRAGE, COL_LBC_ANNEE,
                 COL_LBC_PRIX_ANNONCE, COL_LBC_VENDEUR_PRO, COL_LBC_REGION,
                 COL_LBC_TEL, COL_LBC_ARGUS, COL_LBC_ARGUS_ADJUST, COL_LBC_APPELATION])
    df_line_nb = -1

    # https://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&brd=Renault&mdl=Zoe
    URL_LE_BONCOIN = "https://www.leboncoin.fr/voitures/offres/{}/?o={}&brd={}&mdl={}"

    REGION_LIST = ["ile_de_france", "provence_alpes_cote_d_azur", "aquitaine"]
#    REGION_LIST = [ "aquitaine"]

    print("Connecting to LeBonCoin ...")

    for REGION in REGION_LIST:

        # Main page
        PAGE = 1
        PAGE_NB = 1

        while PAGE <= PAGE_NB:

            soup_main = BeautifulSoup(requests.get(URL_LE_BONCOIN.format(REGION, PAGE, 'Renault', 'Zoe')).text,
                                      "html.parser")

            if PAGE == 1:
                for span_page in soup_main.find_all("span", {"class": "total_page"}):
                    PAGE_NB = int(span_page.get_text())

            for li in soup_main.find_all("li"):
                for a_link in li.find_all("a", href=True):
                    # Select just specific links
                    if "www.leboncoin.fr/voitures/10" in a_link["href"]:
                        # Create soup
                        soup_alapatate = BeautifulSoup(requests.get("http:{}".format(a_link['href'])).text,
                                                       "html.parser")

                        df_line_nb = df_line_nb + 1
                        df_leboncoin.loc[df_line_nb, COL_LBC_VENDEUR_PRO] = 0
                        df_leboncoin.loc[df_line_nb, COL_LBC_REGION] = REGION

                        for is_pro in soup_alapatate.find_all("span", {"class": "ispro"}):
                            df_leboncoin.loc[df_line_nb, COL_LBC_VENDEUR_PRO] = 1

                        for section in soup_alapatate.find_all("section",
                                                               {"class": "adview block-white flex-item-first"}):

                            h1_title = section.find_all("h1", {"class": "no-border"})
                            title = h1_title[0].get_text()
                            title = title.strip()
                            title = remove_accent(title)
                            title = title.upper()
                            df_leboncoin.loc[df_line_nb, COL_LBC_VERSION] = title

                            for h2_price in soup_alapatate.find_all("h2", {"itemprop": "price"}):
                                df_leboncoin.loc[df_line_nb, COL_LBC_PRIX_ANNONCE] = int(h2_price["content"])

                            for span_release_date in soup_alapatate.find_all("span", {"itemprop": "releaseDate"}):
                                df_leboncoin.loc[df_line_nb, COL_LBC_ANNEE] = int(span_release_date.get_text().strip())

                            for elem in soup_alapatate(text="Kilométrage"):
                                line_km = elem.parent.parent
                                for val_km in line_km.find_all("span", {"class": "value"}):
                                    df_leboncoin.loc[df_line_nb, COL_LBC_KILOMETRAGE] = int(
                                        clean_string_to_float(val_km.get_text()))

                            for elem in soup_alapatate.find_all("p", {"itemprop":"description"}):
                                text = elem.get_text()
                                phone_number = re.findall(
                                    "[0][0-9]{9}|[0][0-9]\s[0-9]{2}\s[0-9]{2}\s[0-9]{2}\s[0-9]{2}|[0][0-9][.][0-9]{2}[.][0-9]{2}[.][0-9]{2}[.][0-9]{2}",
                                    text)

                                if len(phone_number) > 0:
                                    df_leboncoin.loc[df_line_nb, COL_LBC_TEL] = phone_number[0]


            PAGE = PAGE + 1


    # Get the mean price

    for index_leboncoin, row_leboncoin in df_leboncoin.iterrows():
        # Create an extract of the cote with only the relevant year.
        df_cote_tmp = df_cote[df_cote[COL_ARG_YEAR] == row_leboncoin[COL_LBC_ANNEE]]

        # Car name, a in LBC description
        car_name = row_leboncoin[COL_LBC_VERSION]
        # All words, to prepare the matching.
        words_annonce = car_name.split(' ')

        # They will contain the best matching version name.
        best_score = 0
        best_index = 0

        # Go through all version
        for index_cote, row_cote in df_cote_tmp.iterrows():

            cote = row_cote[COL_ARG_EDITION]
            score = match_words(cote, words_annonce)
            if score >= best_score:
                best_score = score
                best_index = index_cote

        df_leboncoin.loc[index_leboncoin, COL_LBC_ARGUS] = df_cote_tmp.loc[best_index, COL_ARG_COTE]
        df_leboncoin.loc[index_leboncoin, COL_LBC_APPELATION] = df_cote_tmp.loc[best_index, COL_ARG_EDITION]
        df_leboncoin.loc[index_leboncoin, COL_LBC_ARGUS_ADJUST] = adjust_argus(
            row_leboncoin[COL_LBC_ANNEE], df_cote_tmp.loc[best_index, COL_ARG_COTE],
            row_leboncoin[COL_LBC_KILOMETRAGE], 6920)

    print("Liste des Renault ZOE")
#    print(df_leboncoin)

    df_leboncoin.to_csv(stamp_filename("renault_zoe_leboncoin"))

    return df_leboncoin


df_cote = get_cote_zoe()
df_cars = get_list_zoe(df_cote)
