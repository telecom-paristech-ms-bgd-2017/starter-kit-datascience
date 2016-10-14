from urllib.request import urlopen
from bs4 import BeautifulSoup


# load page and return soup
def get_page():
    url = 'http://www.cdiscount.com/search/10/dell.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B2%5D=f%2F6%2Fdell&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets%5B3%5D=f%2F8%2Fordinateur+portable&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=dell&&_his_'
    data = urlopen(url)
    soup = BeautifulSoup(data, "lxml")
    return soup


# returns list of products with for each one the initial price and the last price
list0 = get_page().findAll("div", {"class": "prdtBZPrice"})
list1 = get_page().find_all(class_='prdtBZPrice')
print(list0)
print(list1)
