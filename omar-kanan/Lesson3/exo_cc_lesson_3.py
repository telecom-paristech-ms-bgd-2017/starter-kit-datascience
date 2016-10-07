import requests
from bs4 import BeautifulSoup as bs

url_incomplete = 'http://www.cdiscount.com/search/10/ordinateur'
end_url = '.html#_his_'
brands = ['acer', 'dell']
data = {'acer': [], 'dell': []}
results = {}

for brand in brands:
    request = requests.get(url_incomplete + brand + end_url)
    soup = bs(request.text, 'html.parser')

    number_of_pcs = len(soup.select("li"))
    soup.find_all(id="lpBloc")
    spans = soup.select("li > div > a > div > span")

    for span in spans:
        data[brand].append(int(span.text.strip()[:-1]))

    results[brand] = sum(data[brand]) / number_of_pcs

print(results)
