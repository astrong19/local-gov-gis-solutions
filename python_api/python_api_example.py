# coding: utf-8
from arcgis import GIS
from IPython.display import display
import sys
sys.path.append("..")

from utilities import util

user = util.get_token('agol_creds.json')["username"]
password = util.get_token('agol_creds.json')["password"]
gis = GIS("https://www.arcgis.com", user, password)

#print items
items = gis.content.search('Parking Inventory')
for item in items:
    display(item)

#print item ids
for item in items:
    print(item.id)

#print item tags
for item in items:
    print(item.tags)

#access item
Parking_Map_Item = gis.content.get('a19d6a0e34a4421bba5f15d95f28b722')

#Display item
Parking_Map_Item

#update item tags
Parking_Map_Item.update(item_properties={'tags':'python, api, is, awesome'})

#Print parking layer feature service url
Parking_Layer = gis.content.get('d8c6ad6734d947a784942380b1fa835c')
feature_service = Parking_Layer.url
print(feature_service)

#get item json
import requests
import json

r = requests.get(feature_service + "?f=pjson")
data = r.json()
data_pretty = json.dumps(data, indent=2)
print(data_pretty)
