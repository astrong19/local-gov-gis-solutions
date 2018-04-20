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

def create_filter(geom):

    # Setup Geometry Filter
    filter = {
        "type": "GeometryFilter",
        "field_name": "geometry",
        "config": geom
    }

    return filter

def request_imagery_for_aoi(session, url, filter, item_types):

    request = {
        "item_types": item_types,
        "filter": filter
    }

    # Send the POST request to the API stats endpoint
    res = session.post(url, json=request)

    # Print response
    p(res.json())

if __name__ == '__main__':

    api_key = util.get_token('planet_api.json')["planet_api"]

    planet_data_url = "https://api.planet.com/data/v1"

    stats_url = f"{planet_data_url}/stats"

    quick_url = f"{planet_data_url}/quick-search"

    aoi = json.load(open('aoi.json'))

    session = authenticate(api_key, planet_data_url)

    filter = create_filter(aoi)

    request_imagery_for_aoi(session, quick_url, filter, ["PSScene3Band", "REOrthoTile"])
