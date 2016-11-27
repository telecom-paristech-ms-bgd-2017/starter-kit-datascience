import pandas as pd


aliments = pd.read_csv("/Users/khouiyadam/Documents/charles/aliment.csv",encoding = "utf-8" ,delimiter ="\t" , error_bad_lines =False ,warn_bad_lines =False)



#elimination des colonnes que j 'ai jugé non nécessaire

aliments_cleaned = aliments.ix[:,8:40]

#elimination des NAN   sur la colonne générique

aliments_cleaned.dropna(subset = ['generic_name'],inplace = True)
aliments_cleaned.drop(['countries_tags','countries_fr','packaging_tags','brands_tags','categories_tags','labels_tags'],inplace=True,axis=1)


grouped_aliment = aliments.groupby(["brands"])["sugars_100g"].mean()


print (grouped_aliment)
# goupement par catégorie et par pays

df_aliment_par_pays = aliments_cleaned.groupby(['countries', 'categories'])['generic_name'].count().to_frame(name="Count")


# reccuperation des pays qui ont plus de produit

df_aliment_varie = df_aliment_par_pays [df_aliment_par_pays["Count"] > 16]


aliments['packaging'].value_counts()#   count de valeur par valeur

#reccupération des magazins (Carrefour','Auchan','Leclerc')

battle = aliments[aliments['stores'].isin(['Carrefour','Auchan','Leclerc'])]

#groupement par stores et nutrition grade
battled_grouped_stores_nutrition_grade_fr = battle.groupby(['stores','nutrition_grade_fr'])['code'].count()

#groupement par store
battled_grouped_stores=battle.groupby('stores')['code'].count()

# Indicateur pour chaque store
indicator = battled_grouped_stores_nutrition_grade_fr/battled_grouped_stores

aliments[u'sugars_100g'].value_counts()

# cinq classe de sucre  labelisées
cat_sugars = pd.qcut(aliments[u'sugars_100g'],5,labels=['a','b','c','d','e'])
