# -*- coding: utf8 -*-
import pandas as pd
aliments = pd.read_csv("aliments.csv", sep="\t", error_bad_lines = )


#=======================================================
# IMPORTANT à reviser !!!!!

# df[''].isin()

# pour lecture 
# error_bad_lines 

# df.melt

#=======================================================

#aliments = pd.read_csv("/Users/papa/MS/kitBGD/starter-kit-datascience/Lessons-Exercices/Lesson4/aliments.csv", sep="\t")


#aliments = pd.read_csv('aliments.csv', delimiter='\t')
#aliments = aliments.set_index('product_name')
#aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True)
#aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True).to_csv('traces.csv')

#aliments_with_traces = aliments.dropna(subset=['traces'])

#traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])
#traces = set.union(*traces_iter)

#dummies = DataFrame(np.zeros((len(aliments_with_traces), len(traces))), columns=traces)

#for i, tr in enumerate(aliments_with_traces.traces):
#     dummies.ix[i, tr.split(',')] = 1

#dummies_nutrition = pd.get_dummies(aliments.dropna(subset=['nutrition_grade_fr'])['nutrition_grade_fr'])
