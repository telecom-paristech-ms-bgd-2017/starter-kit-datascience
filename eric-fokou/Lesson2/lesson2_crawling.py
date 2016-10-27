import requests
import pandas as pd
from bs4 import BeautifulSoup

MAX_PAGE = 2


def extractIntFromDOM(soup, classname):
    res_str = soup.find(class_=classname).text.replace(
        u'\xa0', '').replace('vues', '')
    res = int(res_str)
    return res


def extractLikeDislikeFromDOM(soup, classname, position):
    # print len(soup.find_all(class_=classname))
    res_str = soup.find_all(class_=classname)[position].find(
        class_="yt-uix-button-content").text.replace(u'\xa0', '')
    res = int(res_str)
    return res


def computeIndicatorForPage(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    number_of_views = extractIntFromDOM(soup, 'watch-view-count')
    number_of_likes = extractLikeDislikeFromDOM(
        soup, 'like-button-renderer-like-button', 0)
    number_of_dislikes = extractLikeDislikeFromDOM(
        soup, 'like-button-renderer-dislike-button', 1)
    indicator = 1000. * \
        (number_of_likes - number_of_dislikes) / number_of_views

    title = soup.title.text
    print '====='
    print title
    print "Likes", number_of_likes
    print "Dislikes", number_of_dislikes
    print "VIews", number_of_views
    print "Popularity", indicator
    print '====='
    metrics = {}
    metrics['song'] = title
    metrics['number_of_views'] = number_of_views
    metrics['number_of_likes'] = number_of_likes
    metrics['number_of_dislikes'] = number_of_dislikes
    metrics['indicator'] = indicator
    return metrics


# computeIndicatorForPage('https://www.youtube.com/watch?v=wfN4PVaOU5Q')


def getAllMetricsForArtist(artist):
    all_metrics = []
    for page in range(1, MAX_PAGE + 1):
        all_videos_artist = requests.get(
            'https://www.youtube.com/results?search_query=' + artist + '&page=' + str(page))
        soup_artist = BeautifulSoup(all_videos_artist.text, 'html.parser')
        # print(soup_artist.prettify())

        list_video_artist = map(
            # lambda x: x['href'],
            # soup_artist.find_all(class_="yt-uix-tile-link"))
            lambda x: x['href'], soup_artist.find_all(attrs={"class": "yt-uix-sessionlink spf-link ", "dir": "ltr"}))
        for link in list_video_artist:
            metrics = computeIndicatorForPage('https://www.youtube.com' + link)
            all_metrics.append(metrics)
    return all_metrics

metrics_rihanna = getAllMetricsForArtist('rihanna')
df_rihanna = pd.DataFrame(metrics_rihanna, columns=[
                          'song', 'number_of_views', 'number_of_likes', 'number_of_dislikes', 'indicator'])
df_rihanna.to_csv('Rihanna.csv', index=False, encoding='utf-8')
avg_rihanna_indicator = 0
for song in metrics_rihanna:
    avg_rihanna_indicator += song['indicator']

metrics_beyonce = getAllMetricsForArtist('beyonce')
df_beyonce = pd.DataFrame(metrics_beyonce, columns=[
                          'song', 'number_of_views', 'number_of_likes', 'number_of_dislikes', 'indicator'])
df_beyonce.to_csv('Beyonce.csv', index=False, encoding='utf-8')
avg_beyonce_indicator = 0
for song in metrics_beyonce:
    avg_beyonce_indicator += song['indicator']
print(
    "=================================================================================")

print("Rihanna AVG indicator = " +
      str(float(avg_rihanna_indicator) / len(metrics_rihanna)))
print("Beyonce AVG indicator = " +
      str(float(avg_beyonce_indicator) / len(metrics_beyonce)))
