import urllib.request
from bs4 import BeautifulSoup

#print les donnees mais non sauvegardées

def get_stat(min, max):
#pour A/0 B/1 C/3 D/4
  for year in range(min,max):
    
    all_year = urllib.request.urlopen("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(year)).read()
    #the soup contains all the HTML of the original document

    soup=BeautifulSoup(all_year,"html.parser")
    #extract section
    res=soup.find_all("td",class_="libellepetit G")
    print ("*********Année: " + str(year)+"************")

    for i in [0,1,3,4]:
      section_a=res[i].parent.text
      max=section_a.rindex('\xa0')
      section_a=section_a[:max].replace(" ","")+section_a[max:]
      section_a=section_a[1:-1].replace('\xa0\n',';').replace('\n',';')
      section_a=section_a.split(';')

      # euro par hab
      eur_hab=int(section_a[1])

      #moyenne strat
      moy=int(section_a[2])

      titre=section_a[3]
      print (titre) 
      print("euros par habitant: ", eur_hab)
      print ("moyenne par strate: ", moy)
      print ('=====') 

'''  metrics = {}
     metrics['eur_par_hab'] = eur_hab
     metrics['moy_par_strate'] = moy
     return  metrics
'''   
get_stat(2010,2013)

