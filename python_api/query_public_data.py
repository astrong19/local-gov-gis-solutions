#Helpful Docs: http://esri.github.io/arcgis-python-api/apidoc/html/arcgis.gis.toc.html#contentmanager
#http://resources.arcgis.com/en/help/arcgis-rest-api/#/Search_reference/02r3000000mn000000/
#https://developers.arcgis.com/python/sample-notebooks/clone-portal-users-groups-and-content/
from arcgis.gis import GIS

#initiate public access
gis = GIS()

def if_else(field, action):
    '''simple if else function to save space in build_query function
    :param field: query param defined in __main__
    :param action: string manipulation defined in build query_string
    :return: return manipulated field or blank string'''

    if not field:
        field = ''
    else:
        field_edit = action
        field = ' AND {}'.format(field_edit)

    return field

def build_query(agol_id=None, publisher=None, service_type=None, tags=None, title=None, group_id=None):
    '''function that builds a query string using parameters set in __main__
    :param agol_id: ArcGIS Online unique id
    :param publisher: ArcGIS Online publisher account __name__
    :param service type: ArcGIS Online service service_type
    :param tags: list of keywords used to filter Search_reference
    :param title: title of the item in ArcGIS Online
    :param group_id: unique ID of the ArcGIS Online group the item belongs to
    :return: a query string with the above params'''

    agol_id = if_else(agol_id, 'id:{}'.format(agol_id))

    publisher = if_else(publisher, 'owner:{}'.format(publisher))

    service_type = if_else(service_type, 'type:{}'.format(service_type))

    title = if_else(title, 'title:{}'.format(title))

    group_id = if_else(group_id, 'group:{}'.format(group_id))

    if not tags:
        tags = ''
    else:
        tags = if_else(tags, ', '.join(map(str, tags)))

    query = str(agol_id + publisher + service_type + tags + title + group_id)
    query_string = query.split('AND ', 1)[1]

    print(query_string)
    return query_string

def find_agol_items(query, sort_field=None, sort_order=None, max_items=None):
    '''use the python API to search ArcGIS Online for items using query string
    :param query: query string defined in build_query with params from __main__
    :param sort_field: ArcGIS Online item analytic field to sort by
    :param sort_order: asc or dsc
    :param max_items: limit search results to x items
    :return: items found in search + item name and id
    '''

    #create a for loop that queries AGOL and adds items to items list
    open_layers = gis.content.search(query='{}'.format(query), sort_field=sort_field, sort_order=sort_order, max_items=max_items)

    print("Found {} open datasets".format(len(open_layers)))

    for layer in open_layers:
        print(layer)
        print(layer.title + " with layer id:" + layer.id)

    #return a list of open layers found in the api query... also print for ref
    print(open_layers)
    return open_layers

if __name__ == '__main__':
    '''Define parameters for query string here and run the search
    params are optional'''


    agol_id = None # String, ArcGIS Online Item ID (e.g.,'614bdde2a4714b2098d4c2532fd2c6e7')

    publisher = None #String, ArcGIS Online Publisher name(e.g., 'Publisher_SacCity')

    service_type = None #String, ArcGIS Online item type (e.g., 'Feature Service')

    tags = None #List, ArcGIS Online item tags (e.g., ['Fire Department, .sd'])

    title = None #String, ArcGIS Online item title (e.g., 'Fire_Stations')

    group_id = None #String, ArcGIS Online GRoup ID (e.g., 'f2f40cf99aa947e5961b6c69351a02dc')

    #Build query with above params
    query = build_query(agol_id=agol_id, publisher=publisher, service_type=service_type, tags=tags, title=title)

    #run search with query
    find_agol_items(query, sort_field="numViews", sort_order='asc', max_items=10)
