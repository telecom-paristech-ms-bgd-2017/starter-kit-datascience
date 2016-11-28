from bs4 import BeautifulSoup
import requests


artiste ="Eminem"
page=3
url ="https://www.youtube.com/results?search_query="+artiste+"&page="+str(page)
result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')
List_str_nbr_vues = soup.findAll(class_='yt-lockup-meta-info')
#print (List_str_nbr_vues)
for resultat in List_str_nbr_vues:
    str_nbr_vues = resultat.findAll('li')
    if len(str_nbr_vues) == 2:
        print(str_nbr_vues[1].text.replace(u'\xa0','').replace('vues',''))



#res_str = soup.find_all(class_="watch-view-count")[1].find(class_="yt-uix-button-content")
#[position]


#print(res_str)