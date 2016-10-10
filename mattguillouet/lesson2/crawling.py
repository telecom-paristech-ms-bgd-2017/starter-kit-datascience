import requests
from bs4 import BeautifulSoup
import sys

def computeIndicatorFromPage(url):
	
	result = requests.get(url)

	soup = BeautifulSoup(result.content, 'html.parser')

	nb_views = int(soup.find(class_="watch-view-count").text.replace('\xa0','').replace('vues',''))

	nb_likes = int(soup.find_all(class_="like-button-renderer-like-button")[0].find(class_="yt-uix-button-content").text.replace('\xa0',''))
	nb_dislikes = int(soup.find_all(class_="like-button-renderer-dislike-button")[0].find(class_="yt-uix-button-content").text.replace('\xa0',''))

	indicator = (nb_likes - nb_dislikes) / nb_views
	print('Title : {0}'.format(soup.title.text))
	print('Likes : {0}, Dislikes : {1}, Views : {2}'.format(nb_likes,nb_dislikes,nb_views))
	print('Indicator : {0}'.format(indicator))
	
	metric = {}
	metric['likes'] = nb_likes
	metric['dislikes'] = nb_dislikes
	metric['views'] = nb_views
	metric['indicator'] = indicator
	return metric


def getIndicatorsByArtist(artist):
	
	all_metrics = []
	maxPages = 1
	for page in range(1,maxPages+1):
		url = 'https://www.youtube.com/results?search_query=' + artist + '+page=' + str(page)
		
		result = requests.get(url)
		soup = BeautifulSoup(result.content, 'html.parser')

		urls = list(map(lambda x: x['href'], soup.find_all(class_='yt-uix-tile-link')))

		for u in  urls:
			if 'watch' in u:
				metric = computeIndicatorFromPage('https://www.youtube.com' + u)
				all_metrics.append(metric) 

	return all_metrics

def getMeanIndicators(metrics):

	sum_ = 0
	for m in metrics:
		sum_ += m['indicator']

	return float(sum_)/float(len(metrics))

if __name__ == '__main__':
	artist1 = sys.argv[1]
	artist2 = sys.argv[2]
	metrics_artist1 = getIndicatorsByArtist(artist1)
	metrics_artist2 = getIndicatorsByArtist(artist2)

	print('Mean indicator for {0} : {1}'.format(artist1,getMeanIndicators(metrics_artist1)))
	print('Mean indicator for {0} : {1}'.format(artist2,getMeanIndicators(metrics_artist2)))