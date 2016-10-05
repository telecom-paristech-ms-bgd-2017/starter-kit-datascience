import urllib2
from bs4 import BeautifulSoup

#exo_dom_lesson_02.py

#Crawling Ville de Paris


#from bs4 import BeautifulSoup
#soup = BeautifulSoup(html_doc, 'html.parser')

#print(soup.prettify())

# use the line below to down load a webpage





def ABCD_commune(annee):

    web_address='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+annee.__str__()
    html = urllib2.urlopen(web_address).read()

    soup = BeautifulSoup(html)

    """print soup.prettify()[0:200] #=> read html --------------> best option
    print '/n ------------ /n'
    print soup.get_text()[0:200] #=> all text
    print '/n ------------ /n'
    print soup.get_text('|', strip=True)[0:200]
    """

    """print soup.prettify() #=> read html --------------> best option
    print '/n ------------ /n'
    print soup.title

    #print soup.find_all('montantpetit')
    #print soup.td['montantpetit G']
    print soup.find_all('td')
    print '\n'
    print '*-------------------*'
    print '*-------------------*'
    print type(soup.find_all('td'))
    """
    td_all=soup.find_all('td')
    """result = []

    for td in td_all:
        #    result.extend(td.find_all(text='montantpetit G'))
        #result.extend(td.find_all(class='montantpetit G'))

        #    mydivs = soup.findAll("div", { "class" : "montantpetit G" })
        #mydivs = soup.findAll({ "class" : "montantpetit G" })
        try:
            print td['class']
            print 'td["class"]'
        except KeyError:
            try:
                print td['montantpetit']
                print 'td["montantpetit"]'
            except KeyError:
                print td
                print 'td'

        #print mydivs
        #    result.extend(mydivs)
        raw_input()
    """
    """print soup.find_all(class_='montantpetit G')


    print len(soup.find_all(class_='montantpetit G'))
    """
    result_list=[]

    for a in range(len(soup.find_all(class_='montantpetit G'))):
        el=soup.find_all(class_='montantpetit G')[a]
    #    print el.text
        #print a
        new_string=el.text.replace(' ', '')
        result_list.append(    int(new_string))
    #    print result_list
    #    raw_input()

    en_milliers_deuros=[result_list[r] for r in range(len(result_list)) if r%3==0]
    euros_par_habitant=[result_list[r] for r in range(len(result_list)) if r%3==1]
    moyenne_de_la_strate=[result_list[r] for r in range(len(result_list)) if r%3==2]
    """print moyenne_de_la_strate #=[result_list[r] for r in range(len(result_list)) if r%3==2]
    print euros_par_habitant
    print en_milliers_deuros
    """
    ABCD_moyenne_de_la_strate=[moyenne_de_la_strate[a] for a in range(len(moyenne_de_la_strate)) if a<5 and a!=2]
    """print ABCD_moyenne_de_la_strate
    """

    ABCD_euros_par_habitant=[euros_par_habitant[a] for a in range(len(euros_par_habitant)) if a<5 and a!=2]
    ABCD_en_milliers_deuros=[en_milliers_deuros[a] for a in range(len(en_milliers_deuros)) if a<5 and a!=2]

    #print ABCD_en_milliers_deuros

    
    print ABCD_moyenne_de_la_strate
    print ABCD_euros_par_habitant
    raw_input()
    return ABCD_euros_par_habitant,ABCD_moyenne_de_la_strate





#main

for annee in range(2009,2017,1):
    print 'annee'
    print annee
    [ABCD_euros_par_habitant,ABCD_moyenne_de_la_strate]=ABCD_commune(annee)

#[el.find(class_="montantpetit G") for el in soup.find_all(class_='montantpetit G')]
#print result

#<td class="libellepetit G">TOTAL DES PRODUITS DE FONCTIONNEMENT = A</td>

"""
th_all = soup.find_all('th')
result = []
for th in th_all:
    result.extend(th.find_all(text='A'))
"""



#print soup.td['class']

#print soup.find(id="link3")
#print soup.find(class="montantptit G")
#print soup.select("#names + p + p")
#print soup['montantpetit G']
#print number_of_views = extractIntFromDOM(soup,'montantpetit G')



#=> all text as unicode, separate tags with |, remove line breaks
