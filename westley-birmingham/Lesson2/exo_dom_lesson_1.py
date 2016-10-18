import requests
from bs4 import BeautifulSoup

#Python crawler ebook

def extractColumnsFromDOM(soup1, classname):
    listColumns = soup1.find_all(class_=classname)
    #print(listColumns)
    return listColumns


def extractFiguresFromDOM(soup2, classname, figureColumn):
    figure = soup2.parent.find_all(class_=classname)[figureColumn]
    # print(figure.text)
    return int(figure.text.replace(u'\xa0', '').replace(' ', ''))


def convertFiguresColumns(val):
        dicoFigures = {1: 'Euros par habitant', 2: 'Moyenne de la strate'}
        if val in range(1, 3):
            return dicoFigures[val]


def classifyFigures(soup, classname, listSelected, endOfColumn):
    ColumnsDictionary = {}

    for el in extractColumnsFromDOM(soup, 'libellepetit G'):
        if el.text[-3:] in listSelected:
            for figuresColumn in range(1,endOfColumn+1):
                if el.text not in ColumnsDictionary:
                    figuresDictionary = {}
                    figuresDictionary[convertFiguresColumns(figuresColumn)] = extractFiguresFromDOM(el, classname, figuresColumn)
                    ColumnsDictionary[el.text] = figuresDictionary
                else:
                    if convertFiguresColumns(figuresColumn) not in ColumnsDictionary[el.text]:
                        ColumnsDictionary[el.text][convertFiguresColumns(figuresColumn)] = extractFiguresFromDOM(el, classname, figuresColumn)
                    #else:
                     #   ColumnsDictionary[el.text][convertFiguresColumns(figuresColumn)] = extractFiguresFromDOM(el, classname, figuresColumn)
    return ColumnsDictionary



def getFiguresByYear():
    listChamps = {'= A', '= B', '= C', '= D'}
    classmontant = 'montantpetit G'
    lastColumn = 2

    path = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
    dataSetCitiesAccount = {}

    for year in range(2010, 2014):
        soup = BeautifulSoup(requests.post(path + str(year)).text, 'html.parser')
        if year not in dataSetCitiesAccount:
            dataSetCitiesAccount[year] = classifyFigures(soup, classmontant, listChamps, lastColumn)

        #print(dataSetCitiesAccount)
    return dataSetCitiesAccount



# print(soup.find_all(class_='libellepetit G')[1].parent.find_all(class_='montantpetit G')[2].text)
# souptest = soup.find_all(class_='libellepetit G')[1]


#===========================================================================
#row = 5
#while true
#    element = soup.select('tr:nth-of-type('+ row +')')
#    if len(element) > 0:
#        # element is your desired row element, do what you want with it
#        row += 5
#    else:
#        break

