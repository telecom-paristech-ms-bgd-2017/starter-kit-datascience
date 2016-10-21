# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re


csv = ' John,     47 rue Barrault, 36 ans  '
credits_cards = ' Thanks for paying with 1098-1203-1233-2354        '
cred = re.compile(r'\d{4}-\d{4}')


email = '''
Voici le fichier complété et le calendrier et la liste des adresses des élèves (elles ne seront opérationnelles que la semaine prochaine).








 pierre.arbelet@telECOM-Paristech.fr francois.bLAS@TElecom-parisTECH.fr geoffray.bories@telecom-paristech.fr claire.chazelas@TELECOM-PAristech.fr dutertre@telecom-paristech.fr nde.fOKOU@telecom-paristech.fr wei.he@telecom-paristech.fr anthony.hayot@telecom-paristech.fr frederic.hohner@telecom-paristech.fr yoann.janvier@telecom-paristech.fr mimoune.louarradi@telecom-paristech.fr david.luz@telecom-paristech.fr nicolas.marsallon@telecom-paristech.fr paul.mochkovitch@telecom-paristech.fr martin.prillard@telecom-paristech.fr christian.penon@telecom-paristech.fr gperrin@telecom-paristech.fr anthony.reinette@telecom-paristech.fr florian.riche@telecom-paristech.fr romain.savidan@telecom-paristech.fr yse.wanono@telecom-paristech.fr ismail.arkhouch@telecom-paristech.fr philippe.cayeux@telecom-paristech.fr hicham.hallak@telecom-paristech.fr arthur.dupont@telecom-paristech.fr dabale.kassim@telecom-paristech.fr xavier.lioneton@telecom-paristech.fr sarra.mouas@telecom-paristech.fr jonathan.ohayon@telecom-paristech.fr alix.saas-monier@telecom-paristech.fr thabet.chelligue@telecom-paristech.fr amoussou@telecom-paristech.fr pierre.arbelet@telecom-paristech.fr
'''

pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex_email = re.compile(pattern, flags=re.IGNORECASE)
extracts = regex_email.findall(email)

df = Series(extracts).str.upper().str.extract('([A-Z0-9_%+-]+)\.?([A-Z0-9_%+-]*)@([A-Z0-9.-]+)\.([A-Z]{2,4})')

df = df.rename(columns = {0:'firstname', 1:'lastname', 2:'ecole',3:'domain'} )

df.index = df.index.map(lambda x: 'Eleve ' +str(x))


def strip_corse(val):
    if type(val) == int:
        return val
    if val == 'nan':
        return -1
    return int(re.sub('(A|B)', '0',val))

aliments = pd.read_csv('aliments.csv', delimiter='\t')
aliments = aliments.set_index('product_name')
aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True)
aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True).to_csv('traces.csv')

aliments_with_traces = aliments.dropna(subset=['traces'])

traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])
traces = set.union(*traces_iter)

dummies = DataFrame(np.zeros((len(aliments_with_traces), len(traces))), columns=traces)

for i, tr in enumerate(aliments_with_traces.traces):
     dummies.ix[i, tr.split(',')] = 1

dummies_nutrition = pd.get_dummies(aliments.dropna(subset=['nutrition_grade_fr'])['nutrition_grade_fr'])
