# title:        update_feature_service.py
#
# purpose:      Overwrite or append to existing feature service in ArcGIS Online
#               or portal with data from a file path or a stable url
#               (works for csv, json or zipped shapefiles)
#
# created on:   2/21/18
#
# helpful_docs:
# https://github.com/Esri/arcgis-python-api/blob/master/samples/05_content_publishers/overwriting_feature_layers.ipynb
# https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.features.managers.html?highlight=overwrite#arcgis.features.managers.FeatureLayerCollectionManager.overwrite
# https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.features.toc.html?highlight=append#arcgis.features.FeatureLayer.append
# https://developers.arcgis.com/python/sample-notebooks/updating-features-in-a-feature-layer/
# https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.features.toc.html#feature
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection, FeatureLayer
from copy import deepcopy
import pandas as pd
import requests
import json
import csv
import io
import zipfile
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
        #if user specifies path to csv, shp or json use the path
        data = path

    elif '.zip' in url:
        #grab zipped shp
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))

        #make sure there's a shp in the zip and save to file
        if any('shp' in s for s in z.namelist()):
            open(output_path + '\\data.zip', 'wb').write(r.content)
            data = output_path + '\\data.zip'
            print("download zipped shp to {}".format(data))
        else:
            raise("[ERROR]: Zipped file must have a shapefile inside")

        return data

    elif '.csv' in url:
        #download csv from url and encode utf-8
        with requests.Session() as s:
            download = s.get(url)
            download_decoded = download.content.decode('utf-8')

        #write downloaded csv to file
        f = open(output_path + '\\data.csv', 'w')
        f.write(download_decoded)
        f.close()

        data = output_path + '\\data.csv'
        print("wrote csv to {}".format(data))

    elif '.json' or '.geojson' in url:
        #request json
        r = requests.get(url)
        geojson = r.json()

        #dump json
        with open(output_path + '\\data.json', 'w') as f:
            json.dump(geojson, f)

        data = output_path + '\\data.json'
        print("wrote json to {}".format(data))

    else:
        raise("[ERROR]: File type not found, please provide a link to a .zip, .json, .csv file")

    return data

def overwrite_service(gis, data, item):

    #get item, create collection, overwrite collection
    feature_service = gis.content.get(item)
    feature_collection = FeatureLayerCollection.fromitem(feature_service)
    feature_collection.manager.overwrite(data)

    print("[SUCCESS]: overwrote item: {0} with data {1}".format(item, data))

def append_to_service(gis, data, item, format, uniqueid):
    #step1: read csv
    new_df = pd.read_csv(data)
    print("rows, cols:{}".format(new_df.shape))

    #step2: read attribute table of feature service
    fservice = gis.content.get(item)
    flayer = fservice.layers[0]
    fset = flayer.query()
    features = fset.features
    spatial_reference = fset.spatial_reference #e.g., {'wkid': 102100, 'latestWkid': 3857}

    #step 3: overlap tables to find common features
    overlap_rows = pd.merge(left = fset.df, right = new_df, how='inner', on=uniqueid)

    #step 4: find features not shared between datasets
    new_rows = new_df[~new_df[uniqueid].isin(overlap_rows[uniqueid])]
    print("new rows, cols:{}".format(new_rows.shape))

    #step 5:new features must be a list of dicts
    new_features = new_rows.to_dict(orient='records')

    #step 6: reformat dict function
    update_dict = reformat_dict(new_rows, new_features, geom_columns=['X', 'Y'])
    print(f"updating features with {update_dict}")

    #step 7 append new data to feature service
    try:
        flayer.edit_features(adds = [update_dict])
        print("[SUCCESS]: append features")
    except:
        print("[ERROR]: Couldn't append new features. Try again, please...")

def reformat_dict(new_rows, new_features, geom_columns):

    columns = len(new_rows.columns)
    new_features_count = len(new_features)

    #reformat dict object
    update_dict = {}
    update_dict['attributes'] = {}
    update_dict['geometry'] = {}

    for col in range(0, columns):
        for feat in range(0, new_features_count):
            update_dict['attributes'][new_rows.columns[col]] = new_features[feat][new_rows.columns[col]]

    for coord in geom_columns:
        for feat in range(0, new_features_count):
            update_dict['geometry'][coord] = new_features[feat][coord]

    return update_dict

def update(gis, data, item, operation, format=None, uniqueid=None):

    if operation == 'overwrite':
        overwrite_service(gis, data, item)
    elif operation == 'append':
        append_to_service(gis, data, item, format, uniqueid)
    else:
        raise("Must specify an operation: overwrite or append")

if __name__ == '__main__':

    '''User Specified Inputs'''

    username = None #specify AGOL username here

    password = None #Specify password here

    url = "https://raw.githubusercontent.com/astrong19/local-gov-gis-solutions/master/utilities/example_csv.csv" #specify url to a .csv, .zip or .json file

    output_path = r"C:\Users\asa7362\Desktop\dev\local-gov-gis-solutions\automation" #specify your output path (string)

    item = 'e2176399e902425fb73f91e6e710bb47'#specify your ArcGIS Online Item ID (string)

    '''Get Data and Make Updates'''

    #authenticate
    gis = authenticate(username, password)

    #get data
    data = get_data(output_path=output_path, url=url)

    #update data
    update(gis, data, item, "append", format='csv', uniqueid='objectid')
