#Helpful Docs: http://esri.github.io/arcgis-python-api/apidoc/html/arcgis.gis.toc.html#contentmanager
#http://resources.arcgis.com/en/help/arcgis-rest-api/#/Search_reference/02r3000000mn000000/
#https://developers.arcgis.com/python/sample-notebooks/clone-portal-users-groups-and-content/
from arcgis.gis import GIS

def if_else(field, list_field=None, action=None):
    '''simple if else function to save space in build_query function
    :param field: query param defined in __main__
    :param list_field: specified in build_query to separate list objects
    :param action: string manipulation defined in build query_string
    :return: return manipulated field or blank string'''

    if not field:
        field = ''
    elif isinstance(field, list) and list_field=='tags':
        field_edit = ', '.join(map(str, field))
        field = 'AND tags:{}'.format(field_edit)
    elif isinstance(field, list) and list_field=='agol_id':
        length = len(field)
        field = ("OR id:%s " * (int(length))) %(tuple(field))
    elif isinstance(field, list) and list_field=='group_id':
        length = len(field)
        field = ("OR group:%s " * (int(length))) %(tuple(field))
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

    agol_id = if_else(agol_id, list_field='agol_id', action='id:{}'.format(agol_id))

    publisher = if_else(publisher, action='owner:{}'.format(publisher))

    service_type = if_else(service_type, action='type:{}'.format(service_type))

    title = if_else(title, action='title:{}'.format(title))

    group_id = if_else(group_id, list_field='group_id', action='group:{}'.format(group_id))

    tags = if_else(tags, list_field='tags')

    query = str(publisher + ' ' + service_type + ' ' + title + ' ' + group_id + ' ' + agol_id + ' ' + tags)

    #remove first AND in query string
    if 'AND' in query:
        query_string = query.split('AND ', 1)[1]
    elif 'OR' in query and 'AND' not in query:
        query_string = query.split('OR ', 1)[1]
    else:
        pass

    print("[DEBUG]: query string = {}".format(query_string))
    return query_string

def find_agol_items(gis, query, sort_field=None, sort_order=None, max_items=None):
    '''use the python API to search ArcGIS Online for items using query string
    :param gis: anonymous access gis authentification
    :param query: query string defined in build_query with params from __main__
    :param sort_field: ArcGIS Online item analytic field to sort by
    :param sort_order: asc or dsc
    :param max_items: limit search results to x items
    :return: items found in search + item name and id
    '''

    #empty list to hold item ids
    item_ids = []

    #create a for loop that queries AGOL and adds items to items list
    open_layers = gis.content.search(query='{}'.format(query), sort_field=sort_field, sort_order=sort_order, max_items=max_items)

    print("[SUCCESS]: Found {} open datasets".format(len(open_layers)))

    for layer in open_layers:
        print(layer)
        print("[DEBUG]:" + layer.title + " with layer id:" + layer.id)
        item_ids.append(layer.id)

    #return a list of item ids
    return item_ids

def clone_item(gis, item_ids, reference, folder):
    '''function to clone items found in the search to your ArcGIS Online or portal account
    :param gis: target gis specified under if name == main (the account to clone to)
    :param item_ids: the AGOL items ids found in the search
    :param reference: if true will make a reference to the existing service, if false will copy the data
    :param folder: specify where in My content to clone the data '''

    for item_id in item_ids:
        item = gis.content.get(item_id)

        if reference == True:
            gis.content.add(item, data=item.url, folder=folder)
            print("[SUCCESS]: copied reference service to ArcGIS Online for {}".format(item.title))
        elif reference == False:
            data = [item]
            gis.content.clone_items(data, folder=folder, copy_data=False, search_existing_items=False)
            print("[SUCCESS]: copied item to ArcGIS Online for {}".format(item.title))
        else:
            print("[WARNING]: reference must be specified true or false")

if __name__ == '__main__':
    '''Define parameters for the query string and ArcGIS Online/Portal access here.
    Sarch parameters are optional but at least one ust be specified. If you want to clone
    content to your ArcGIS Online or Portal account you must specify a username and password'''
    #Issue: when you login to your agol account the script only finds items that you own... not other AGOL stuff

    '''ARCGIS ONLINE PARAMS'''
    #get password needed to login to account to clone items:
    user = None #Specify your ArcGIS Online username here
    password = None #Specify your ArcGIS Online password here

    portal_url = None #if you'd like to authetnicate with your portal paste the url here
    folder = None #String, specify for cloning... so script knows where to clone content in your Org
    reference = True #Specify True if you'd like to reference an existing service url or False if you'd like to copy the data directly

    #specify target GIS account to clone content
    if portal_url:
        target_gis = GIS(portal_url, user, password)
    else:
        target_gis = GIS("https://www.arcgis.com", user, password)

    #specify anonymous GIS access to all public datasets
    gis = GIS()

    '''SEARCH PARAMS'''
    agol_id = None #List, list of ArcGIS Online ID(s) (e.g.,['7ccbaa1f4ea6421a8e58b3e3efda7903', '2c3e136e2e00435b9a875bb14d5aaf85'])

    publisher = None #String, ArcGIS Online Publisher name(e.g., 'Publisher_SacCity')

    service_type = None #String, ArcGIS Online item type (e.g., 'Feature Service')

    tags = None #List, ArcGIS Online item keywords (e.g., ['tag1', 'tag2', 'tag3'])

    title = None #String, ArcGIS Online item title (e.g., 'Fire_Stations')

    group_id = None #List, ArcGIS Online GRoup ID(s) (e.g., ['7926ad6eb91c46bd8229683d4b6a2bd1', 'f2f40cf99aa947e5961b6c69351a02dc'])

    '''RUN SEARCH AND CLONE COMMANDS'''
    #Build query with above params
    query = build_query(agol_id=agol_id, publisher=publisher, service_type=service_type, tags=tags, title=title, group_id=group_id)

    #run search with query
    items = find_agol_items(gis, query, sort_field="numViews", sort_order='asc', max_items=10)

    #run clone item command
    if user and password:
        clone_item(target_gis, items, reference, folder)
    elif not user or password:
        print("[WARNING]: must enter username and password to clone content")
        pass
