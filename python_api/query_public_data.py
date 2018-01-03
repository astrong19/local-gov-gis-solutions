#find and use open ArcGIS data without an ArcGIS Online account or software license
from arcgis.gis import GIS

#initiate class
gis = GIS()

#search for data by in Sac's open data site: http://data.cityofsacramento.org/datasets
open_layers = gis.content.search(query='owner:Publisher_SacCity AND type:Feature Service', sort_field="numViews", sort_order='asc', max_items=100)

#print layers
for layer in open_layers:
    print(layer)

#select layer
most_viewed_layer = gis.content.search(query='owner:Publisher_SacCity AND type:Feature Service', sort_field="numViews", sort_order='asc', max_items=1)
for layer in most_viewed_layer:
    item_id = layer.id

sac_layer = gis.content.get(item_id)
print('the most viewed layer in Sac Open data is %s' %(sac_layer))
