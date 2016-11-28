import json
import pandas as pd

path = '/Users/khouiyadam/Documents/charles/usagov_bitly_data2012-03-16-1331923249.txt'

records = [json.loads(line) for line in open(path)]

# print(records)

# clean_tz = frame['tz'].fillna('Missing')

cframe = frame[mask]

mask = frame.a.notnull()

indexer  = agg_count.sum(1).argsort() #  sommer les column (sum(1)) et argsort  c 'est pour générer  l 'indexe en ordre croissant

count_subset = agg_counts.take(indexer)[-10:] # reccuperer les 10 derniers element
count_subset.plot(kind='barh', stacked=True) #  stacked=True pour mettre deux element sur la méme  bar et non pas cote a cote
normed_subset = count_subset.div(count_subset.sum(1), axis=0) # diviser chaque ligne par la somme des colonnes de cette ligne (normalisation).


mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('/Users/khouiyadam/movie.dat', sep='::', header=None, names=mnames)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('/Users/khouiyadam/ratings.dat', sep='::', header=None, names=rnames)

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('/Users/khouiyadam/users.dat', sep='::', header=None,names=unames)


mean_ratings = data.pivot_table('rating',index=["title"],columns=["gender"],aggfunc='mean') #  il est modifié par rapport ce qui est dans le livre

ratings_by_title = data.groupby('title').size() # grouper par titre

active_titles = ratings_by_title.index[ratings_by_title >= 250] # reccuperer les + 250

mean_ratings = mean_ratings.ix[active_titles]

top_view_femme = mean_ratings.sort('F',ascending=False)
top_view_femme = mean_ratings.sort_index(by='F', ascending=False)

sorted_by_diff[::-1][:15] # inverser lordre de la dataframe puis reccuperer les 15 premiere lignes

sorted_data_by_std =  data.groupby('title')['title','rating'].std()


names1880 = pd.read_csv('/Users/khouiyadam/Documents/charles/names/yob1880.txt', names=['name', 'sex', 'births'])
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']

# ici on veut lire tous les fichier yob allons de 1880 à 2011
for year in years:
    path = '/Users/khouiyadam/Documents/charles/names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)
names = pd.concat(pieces, ignore_index=True)

#############################################################

train_a = pd.read_csv('/Users/khouiyadam/Documents/charles/train_a.csv')

def num_missing(x):
  return sum(x.isnull())


data.apply(num_missing, axis=0) # nombre de lignes lignes par colonne

modeEmbarked = mode(train_a.Gender.dropna())# retrouver le mode