import requests
from bs4 import BeautifulSoup

urlacer = "http://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-acer.html#_his_"
urldell = "http://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-dell.html#_his_"
html_class = "ecoBlk"


def get_all_remise_for_marque(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    i = 0
    results = []
    while i <= 500:
        try:
            res_str = soup.find_all(class_=html_class)[i].text.replace(u'\xa0', '').replace("€d'économie", "")
            res_int = int(res_str)
            results.append(res_int)
            print(res_int)
        except IndexError:
            break
        i += 1
    return results

remise_acer = get_all_remise_for_marque(urlacer)

remise_dell = get_all_remise_for_marque(urldell)