#Helpful Docs: http://esri.github.io/arcgis-python-api/apidoc/html/arcgis.gis.toc.html#contentmanager
#http://resources.arcgis.com/en/help/arcgis-rest-api/#/Search_reference/02r3000000mn000000/
from arcgis.gis import GIS

#initiate public access
gis = GIS()

def find_popular_items(publisher, service_type, tags):

    #create a for loop that queries AGOL and adds items to items list
    open_layers = gis.content.search(query='owner:{0} AND type:{1} AND tags:{2}'.format(publisher, service_type, tags), sort_field="numViews", sort_order='asc', max_items=10)

    print("Found %d open datasets" %(len(open_layers)))

    for layer in open_layers:
        print(layer)
        print("with layer id:" + layer.id)

if __name__ == '__main__':

    #create list of publishers to NorCal open data sites
    publisher = 'Publisher_SacCity'

    service_type = 'Feature Service'

    tags = 'Fire Department, Fire'

    #call script
    find_popular_items(publisher, service_type, tags)
