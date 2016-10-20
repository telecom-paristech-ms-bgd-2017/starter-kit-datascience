import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

pattern_year = "[0-9]{4}"
re_year = re.compile(pattern_year)
pattern_km = "[0-9]{1,20}"
re_km = re.compile(pattern_km)
pattern_city = "[A-Z._ %+-]{1,100}"
re_city = re.compile(pattern_city, flags=re.IGNORECASE)
pattern_type = "(zen|life|intens)"
re_type = re.compile(pattern_type, flags = re.IGNORECASE)
pattern_phone = "([+0-9]{11}|[0-9]{10})"
re_phone = re.compile(pattern_phone)

base_url = "https://www.leboncoin.fr/voitures/offres/"
page_url = "/?o="
search_url = "&q=renault%20zoe"

argus_base_url = "http://www.lacentrale.fr/cote-auto-renault-zoe-"
argus_end_url = "+charge+rapide-"

versions = ["intens", "life", "zen"]

regions_list = ["ile_de_france",  "provence_alpes_cote_d_azur", "aquitaine"]

base_result = requests.get(base_url)
base_soup = BeautifulSoup(base_result.text, "html.parser")

fields = ["region", "version", "year", "km", "price", "city", "phone", "seller", "argus", "comp"]
all_results = pd.DataFrame(columns=fields)

def get_argus_cote(listversion):
    results = {}
    for version in listversion:
        url = argus_base_url + version + argus_end_url
        argus_request = requests.get(url)
        argus_soup = BeautifulSoup(argus_request.text, "html.parser")
        temp_price = argus_soup.find_all("strong", class_="f24")[0].text
        argus_price = re.sub("[^0-9]", "", temp_price)
        results[version] = argus_price
    return results


def get_infos_for_region(region):
    results = pd.DataFrame(columns=fields)
    page = 1
    line = 0
    while True:
        url = base_url + region + page_url + str(page)+ search_url
        page_request = requests.get(url)
        page_soup = BeautifulSoup(page_request.text, "html.parser")
        car_list = page_soup.find_all("a", class_="list_item")
        name_list = page_soup.find_all("h2", class_="item_title")
        if len(car_list) == 0:
            break
        for j in range(len(car_list)):
            current_type = re_type.findall(name_list[j].text)
            if len(current_type) != 0:
                results.set_value(line, "version", current_type[0].lower())

            current_seller =  json.loads(car_list[j]["data-info"])["ad_offres"]
            results.set_value(line, "seller", current_seller)

            car_url = "https:" + car_list[j]["href"]
            car_request = requests.get(car_url)
            car_soup = BeautifulSoup(car_request.text, "html.parser")
            current_price = car_soup.find_all("h2", class_="item_price")[0]["content"]
            results.set_value(line, "price", float(current_price))

            current_city = re_city.findall(
                        car_soup.find_all("span", class_="value")[1].text)
            if len(current_city) != 0:
                results.set_value(line, "city", current_city[0])

            current_year = re_year.findall(
                        car_soup.find_all("span", class_="value")[4].text)
            if len(current_year) != 0:
                results.set_value(line, "year", int(current_year[0]))

            current_km = re_km.findall(
                        car_soup.find_all("span", class_="value")[5].text)
            if len(current_km) != 0:
                results.set_value(line, "km", float(current_km[0]))

            current_desc = car_soup.find_all("p", itemprop="description")[0].text
            current_phone = re_phone.findall(current_desc)
            if len(current_phone) > 0:
                results.set_value(line, "phone", current_phone[0])
            else:
                results.set_value(line, "phone", "")

            current_argus = 0.0
            try:
                if current_year[0] == "2016":
                    argus_url = argus_base_url + current_type[0].lower() + argus_end_url + "2015.html"
                else:
                    argus_url= argus_base_url + current_type[0].lower() + argus_end_url + current_year[0] + ".html"
                argus_req = requests.get(argus_url)
                argus_soup = BeautifulSoup(argus_req.text, "html.parser")
                temp_price = argus_soup.find_all("strong", class_="f24")[0].text
                temp_price1 = argus_soup.find_all("strong", class_="mL15")[1].text
                argus_price = re.sub("[^0-9]", "", temp_price)
                new_price = re.sub("[^0-9]", "", temp_price1)
                current_argus = float(argus_price)
                if current_year[0] == "2016":
                    current_argus = (float(argus_price) + float(new_price)) / 2.0
                    results.set_value(line, "argus", current_argus)
                else:
                    results.set_value(line, "argus", current_argus)
            except:
                print("error in url")

            if float(current_price) > float(current_argus) + 1000:
                results.set_value(line, "comp", "expensive")
            else:
                if float(current_price) < float(current_argus) - 1000:
                    results.set_value(line, "comp", "cheap")
                else:
                    results.set_value(line, "comp", "fair")
            line += 1
        page += 1
        results["region"] = region
    return results


def get_info_for_all_regions(listregion):
    results = pd.DataFrame(columns=fields)
    for region in listregion:
        frames = [results, get_infos_for_region(region)]
        results = pd.concat(frames, ignore_index=True)
    return results


zoe_results = get_info_for_all_regions(regions_list)


