# Title: api_utility_functions
#
# Purpose: Quick tasks using ArcGIS APIs
#
# Created on 5/21/18
# https://community.esri.com/thread/199333-does-anyone-have-a-python-api-recipe-for-deleting-features-in-an-arcgis-online-hosted-feature-layer-im-specifically-looking-to-clear-out-all-the-features-in-several-layers

import requests
from arcgis.gis import GIS
from getpass import getpass

class ApiUtilities(object):

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.gis = self.getGIS()

    def getGIS(self):

        gis = GIS("https://arcgis.com", self.username, self.password)
        print(f"Established Connection {gis}")

        return gis

    def delete_features(self, item_id):

        item = self.gis.content.get(item_id)
        flayer = item.layers[0]
        flayer.delete_features(where="objectid > 0")

        print("Deleted Features for {}".format(item.title))

    def clone_item(self, item_id):

        item_to_clone = self.gis.content.get(item_id)
        data = [item_to_clone]

        self.gis.content.clone_items(data, copy_data=False, search_existing_items=False)
        print("copied item {0} to {1}".format(item_to_clone.title, self.gis))

    def get_json_from_item(self, item_id):

        item = self.gis.content.get(item_id)
        r = requests.get(item.url + '?f=pjson')
        data = r.json()

        print(data)
        return data

if __name__ == '__main__':

    item_id = '53244a1d3ca447d8a890ad6bbc43621b' #enter item id here
    api = ApiUtilities('astrong_pnw', getpass())
    api.get_json_from_item(item_id)
