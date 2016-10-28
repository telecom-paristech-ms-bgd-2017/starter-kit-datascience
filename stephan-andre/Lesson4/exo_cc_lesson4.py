# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:10:42 2016

@author: Stephan
"""
import requests
from bs4 import beautifulSoup
import numpy as np
import pandas as pd
import json, urllib
url = "http://www.toutes-les-villes.com/villes-population.html"
df = pd.read_csv(url, sep=r"\s+", names=u_cols, na_values='NA')

orig_coord = orig_lat, orig_lng
dest_coord = dest_lat, dest_lng
url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
result= simplejson.load(urllib.urlopen(url))
driving_time = result['rows'][0]['elements'][0]['duration']['value']