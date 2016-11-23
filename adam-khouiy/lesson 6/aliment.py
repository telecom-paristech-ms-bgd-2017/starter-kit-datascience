import pandas as pd


df = pd.read_csv("/Users/khouiyadam/Desktop/charles/aliment.csv",encoding = "utf-8" ,delimiter ="\t" , error_bad_lines =False ,warn_bad_lines =False)

#df.ix[:,0:4].head()


#df.ix[0:5,0:4]

#df2 = df.ix[:,8:40]

#elimination des NAN   sur la colonne générique

#df2.dropna(subset = ['generic_name'],inplace = True)

#df2.drop(['countries_tags','countries_fr','packaging_tags','brands_tags','categories_tags','labels_tags'],inplace=True,axis=1)

# goupement par catégorie et par pays

#df_aliment_par_pays = df2.groupby(['countries', 'categories'])['generic_name'].count().to_frame(name="Count")

# reccuperation des pays qui ont plus de produit

#df_aliment_varie = df_aliment_par_pays [df_aliment_par_pays["Count"] > 1]


df['packaging'].value_counts() #   count de valeur par valeur

