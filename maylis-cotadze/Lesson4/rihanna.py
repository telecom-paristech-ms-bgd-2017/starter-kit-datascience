import requests
from bs4 import BeautifulSoup
import pandas as pd

def extractIntFromDom(soup, classname):
    res_str = soup.find(class_=classname).text.replace(u'\xa0','').replace('vues','')
    res = int(res_str)
    return res

def extractLikeDislikeFromDom(soup, classname, position):
    res_str = soup.find_all(class_=classname)[position].find(class_='yt-uix-button-content').text.replace(u'\xa0','')
    res = int(res_str)
    return res

def computeIndicatorForPage(url):
    result = request.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    number_of_views = extractIntFromDom(soup,'watch-view-button',0)
    number_of_likes = extractLikeDislikeFromDom(soup, 'like-button-rendered-like-button',0)
    number_of_dislikes = extractLikeDislikeFromDom(soup, 'like-button-rendered-dislike-button',1)

title = soup.title.text

def getAllMetricsForArtist(artist):
    all_metrics = []
    MAX_PAGE = 1
    for page in range(1,MAX_PAGE+1):
        all_videos_artist = requests.get('https:://www.youtube.com/results?search_query='+ artist + '&page' + str(page))
        soup_artist = BeautifulSoup(all_videos_artist.text, 'html.parser')
        list_video_artist = map(lambda x: x['href'], soup_artist.find_all(class_="yt-uix-tile-link"))
        for link in list_video_artist:
            if 'watch' in link:
                metrics = computeIndicatorForPage('https://www.youtube.com'+link)
                all_metrics.append(metrics)
        return all_metrics
        
