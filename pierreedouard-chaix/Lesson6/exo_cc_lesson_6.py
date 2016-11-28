# -*- coding: utf-8 -*-

import requests
import bs4
import os
import pandas as pd
import json
import numpy as np
from unidecode import unidecode
import re
import pdb
import time
import matplotlib.pyplot as plt

aliments = pd.read_csv('aliments.csv', delimiter='\t')
aliments = aliments.set_index([range(0, len(aliments))])

# Réduire les packaging aux occurrences les plus fréquentes
frequent_packaging = aliments["packaging"].value_counts() > 20
packaging_to_keep = frequent_packaging[frequent_packaging].index
aliments_with_frequent_packaging = aliments[aliments["packaging"].isin(packaging_to_keep)]

def contientMateriau(materiau):
	aliments_materiaupasnan = aliments.dropna(subset = ["packaging"])
	aliments_avec_materiau = aliments_materiaupasnan[aliments_materiaupasnan["packaging"].str.lower().str.contains(str.lower(materiau))]
	return aliments_avec_materiau.groupby("countries_fr")[["countries_fr"]].count()

# Version alternative utilisant une expression régulière, pour les ingrédients
def contientIngredients(ingredients):
	regex = ""
	for ingredient in ingredients:
		regex = regex + ingredient + "|"
	regex_f = "("+ regex[:-1] + ")"
	ingredient_lines = np.invert(pd.isnull(aliments["ingredients_text"].str.lower().str.extract(regex_f, expand = True)))[0]
	aliments_avec_ingredient = aliments[ingredient_lines]
	return aliments_avec_ingredient.replace(np.nan, "--Aucun pays de consommation identifié--").groupby("countries_fr")[["countries_fr"]].count()