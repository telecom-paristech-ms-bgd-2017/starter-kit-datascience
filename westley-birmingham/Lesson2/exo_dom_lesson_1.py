import requests
from bs4 import BeautifulSoup

year = 2013

result = requests.post('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year)).text
soup = BeautifulSoup(result, 'html.parser')
print(soup.find_all(class_='libellepetit G')[1].parent.find_all(class_='montantpetit G')[2].text)
souptest = soup.find_all(class_='libellepetit G')[1]

def extractColumnsFromDOM(soup1, classname):
    listColumns = soup1.find_all(class_=classname)
    #print(listColumns)
    return listColumns

def extractFiguresFromDOM(soup2, classname, figureColumn):
    figure = soup2.parent.find_all(class_=classname)[figureColumn]
    print(figure.text)
    return int(figure.text.replace(u'\xa0', '').replace(' ', ''))

def convertFiguresColumns(val):
        dicoFigures = {1: 'Euros par habitant', 2: 'Moyenne de la strate'}
        if val in range(1, 3):
            return dicoFigures[val]

def test():
    ColumnsDictionary = {}
    listSelected = {'= A', '= B', '= C', '= D'}
    classname = 'montantpetit G'
    #figuresColumn = 1
    #endOfColumn = 3

    for el in extractColumnsFromDOM(soup, 'libellepetit G'):
        if el.text[-3:] in listSelected:
            for figuresColumn in range(1,3):
                if el.text not in ColumnsDictionary:
                    figuresDictionary = {}
                    figuresDictionary[convertFiguresColumns(figuresColumn)] = extractFiguresFromDOM(el, classname, figuresColumn)
                    ColumnsDictionary[el.text] = figuresDictionary
                else:
                    if convertFiguresColumns(figuresColumn) not in ColumnsDictionary[el.text]:
                        ColumnsDictionary[el.text][convertFiguresColumns(figuresColumn)] = extractFiguresFromDOM(el, classname, figuresColumn)
                    #else:
                     #   ColumnsDictionary[el.text][convertFiguresColumns(figuresColumn)] = extractFiguresFromDOM(el, classname, figuresColumn)
            #figuresColumn += 1
    print(ColumnsDictionary)
    return








#===========================================================================
#row = 5
#while true
#    element = soup.select('tr:nth-of-type('+ row +')')
#    if len(element) > 0:
#        # element is your desired row element, do what you want with it
#        row += 5
#    else:
#        break

