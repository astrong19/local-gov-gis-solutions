# Name:         gp_tool_edit_service.py
#
# Function:     A script tool that can be added to an ArcGIS Python toolbox that
#               will update data in ArcGIS Online with data on your local computer
#
# Created:      2/21/18
#
# Helpful Docs:
# https://github.com/Esri/arcgis-python-api/blob/master/guide/04-feature-data-and-analysis/editing-features.ipynb
# https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.features.toc.html?highlight=edit_features#arcgis.features.FeatureLayer.edit_features
# http://pro.arcgis.com/en/pro-app/arcpy/geoprocessing_and_python/defining-parameter-data-types-in-a-python-toolbox.htm

import arcpy
from arcgis.gis import GIS

def authenticate(user, password, portal_url=None):

    #authenticate with portal or AGOL
    if portal_url:
        arcpy.AddMessage("[DEBUG]: Using Portal for ArcGIS")
        gis = GIS(portal_url, user, password)
    elif user and not portal_url:
        arcpy.AddMessage("[DEBUG]: Using ArcGIS Online")
        gis = GIS("https://www.arcgis.com", user, password)
    else:
        arcpy.AddMessage("[DEBUG]: Using anonymous access to ArcGIS Online")
        gis = GIS()

    return gis

def get_data_dict(gdb, layer):
    #tranform data into dictionary
    arcpy.env.workspace = gdb
    fjson = arcpy.FeaturesToJSON_conversion(layer, "features9.json")

    #open json and assign dictionary to variable
    open_file = open(fjson[0], 'r')
    json_data = open_file.read()
    data = eval(json_data)

    #grab features (geom/attributes)
    features = data['features']
    arcpy.AddMessage("converted {} to json".format(layer))

    return features

def update_service(gis, item_id, data_dict):

    #get feature layer
    item = gis.content.get(item_id)
    item_layer = item.layers[0]

    #make sure update capability is enabled, then update
    if 'Update' not in item_layer.properties.capabilities:
        arcpy.AddError("feature service does not have update capabilities enabled")
    else:
        item_layer.edit_features(adds = data_dict)
        arcpy.AddMessage("Updated {0} with new data: {1}".format(item_id, data_dict))

if __name__ == '__main__':

    #input params defined here
    gdb = arcpy.GetParameterAsText(0) #string, path to geodatabase

    layer_name = arcpy.GetParameterAsText(1) #string, layer name in gdb

    item_id = arcpy.GetParameterAsText(2) #string, ArcGIS Online Item ID

    username = arcpy.GetParameterAsText(3) #string, ArcGIS Online username

    password = arcpy.GetParameterAsText(4) #string, ArcGIS Online password

    gis = authenticate(username, password) #authenticate

    data_dict = get_data_dict(gdb, layer_name) #get dictionary from input data

    update_service(gis, item_id, data_dict) #update service
