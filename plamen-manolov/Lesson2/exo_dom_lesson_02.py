import requests
from bs4 import BeautifulSoup



# def extractIntFromDOM(soup, classname):
#   res_str = soup.find(class_=classname).text.replace(u'\xa0','').replace('vues','')
#   res = int(res_str)
#   return res

# def extractLikeDislikeFromDOM(soup, classname, position):
#   res_str = soup.find_all(class_=classname)[position].find(class_="yt-uix-button-content").text.replace(u'\xa0','')
#   res = int(res_str)
#   return res

# def computeIndicatorForPage(url):
#   result = requests.get(url)
#   soup = BeautifulSoup(result.text, 'html.parser')
#   number_of_views = extractIntFromDOM(soup,'watch-view-count')
#   number_of_likes = extractLikeDislikeFromDOM(soup,'like-button-renderer-like-button', 0)
#   number_of_dislikes = extractLikeDislikeFromDOM(soup,'like-button-renderer-dislike-button',1)
#   indicator = 1000.* (number_of_likes - number_of_dislikes ) / number_of_views

#   title = soup.title.text
#   print '====='
#   print title
#   print "Likes", number_of_likes
#   print "Dislikes", number_of_dislikes
#   print "VIews", number_of_views
#   print "Popularity", indicator
#   print '====='
#   metrics = {}
#   metrics['number_of_views'] = number_of_views
#   metrics['number_of_likes'] = number_of_likes
#   metrics['number_of_dislikes'] = number_of_dislikes
#   metrics['indicator'] = indicator
#   return  metrics


#computeIndicatorForPage('https://www.youtube.com/watch?v=wfN4PVaOU5Q')


def getAllMetricsForTown(commune,dpt,annee):
 
  #for page in range(1, MAX_PAGE + 1):
  #resutTown = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' + commune + '&dep=' + dpt + '&type=BPS&param=5&exercice=' + annee )
  #lesParams = {'ICOM':commune,'DEP':dpt,'EXERCICE':annee}

  #http://alize2.finances.gouv.fr/communes/eneuro/tableau.php?icom=118&dep=014&type=BPS&param=0&comm=0&exercice=2014
  #lesParams={'ICOM':'101','DEP':'075','TYPE':'BPS','PARAM':'5','comm':'0','EXERCICE':'2009'}
  lesParams = {'icom': commune, 'dep': dpt, 'type': 'BPS', 'param': '0','dep': '', 'reg': '', 'nomdep': '', 'moysst': '', 'exercice': '', 'param': '', 'type': '', 'siren': '', 'comm': '0', 'exercice': annee}
  #print (lesParams)
  #resutTown = requests.put('http://alize2.finances.gouv.fr/communes/eneuro/tableau.php' , params = lesParams)

  print(r.url)




  #print ( 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' + commune + '&dep=' + dpt + '&type=BPS&param=5&exercice=' + annee )
  soup_town = BeautifulSoup(resutTown.text, 'html.parser')
  print (soup_town)
  soup = BeautifulSoup(result.text, 'html.parser')  
  res_str= soup.findAll('td', {"class": "libellepetit"})
  #res_str = soup.find_all(class_='libellepetit')[position].find(class_="yt-uix-button-content").text.replace(u'\xa0','')
  for i in (2,4,5,6):
    leResut[i] = int(res_str[i])
  print leResut  
  

for annee in (range (2009,2017)):
  getAllMetricsForTown('056','075',annee)


#metrics_rihanna = getAllMetricsForTown('Paris')
#metrics_beyonce = getAllMetricsForArtist('beyonce')
