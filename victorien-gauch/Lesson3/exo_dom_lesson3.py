import requests
from bs4 import BeautifulSoup

dell_reduction = []
acer = []

def getData(marque,page):

	url = requests.get('http://www.cdiscount.com/search/10/'+marque+'.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword='+marque+'&page='+str(page)+'&_his_')
	soup = BeautifulSoup(url.text,'html.parser')
	pc = soup.find_all(class_="prdtBloc")
	return pc


def parcourir(marque,page):

	for j in marque:	

		for i in page:
			
			pc = getData(j,i)
			
			for el in pc:
				if el.find(class_="prdtPrSt") == None:
					dell_reduction.append(0)
				else:
					dell_reduction.append(float(el.find(class_="prdtPrice").text.replace('€','.')) / float(el.find(class_="prdtPrSt").text.replace(',','.')))

				somme = 0
				for el in dell_reduction:
					somme += el
					moyenne = somme / len(dell_reduction)

	print(moyenne * 100)

parcourir(['dell'],[1,2,3])




	





