# -*- coding: utf-8 -*-
import googlemaps

# chercher les les 30 villes les + importantes
origins = ['Paris', 'Nice','Marseille']
destinations = ['Paris', 'Nice','Marseille']


gmaps = googlemaps.Client(api_key='AIzaSyCYEzx4X2oCbRI9rNJAt-o6bO8Ju9ZGHGQ')



resultat = gmaps.distance_matrix(origins, destinations)

print (resultat)

#for item in resultat:
#print ('origin: %s' % item.origin)
#	print ("origin:", item.origin)
#	print ('destination: %s' % item.destination)
#	print ('km: %s' % item.distance.kilometers)
#	print ('m: %s' % item.distance.meters)
#	print ('miles: %s' % item.distance.miles)
#	print ('duration: %s' % item.duration) # returns string.
#	print ('duration datetime: %s' % item.duration.datetime) # returns datetime.