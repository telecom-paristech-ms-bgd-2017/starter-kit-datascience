import requests
from bs4 import BeautifulSoup


def extractSource(soup, line):
    tables = soup.body.findAll('table')
    if len(tables) >= 3:
        lineA = tables[2].findAll('tr')[line]
        epH = int(lineA.findAll('td')[1].text.replace("\xa0", "")
                     .replace(" ", ""))
        moStrate = int(lineA.findAll('td')[2].text.replace("\xa0", "")
                    .replace(" ", ""))
        return (str(epH)+"                          "+str(moStrate))

def getAllMetrics():
     lines = [7,11,19,14]
     alpha = ["A","B","C","D"]
     for year in range(2009, 2014):
         resultats = requests.get("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+str(year))
         soup_paris = BeautifulSoup(resultats.text, 'html.parser')
         print ("-------")
         print (year)
         print ("--")
         print ("Euros par habitant	"+" Moyenne de la strate	")
         for line, a in zip(lines, alpha):
             print (a)
             print (extractSource(soup_paris, line))
         print ("-------")

getAllMetrics()
