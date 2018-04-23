#https://github.com/Qberto/ArcGISPythonAPI_Projects/blob/master/Presentation/TensorFlow_ObjectDetection_Demo02_Stream.ipynb
#https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/data-api-tutorials/planet_data_api_introduction.ipynb
import json
import requests
import sys
sys.path.append("..")

from utilities import util

def p(data):
    print(json.dumps(data, indent=2))

def authenticate(api_key, planet_data_url):

    session = requests.Session()
    session.auth = (api_key, "")

    res = session.get(planet_data_url)

    if res.status_code == 200:
        p(res.json())
    else:
        print("[ERROR]: Something went wrong")

    return session

def create_filter(geom, gt_year, lt_year=None):

    # Setup Geometry Filter
    geom_filter = {
        "type": "GeometryFilter",
        "field_name": "geometry",
        "config": geom
    }

    date_filter = {
      "type": "DateRangeFilter",
      "field_name": "acquired",
      "config": {
        "gt": f"{gt_year}-01-01T00:00:00Z",
        }
    }

    and_filter = {
    "type": "AndFilter",
    "config": [geom_filter, date_filter]
    }

    return geom_filter, date_filter, and_filter

def request_imagery_for_aoi(session, url, filter, item_types):

    request = {
        "item_types": item_types,
        "interval": "year",
        "filter": filter
    }

    # Send the POST request to the API stats endpoint
    res = session.post(url, json=request).json()

    # Print response
    features = res['features']
    print("total features: {}".format(len(features)))
    Fids = []
    data_dict = {}
    for f in features:
        data_dict[f['id']] = {}
        data_dict[f['id']]['permissions'] = f['_permissions']
        data_dict[f['id']]['assets'] = f['_links']['assets']
        print("added {} to asset_dict".format(f['id']))

    return data_dict

def status_code(status):

    if status == 202:
        print("The request has been accepted and the activation will begin shortly.")
    elif status == 204:
        print("The asset is already active and no further action is needed.")
    elif status == 401:
        print("The user does not have permissions to download this file.")
    else:
        print("something went wrong")

def activate(session, data_dict):

    assets = {}

    for image_id in data_dict.keys():
        res = session.get(data_dict[image_id]['assets'])
        asset = res.json()
        activation_url = asset['visual']['_links']['activate']
        assets[image_id] = {}
        assets[image_id]['activation_url'] = activation_url

    res_activate = session.get(assets[next(iter(assets))]['activation_url'])

    # Print the response from the activation request
    print(res.status_code)
    status_code(res.status_code)

if __name__ == '__main__':

    api_key = util.get_token('planet_api.json')["planet_api"]

    planet_data_url = "https://api.planet.com/data/v1"

    stats_url = f"{planet_data_url}/stats"

    quick_url = f"{planet_data_url}/quick-search"

    aoi = json.load(open('aoi.json'))

    filter = create_filter(aoi, '2013')[2]

    session = authenticate(api_key, planet_data_url)

    data_dict = request_imagery_for_aoi(session, quick_url, filter, ["PSScene3Band", "REOrthoTile"])

    activate(session, data_dict)
