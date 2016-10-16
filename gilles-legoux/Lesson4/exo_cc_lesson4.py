#!/usr/bin/env python3

# standard library imports
import sys
import json
import itertools

# related third party imports
import requests
import pandas
import configparser
from bs4 import BeautifulSoup
import googlemaps


class ScrapingCities:
    CITY_FILE = 'top-french-cities-for-google-maps.csv'
    URL = 'http://www.insee.fr'

    class City:
        def __init__(self, name, population):
            self.name = name
            self.population = population

    def __init__(self):
        pass

    # public methods

    @staticmethod
    def get_cities():
        url = ScrapingCities.URL
        url += '/fr/themes/tableau.asp?reg_id=0&ref_id=nattef01214'
        result = requests.get(url)
        if result.status_code == 404:
            sys.stderr.write('ERROR: no data for url {}.\n'.format(result.url))
            exit(1)
        bs = BeautifulSoup(result.text, 'html.parser')
        table_body = bs.find('table').find('tbody', recursive=False)
        cities = []
        for row in table_body.find_all('tr', recursive=False):
            columns = row.find_all('td', recursive=False)
            city = ScrapingCities.City(
                name=columns[0].contents[0],
                population=int(columns[1].contents[0].replace(' ', ''))
            )
            cities.append(city)
        return cities

    @staticmethod
    def persist(cities):
        if len(cities) == 0:
            return pandas.DataFrame()
        city_dicts = [city.__dict__ for city in cities]
        columns = list(city_dicts[0].keys())
        df = pandas.DataFrame(city_dicts, columns=columns)
        df.to_csv(ScrapingCities.CITY_FILE, index=False)
        return df


class GoogleMapsAPIClient:
    """
    References
    ----------
    https://console.developers.google.com/apis/credentials
    https://console.developers.google.com/iam-admin
    
    """
    FORMAT = 'json'
    URL = 'https://maps.googleapis.com/maps/api/{function}/' + FORMAT
    DATA_FILE = 'flat-distance-matrix-google-maps.csv'
    CONFIG = 'CONFIG_GOOGLE_MAPS'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(GoogleMapsAPIClient.CONFIG)
        self.api_key = self.config['default']['api_key']

    # public methods

    def get_distance_matrix(self,
                            city_names,
                            persistence=True,
                            verbose=True,
                            batch_size=10):
        chunks = [city_names[x:x + batch_size]
                  for x in range(0, len(city_names), batch_size)]
        distance_list = []
        for origins in chunks:
            for destinations in chunks:
                raw_data = \
                    self._get_distance_matrix_raw_data(origins,
                                                       destinations)
                distances = \
                    GoogleMapsAPIClient._parse_result_distance_matrix(raw_data)
                distance_list.extend(distances)
                if verbose:
                    print(distances)
        if persistence:
            GoogleMapsAPIClient.persist(distance_list)
        return distance_list

    @staticmethod
    def persist(list_of_dicts, file_name=DATA_FILE):
        if len(list_of_dicts) == 0:
            return pandas.DataFrame()
        df = pandas.DataFrame(
            list_of_dicts,
            columns=list(list_of_dicts[0].keys())
        )
        df.to_csv(file_name, index=False)
        return df

    # private methods

    def _get_distance_matrix_raw_data(self, origins, destinations):
        """
        References
        ----------
        https://developers.google.com/maps/documentation/distance-matrix
        
        """
        options = {'function': 'distancematrix'}
        url = GoogleMapsAPIClient.URL.format(**options)
        result = requests.get(url,
                              params={'units': 'metric',
                                      'origins': '|'.join(origins),
                                      'destinations': '|'.join(destinations),
                                      'key': self.api_key
                                      }
                              )
        return json.loads(result.text)

    @staticmethod
    def _parse_result_distance_matrix(raw_data):

        def error(raw_data):
            sys.stderr.write(
                'ERROR: no correct data:\n {}.\n'.format(raw_data))
            sys.exit(1)

        def clean(addresses):
            return [address.split(',')[0] for address in addresses]

        def get_data(element):
            result = {}
            if element['status'] != 'OK':
                result['duration'] = 'NA'
                result['distance'] = 'NA'
            else:
                result['duration'] = element['duration']['value']
                result['distance'] = element['distance']['value']
            return result

        try:
            if raw_data['status'] != 'OK':
                error(raw_data)

            destinations = clean(raw_data['destination_addresses'])
            origins = clean(raw_data['origin_addresses'])
            distance_matrix = \
                [[get_data(element)
                  for element in row['elements']]
                 for row in raw_data['rows']]
            for i, origin in enumerate(origins):
                for j, destination in enumerate(destinations):
                    distance_matrix[i][j]['edge'] = \
                        '{}-{}'.format(origin, destination)
            return list(itertools.chain(*distance_matrix))

        except KeyError:
            error(raw_data)


def get_distance_matrix_with_library(city_names):
    """
    Without manage error.

    References
    ----------
    https://github.com/googlemaps/google-maps-services-python
    
    """

    def clean_and_save(distances, city_names, indicator, type_indicator):
        clean_distances = []
        for row in distances:
            clean_distances.append(
                map(lambda x: x[indicator][type_indicator], row['elements']))
        df = pandas.DataFrame(clean_distances,
                              index=city_names,
                              columns=city_names)
        df.to_csv('client-api-{}-{}-google-maps.csv'
                  .format(indicator, type_indicator))
        return clean_distances

    config = configparser.ConfigParser()
    config.read(GoogleMapsAPIClient.CONFIG)
    api_key = config['default']['api_key']

    gmaps = googlemaps.Client(key=api_key)
    distances = gmaps.distance_matrix(city_names, city_names)['rows']

    indicators = ['duration', 'distance']
    type_indicators = ['value', 'text']

    for indicator in indicators:
        for type_indicator in type_indicators:
            clean_and_save(distances, city_names, indicator, type_indicator)


if __name__ == "__main__":
    # scraping cities
    cities = ScrapingCities.get_cities()
    ScrapingCities.persist(cities)
    city_names = [city.name for city in cities]
    # without library
    client = GoogleMapsAPIClient()
    client.get_distance_matrix(city_names[:10])
    # with library
    get_distance_matrix_with_library(city_names[:10])
