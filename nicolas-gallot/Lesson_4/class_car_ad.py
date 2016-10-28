from bs4 import BeautifulSoup
import requests
import re

DEFAULT_VALUE = "#NA"

class CarAd:


    url = DEFAULT_VALUE
    year = DEFAULT_VALUE
    add_type = DEFAULT_VALUE
    model = DEFAULT_VALUE # Intense/Life/Zen
    owner_phone = DEFAULT_VALUE
    price = DEFAULT_VALUE
    data_block = DEFAULT_VALUE
    description_block = DEFAULT_VALUE
    kilometrage = DEFAULT_VALUE

    def __init__(self, add_attributes, txt_price):

        data_info = add_attributes['data-info']

        self.url = "http://{0}".format(add_attributes['href'][2:])
        self.add_type = self.get_add_type(data_info)
        self.model = self.get_model_from_title(add_attributes['title'])
        self.get_extra_info_block()
        self.owner_phone = DEFAULT_VALUE
        self.price = self.get_price_from_price_block(txt_price)

        # Extra info
        self.kilometrage = self.get_kilometrage()
        self.owner_phone = self.get_owner_phone()
        self.year = self.get_year()

    def get_model_from_title(self, title):
        pattern_title = "intens|life|zen"
        rgx_title = re.compile(pattern_title, re.IGNORECASE)
        extracts_title = rgx_title.findall(title)
        res = "NA"
        if len(extracts_title)>0:
            res = extracts_title[0].lower()
        return res

    def get_add_type(self, data_info):
        pattern = "{0}ad_offres{0} : {0}pro{0}|{0}ad_offres{0} : {0}part{0}".format('"')
        rgx = re.compile(pattern, re.IGNORECASE)
        res = rgx.findall(data_info)
        if len(res) > 0:
            pattern = "part|pro"
            rgx = re.compile(pattern, re.IGNORECASE)
            mtc = rgx.findall(res[0])
            return mtc[0]
        else:
            return DEFAULT_VALUE

    def get_price_from_price_block(self, price_block):
        pattern = "[0-9]"
        rgx = re.compile(pattern, re.IGNORECASE)
        return int("".join(rgx.findall(price_block)))

    def get_extra_info_block(self):
        bs_res = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.data_block = bs_res.find_all('span', {'class' : 'property'})
        self.description_block = bs_res.find_all('p', {'class' : 'value', 'itemprop' : 'description'})

    def find_info_in_block(self, info_type):
        for d in self.data_block:
            if d.text.lower() == info_type.lower():
                return d.parent.contents[3].text

    def get_kilometrage(self):
        info = self.find_info_in_block("Kilométrage")
        pattern = "[0-9]"
        rgx = re.compile(pattern)
        return int("".join(rgx.findall(info)))

    def get_year(self):
        info = self.find_info_in_block("Année-modèle")
        pattern = "[0-9]{4}"
        rgx = re.compile(pattern)
        return "".join(rgx.findall(info))

    def get_owner_phone(self):
        desc = self.description_block[0].text
        pattern = "\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}"
        rgx = re.compile(pattern)
        res = rgx.findall(desc)
        if len(res) > 0:
            return res[0]
        else:
            return DEFAULT_VALUE

    def to_df(self):
        return [self.model, self.year, self.kilometrage, self.add_type, self.owner_phone
                , self.price]

    def __str__(self):
        return "Add Type : {0}. Model : {1}. Year : {2}. Km : {3}. Price : {4}. Owner's phone : {5}. Url : {6}" \
            .format(self.add_type, self.model, self.year, self.kilometrage, self.price, self.owner_phone, self.url)
