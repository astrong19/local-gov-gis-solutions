# title:        update_feature_service.py
#
# purpose:      Overwrite or append to existing feature service with data from a
#               file path or a stable url
#
# helpful_docs:
# https://github.com/Esri/arcgis-python-api/blob/master/samples/05_content_publishers/overwriting_feature_layers.ipynb
import requests
import json
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import sys
sys.path.append("..")

from utilities import util

def authenticate(user, password, portal_url=None):

    if portal_url:
        print("[DEBUG]: Using Portal for ArcGIS")
        gis = GIS(portal_url, user, password)
    elif user and not portal_url:
        print("[DEBUG]: Using ArcGIS Online")
        gis = GIS("https://www.arcgis.com", user, password)
    else:
        print("[DEBUG]: Using anonymous access to ArcGIS Online")
        gis = GIS()

    return gis

def get_data(output_path, url, path=None):

    if path:
        data = path
    elif url.endswith('zip'):
        #dox
        pass #working progress
    elif url.endswith('json'):

        #request json
        r = requests.get(url)
        geojson = r.json()

        #dump json
        with open(output_path + '\\data.json', 'w') as f:
            json.dump(geojson, f)

        data = output_path + '\\data.json'

    elif url.endwith('csv'):
        #doy
        pass #working progress
    else:
        print("[ERROR]: File type not found, please provide a link to a .zip, .json, .csv file")

    return data

def overwrite_service(gis, data, item):

    #get item, create collection, overwrite collection
    feature_service = gis.content.get(item)
    feature_collection = FeatureLayerCollection.fromitem(feature_service)
    feature_collection.manager.overwrite(data)

    print("[SUCCESS]: overwrote item: {0} with data {1}".format(item, data))

def append_to_service(gis, data, item):

    pass #working progress
    feature_service = gis.content.get(item)
    arcpy.Append_management(data, feature_service, "TEST")

if __name__ == '__main__':

    username = util.get_token('agol_creds.json')["username"]

    password = util.get_token('agol_creds.json')["password"]

    gis = authenticate(username, password)

    url = "https://raw.githubusercontent.com/astrong19/local-gov-gis-solutions/master/utilities/example.json"

    output_path = r"C:\Users\asapc\Desktop\dev\data"

    item = '9c6230bab74743f7ae4b54f3b34dfba4'

    #get data
    data = get_data(output_path=output_path, url=url)

    #overwrite data
    overwrite_service(gis, data, item)
