
import googlemaps
from pandas import DataFrame, Series

API_KEY = 'BLjaSyC5jZ4jLw8bFgXoLY5RJ5IKge7CXi4zI0Q'

gmaps = googlemaps.Client(key=API_KEY)

villes = ['Paris','Lille','Marseille','Lyon','Strasbourg','Nantes','Nice','Bordeaux','Toulouse']

distances = gmaps.distance_matrix(villes, villes)['rows']

INDICATEUR = 'duration'
TYPE = 'value'

clean_distances = []
for row in distances:
  clean_distances.append(map(lambda x: x[INDICATEUR][TYPE], row['elements']))

df = DataFrame(clean_distances,index=villes,columns=villes)
df.to_csv(INDICATEUR + '.csv')