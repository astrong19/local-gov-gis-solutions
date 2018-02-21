#
# Helpful Docs:
# https://github.com/Esri/arcgis-python-api/blob/master/guide/04-feature-data-and-analysis/editing-features.ipynb
import arcpy
from arcgis.gis import GIS

def authenticate(user, password, portal_url=None):

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

def update_service(gis, item_id, data_dict):

    #get feature layer
    item = gis.content.get(item_id)
    item_layer = item.layers[0]

    if 'Update' not in item_layer.properties.capabilities:
        arcpy.AddError("feature service does not have update capabilities enabled")
    else:
        item_layer.edit_features(adds = [data_dict])
        arcpy.AddMessage("Updated {0} with new data: {1}".format(item_id, data_dict))

if __name__ == '__main__':


    item_id = arcpy.GetParameterAsText(0) #string, ArcGIS Online Item ID


    username = arcpy.GetParameterAsText(1)

    password = arcpy.GetParameterAsText(2)

    gis = authenticate(username, password)

    data_dict = {'geometry': {'x': -12484306.9558, 'y': 6589483.33441}, 'attributes': {'ObjectId': 6}}

    update_service(gis, item_id, data_dict)
