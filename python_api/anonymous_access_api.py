import os
import requests
from arcgis.gis import GIS

class AnonymousApiUser(object):

    def __init__(self):

        self.gis = GIS()
        print(self.gis.properties.portalName)

    def get_json_from_item(self, item_id):

        item = self.gis.content.get(item_id)
        r = requests.get(item.url + '?f=pjson')
        data = r.json()

        print(data)
        return data

    def download_data(self, item_id):

        item = self.gis.content.get(item_id)

        file_path = r"./data"
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        item.download(save_path = file_path)
        print("downloaded {}".format(item.title))

if __name__ == '__main__':

    item_id = 'a04933c045714492bda6886f355416f2' #enter item id here
    api = AnonymousApiUser()
    api.download_data(item_id)
