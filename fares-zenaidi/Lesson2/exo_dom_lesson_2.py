import requests
from bs4 import BeautifulSoup


def extractIntFromDOM(soup, classname):
  res_str = soup.find(class_=classname).text.replace(u'\xa0','').replace('vues','')
  res = int(res_str)
  return res


def extractLikeDislikeFromDOM(soup, classname, position):
  res_str = soup.find_all(class_=classname)[position].find(class_="yt-uix-button-content").text.replace(u'\xa0','')
  res = int(res_str)
  return res


def computeIndicatorForPage(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  number_of_views = extractIntFromDOM(soup,'watch-view-count')
  number_of_likes = extractLikeDislikeFromDOM(soup,'like-button-renderer-like-button', 0)
  number_of_dislikes = extractLikeDislikeFromDOM(soup,'like-button-renderer-dislike-button',1)
  indicator = 1000.* (number_of_likes - number_of_dislikes ) / number_of_views

  title = soup.title.text
  print('=====')
  print(title)
  print("Likes", number_of_likes)
  print("Dislikes", number_of_dislikes)
  print("VIews", number_of_views)
  print("Popularity", indicator)
  print('=====')
  metrics = {}
  metrics['number_of_views'] = number_of_views
  metrics['number_of_likes'] = number_of_likes
  metrics['number_of_dislikes'] = number_of_dislikes
  metrics['indicator'] = indicator
  return  metrics


#computeIndicatorForPage('https://www.youtube.com/watch?v=wfN4PVaOU5Q')


def getAllMetricsForArtist(artist):
  all_metrics = []
  MAX_PAGE = 1
  for page in range(1, MAX_PAGE + 1):
    all_videos_artist = requests.get('https://www.youtube.com/results?search_query=' + artist + '&page=' + str(page))
    soup_artist = BeautifulSoup(all_videos_artist.text, 'html.parser')
    list_video_artist = map(lambda x: x['href'] , soup_artist.find_all(class_="yt-uix-tile-link"))
    for link in list_video_artist:
      if 'watch' in link:
        metrics = computeIndicatorForPage('https://www.youtube.com' + link )
        all_metrics.append(metrics)
  return all_metrics

metrics_rihanna = getAllMetricsForArtist('rihanna')
metrics_beyonce = getAllMetricsForArtist('beyonce')