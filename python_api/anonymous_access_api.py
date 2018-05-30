import os
import requests
from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode
from arcgis.geometry import Point

class AnonymousApiUser(object):

    def __init__(self):

        self.gis = GIS()
        print("connected:{}".format(self.gis.properties.portalName))

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

    item_id = 'a04933c045714492bda6886f355416f2' #enter item id here
    locations = [{'Y':34.13419,
        'X':-118.29636,
       'spatialReference':{
           'wkid':4326}
       }]

    '''RUN AN OPERATION'''
    api = AnonymousApiUser()
    api.reverse_geocode(locations)
