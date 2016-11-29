import requests
from bs4 import BeautifulSoup


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

    for year in range(2010, 2016):
        soup = BeautifulSoup(requests.post(path + str(year)).text, 'html.parser')
        if year not in dataSetCitiesAccount:
            dataSetCitiesAccount[year] = classifyFigures(soup, classmontant, listChamps, lastColumn)

        #print(dataSetCitiesAccount)
    return dataSetCitiesAccount




data_return = {}
data_return = getFiguresByYear()
for el in data_return.keys():
    for sub_el in data_return.get(el):
        for fin_el in data_return[el].get(sub_el):
            print(str(el) + ' : ' +str(sub_el) + ' : ' + str(fin_el) + ' : ' + str(data_return[el].get(sub_el).get(fin_el)))

