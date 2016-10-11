
### EXO SCRAP CDISCOUNT ###

# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup

# sur Cdiscount, qui a les meilleurs remises: les ACER ou les DELL?
nbPages = 1

def countDiscount(brand):
  for page in range(1,nbPages+1):
    url = 'http://www.cdiscount.com/search/10/pc+' + brand + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=14&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=pc%2B' + brand + '&page=' + str(page) + '&_his_'
    page_brand = requests.get(url)
    soup = BeautifulSoup(page_brand.text, 'html.parser')
    #print(soup.prettify())
    ratio = 0

    products = soup.find_all('div', class_='prdtBloc')
    #print(products)

    for product in products:
      try:
        prdtPrSt = product.find_all('div', class_='prdtPrSt')
        ecoBlk =  product.find_all('div', class_='ecoBlk')

        oldPrice = int(round(float(prdtPrSt[0].text.replace(u',','.'))))
        discount = int(ecoBlk[0].text.replace(u'€d\'économie',''))
        ratio += discount/oldPrice
        #print(ratio)
        #print(discount)
        #print(oldPrice)
        break
      except:
        errorMsg = 'no data here'
        #print(errorMsg)
  
  return ratio

def compareBrands(brand1, brand2):
  diff = round(countDiscount(brand1)-countDiscount(brand2), 2)
  text1 = brand1 + ' cheaper with a rate difference of ' + str(diff) + ' euros'
  text2 = brand2 + ' cheaper with a rate difference of ' + str(-diff) + ' euros'
  return text1 if (diff > 0) else text2

#countDiscount('acer')
print(compareBrands('acer', 'dell'))