# -*- coding: utf-8 -*-

import requests
import bs4
import os

def URL(MARQUE, PAGE):
    if MARQUE == "DELL":
        return "http://www.cdiscount.com/search/10/ordinateurs.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B2%5D=f%2F6%2Facer&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=ordinateurs&"+str(PAGE)+"&_his_"
    elif MARQUE  == "ACER":
        return "http://www.cdiscount.com/search/10/ordinateurs.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B2%5D=f%2F6%2Fdell&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=ordinateurs&"+str(PAGE)+"&_his_"

def analyser(MARQUE, MAXPAGE):
    COUT_TOTAL = 0
    COUT_TOTAL_APRES_REDUCTION = 0
    print "Marque "+MARQUE+" : seules les "+str(MAXPAGE) + " premières pages de résultats seront analysées."

    for PAGE in range(0, MAXPAGE):
        COUT_TOTAL_PAGE, COUT_TOTAL_PAGE_APRES_REDUCTION = analyserPage(MARQUE, PAGE)
        COUT_TOTAL += COUT_TOTAL_PAGE
        COUT_TOTAL_APRES_REDUCTION += COUT_TOTAL_PAGE_APRES_REDUCTION

    return COUT_TOTAL, COUT_TOTAL_APRES_REDUCTION, 1-(COUT_TOTAL_APRES_REDUCTION)/COUT_TOTAL

def analyserPage(MARQUE, PAGE):

    R = requests.get(URL(MARQUE, PAGE))
    soup = bs4.BeautifulSoup(R.content, 'html.parser')

    COUT_TOTAL_PAGE = 0
    COUT_TOTAL_PAGE_APRES_REDUCTION = 0

    a = soup.find_all("div", class_="prdtBloc")

    for produit in range(0, len(a)):
        PRIX_APRES_PROMO_0 = escapeandint(a[produit].find(class_="prdtPrice").text.split(u"\u20AC")[0])
        PRIX_APRES_PROMO_1 = escapeandint(a[produit].find(class_="prdtPrice").text.split(u"\u20AC")[1])
        PRIX_APRES_PROMO = float(PRIX_APRES_PROMO_0) + float(PRIX_APRES_PROMO_1)/100

        try:
            PRIX_AVANT_PROMO = int(a[produit].find(class_="prdtPrSt").text.split(",")[0].replace(u'','').replace(' ',''))
        except AttributeError:
            PRIX_AVANT_PROMO = PRIX_APRES_PROMO
        except ValueError:
            PRIX_AVANT_PROMO = PRIX_APRES_PROMO

        COUT_TOTAL_PAGE += PRIX_AVANT_PROMO
        COUT_TOTAL_PAGE_APRES_REDUCTION += PRIX_APRES_PROMO

    print("Page "+str(PAGE+1)+" pour la marque "+MARQUE+" terminée.")
    return COUT_TOTAL_PAGE, COUT_TOTAL_PAGE_APRES_REDUCTION

def escapeandint(s):
    try:
        ss = int(s.replace(u'','').replace(' ',''))
        return ss
    except ValueError:
        print "Erreur de conversion !"

##################
# ACER OU DELL ? #
##################

RESACER = analyser("ACER", 20)
RESDELL = analyser("DELL", 20)
if RESACER[2] <= RESDELL [2]: GAGNANT = "DELL"
elif RESACER[2] > RESDELL [2]: GAGNANT = "ACER"
print "Le pourcentage moyen de réduction chez ACER est "+str(round(100.0*RESACER[2],2))+"%."
print "Le pourcentage moyen de réduction chez DELL est "+str(round(100.0*RESDELL[2],2))+"%."
print "Marque qui bénéficie de la réduction la plus importante : "+GAGNANT