import requests
from bs4 import BeautifulSoup
#
# récuperation de l'URL complété de computer et page étudié
def get_urlcomplete(computer,page):
#    url = "http://www.cdiscount.com/search/10/ordinateur+acer.html#_his_"
    url_debut = "http://www.cdiscount.com/search/10/ordinateur+" + computer + ".html"
    url_s1 = "?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10"
    url_s2 = "&TechnicalForm.ProductId=&hdnPageType=Search"
    url_s3 = "&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX"
    url_s4 = "&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0"
    url_s5 = "&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2"
    url_s6 = "&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5"
    url_s7 = "&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8"
    url_s8 = "&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11"
    url_s9 = "&FacetForm.SelectedFacets.Index=12&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=13"
    url_s10 = "&FacetForm.SelectedFacets.Index=14&SortForm.SelectedNavigationPath=&ProductListTechnicalForm."
    url_s11 = "Keyword=ordinateur%2B" + computer + "&page="
    url_s12 = str(page)
    url_s13 = "&_his_"
    url = url_debut + url_s1 + url_s2 + url_s3 + url_s4 + url_s5 + url_s6 + url_s7 + url_s8 + url_s9 + \
        url_s10 + url_s11 + url_s12 + url_s13
#    print(url)
    return url

def nettoie(text):
    texts = text.replace(u'</sup></span>', '').replace(u'<sup>', '').replace(',', '.')
    return texts

def nettoie_price(text):
    texts = text.replace(u'</sup>', '').replace(u'</span>', '').replace('€', '.')
    return texts

def extract_amounts(node):
    decode = lambda text: int(text.replace(u'xa', '').replace(u' ', ''))
    children = node.parent.findAll(class_="montantpetit G")
    return decode(children[1].text), decode(children[2].text)

def recupere_result(compute,page):
    result = requests.get(get_urlcomplete(compute,page))
    soup = BeautifulSoup(result.text, 'html.parser')
#    print(soup)
    results = {}
    count1 = 0
    count2 = 0
    somme_prix_avant_remise = 0
    somme_prix_apres_remise = 0
    for li in soup.find_all(class_="prdtBZPrice"):
#        print(li)
        children = li.findChildren(class_= "price")
        count1 = count1 + 1
        for child in children :
     #       print("prix R0 :" + child.text)
            text0 = nettoie_price(child.text)
     #       print("prix R1        : " + text0)
        children1 = li.findChildren(class_= "prdtPInfoT")
        count2 = count2 + 1
        for child1 in children1:
         #   print("prix récupéré uniquement si remise : " + child1.text)
            if child1.text == '' :
                text1 = text0
            else:
                text1 = nettoie(child1.text)
     #       print("Prix origine   : " + text1)
            somme_prix_avant_remise = somme_prix_avant_remise + float(text1)
            somme_prix_apres_remise = somme_prix_apres_remise + float(text0)
     #       print("compute" + compute + " : " + text1)
     #       print("compute" + compute + " : " + text0)

    print("+ somme prix apres remise : " + str(round(somme_prix_apres_remise,2)) + "                      -")
    print("+ somme prix avant remise : " + str(round(somme_prix_avant_remise,2)) + "                      -")
    results = round((1- (somme_prix_apres_remise / somme_prix_avant_remise)) * 100, 2)
    resultats = [somme_prix_apres_remise, somme_prix_avant_remise]
    print("Pourcentage de remises " + compute + " pour la page " + str(page) + " : " + str(results) + " % ")
    return resultats


page = 1
pages = [1,2,3]
montants_acer_total_0 = 0
montants_acer_total_1 = 0
montants_dell_total_0 = 0
montants_dell_total_1 = 0
resultats = 0
resultats_dell = 0
for i in pages :
    montants_acer = recupere_result('acer',i)
#    print("Montants  " + " acer : " + str(montants_acer))
    montants_acer_total_0 = montants_acer_total_0 + montants_acer[0]
    montants_acer_total_1 = montants_acer_total_1 + montants_acer[1]
    montants_dell = recupere_result('dell',i)
#    print("Montants " + " dell : " + str(montants_dell))
    montants_dell_total_0 = montants_dell_total_0 + montants_dell[0]
    montants_dell_total_1 = montants_dell_total_1 + montants_dell[1]
print("-------Calcul de la moyenne des remises ------------------")
print("+ Montants acer après remise: " + str(round(montants_acer_total_0,2)) + "                    -")
print("+ Montants acer avant remise: " + str(round(montants_acer_total_1,2)) + "                    -")
results = round((1- (montants_acer_total_0/ montants_acer_total_1)) * 100, 2)
print("+ Montants dell 0 après remise : " + str(round(montants_dell_total_0,2)) + "                 -")
print("+ Montants dell 1 avant remise : " + str(round(montants_dell_total_1,2)) + "                 -")
results_dell = round((1- (montants_dell_total_0/ montants_dell_total_1)) * 100, 2)
print("+ Pourcentage de remises acer : " + str(results) + " % ")
print("+ Pourcentage de remises dell : " + str(results_dell) + " % ")