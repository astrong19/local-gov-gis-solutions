import os
import requests
from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode
from arcgis.geometry import Point

class AnonymousApiUser(object):

    def __init__(self):

        self.gis = GIS()
        print("connected: {}".format(self.gis.properties.portalName))

    def get_json_from_item(self, item_id):
        '''Access json of a feature service'''

        item = self.gis.content.get(item_id)
        r = requests.get(item.url + '?f=pjson')
        data = r.json()

        print(data)
        return data

    def download_data(self, item_id):
        '''Download data from a ArcGIS Online item'''

        item = self.gis.content.get(item_id)

        file_path = r"./data"
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        item.download(save_path = file_path)
        print("downloaded {}".format(item.title))

    def geocode(self, locations):
        '''Get coordinates from address or location name'''

        coordinates = []
        for location in locations:
            coord = geocode(location)
            coordinates.append(coord)

        print(coordinates)
        return coordinates

    def reverse_geocode(self, locations):
        '''Get address from coordinate pairs'''

        addresses = []
        for location in locations:
             unknown_pt = Point(location)
             address = reverse_geocode(unknown_pt)
             addresses.append(address)

        print(addresses)
        return addresses

if __name__ == '__main__':
    '''USER SPECIFIED VARIABLES'''
    #ArcGIS Online Item ID
    item_id = 'a04933c045714492bda6886f355416f2'
    #If reverse geocoding, list coordinates as dictionaries
    #If geocoding list addresses or place names
    locations = ['1315 10th St B-27, Sacramento, CA 95814']

    '''RUN AN OPERATION'''
    #Initalize class
    api = AnonymousApiUser()
    #Specify class method
    api.geocode(locations)
