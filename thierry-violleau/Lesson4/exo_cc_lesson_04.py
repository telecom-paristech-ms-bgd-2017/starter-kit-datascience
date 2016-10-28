import math
import urllib
import zipfile
from os import path
from time import sleep

import pandas as pd
import requests

# Goal: Retrieve the distance/travel time between the 30 most important cities (as per their number of inhabitants).


# Url to the Google Map API (JSON format).
# https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=Washington,DC&destinations=New+York+City,NY&key=YOUR_API_KEY
Google_map_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
# The Google Maps Distance Matrix API has the following limits in place:
#   - Maximum of 25 origins or 25 destinations per request.
#   - 100 elements per request.
#   - 100 elements per second, calculated as the sum of client-side and server-side queries.
Google_map_request_limit = 100

# Url to the INSEE web site to retrieve French cities statistics (as Zipped Excel file).
Insee_url = "http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/base-cc-resume-stat/"
Insee_city_stats_file = "base_cc_resume_20161013"

# Common HTTP request query parameters (template), if any
Params = {
    'unit': 'metrics',
    'origins': '<origin cities>',
    'destinations': '<destination cities>',
    'key': '<key>'
}


# Retrieves the <nb> top french city names (according to their respective population size);
# returns a data frame containing the names of the top french cities.
def get_top_cities(nb):
    cities_df = load_city_stats(Insee_url, Insee_city_stats_file)
    return cities_df.sort_values(by='P13_POP', ascending=False)['LIBGEO'][0:nb]


# Retrieves the distances between the provided cities;
# returns a data frame containing the matrix of distances between every two cities.
def get_intercity_distance(cities, key):
    result_df = None
    for orig_chunk in chunk_list(cities.values, int(math.sqrt(Google_map_request_limit))):
        df1 = None
        for dest_chunk in chunk_list(cities.values, int(math.sqrt(Google_map_request_limit))):
            data = submit_request(key, orig_chunk, dest_chunk)
            if data is not None:
                print(data)
                df = read_json(data)
                df1 = df if df1 is None else df1.join(df, how='outer')
        result_df = df1 if result_df is None else result_df.append(df1)
    return result_df


# Loads the Google API key from the designated file;
# returns the key as a string.
# The Google API key must be obtained via "https://developers.google.com/maps/documentation/distance-matrix/get-api-key"
# and saved in a file locally.
def load_api_key(filename):
    with open(filename, 'r') as file:
        key = file.readline().strip()
        return key


# Submits the HTTP Get requests to the Google Map API to retrieve the distances between the provided origin and destination
#  cities;
# returns a JSON data structure (as nested dictionaries) or 'None' if any unrecoverable error occurred.
def submit_request(key, origin_cities, destination_cities):
    for attempt in range(0, 3):
        url = Google_map_url
        params = Params.copy()
        params['key'] = key
        params['origins'] = "|".join(origin_cities)
        params['destinations'] = "|".join(destination_cities)
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            print(data)
            if data['status'] == 'OK':
                return data
            else:
                print("API Error %s... retrying (attempt %d)..." % (data['status'], attempt))
                if data['status'] == 'OVER_RATE_LIMIT':
                    sleep(2)
                elif data['status'] == 'OVER_QUERY_LIMIT':
                    print("Retry tomorrow...")
                    break
        else:
            print("HTTP Error %d [%s]... retrying (attempt %d)..." % (r.status_code, r.reason, attempt))
    return None


# Reads the relevant data fro; the provided JSON data structure;
# returns a data frame containing the matrix of distances between every two cities.
def read_json(data):
    columns = data['destination_addresses']
    orig = data['origin_addresses']
    df = pd.DataFrame(columns=columns)
    orig.reverse()
    for row in data['rows']:
        r = []
        for element in row['elements']:
            r.append(element['distance']['value'])
        other = pd.DataFrame([r], columns=df.columns, index=[orig.pop()])
        df = df.append(other)
    return df


# Splits the provided lists into chunks of th especified length;
# returns a generator of chunks of the specified length.
def chunk_list(l, n):
    return (l[i:i + n] for i in range(0, len(l), n))


# Loads the french cities statistics from the specified Url.
# returns a data frame containing the name and the population size of all the french cities.
def load_city_stats(url, filename):
    zipfilename = filename + '.zip'
    Location = url + zipfilename
    if not (path.isfile(filename + '.xls')):
        urllib.request.urlretrieve(Location, zipfilename)
        zip = zipfile.ZipFile(zipfilename)
        zip.extractall()
    na_values = ['?', '']
    fields = "B,E"
    skiprows = 5
    df = pd.read_excel(filename + '.xls', sep=';', na_values=na_values, parse_cols=fields, skiprows=skiprows)
    return df


def test(top_cities_nb=30):
    top_cities_df = get_top_cities(top_cities_nb)
    print(top_cities_df)
    print(get_intercity_distance(top_cities_df, load_api_key('GoogleAPI.key')))

test(top_cities_nb=10)