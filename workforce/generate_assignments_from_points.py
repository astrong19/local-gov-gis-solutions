# Title: generate_assignments_from_points.py
#
# Purpose: create a new workforce assignment when a point is added to an application
# such as the water service request app: http://pnw.maps.arcgis.com/apps/GeoForm/index.html?appid=72dab4d5a06248a9a21ad32a9636e3e6
#
# Helpful links:
# https://github.com/Esri/workforce-scripts/blob/master/create_assignments_from_csv_readme.md
# https://github.com/Esri/workforce-scripts/blob/master/scripts/create_assignments_from_csv.py

import csv
import ast
import dateutil
import datetime
import pandas as pd
from arcgis.gis import GIS
from getpass import getpass
from arcgis.apps import workforce

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

def get_csv_from_fs(gis, fs, output):

    print("download app fs as csv")
    fservice = gis.content.get(fs)
    flayer = fservice.layers[0]
    features = flayer.query()
    df = features.df
    #df = df.where((pd.notnull(df)), None) change all nans to None
    fs_csv = df.to_csv(output)
    print(f"csv exported to {output}")

    reformat_shape_field(output)

def reformat_shape_field(output):

    pd_csv = pd.read_csv(output)
    xy_column = pd_csv['SHAPE']

    #iterative over rows
    for row in range(0, len(pd_csv)):
        xy_dict = ast.literal_eval(xy_column[row])
        x = xy_dict['x']
        y = xy_dict['y']
        pd_csv['x'] = x
        pd_csv['y'] = y

    pd_csv = pd_csv.to_csv(output)
    print(f"added x, y fields to {output}")

def define_project(gis, project_id):

    workforce_item = gis.content.get(project_id)
    workforce_project = workforce.Project(workforce_item)

    #fetch assignment types
    assignment_types = workforce_project.assignment_types.search()
    assignment_type_dict = {}
    for assignment_type in assignment_types:
        assignment_type_dict[assignment_type.name] = assignment_type

    # Fetch dispatchers
    dispatchers = workforce_project.dispatchers.search()
    dispatchers_dict = {}
    for dispatcher in dispatchers:
        dispatchers_dict[dispatcher.user_id] = dispatcher

    # Fetch the workers
    workers = workforce_project.workers.search()
    workers_dict = {}
    for worker in workers:
        workers_dict[worker.user_id] = worker

    print("returning project definition dictionaries")

    return workforce_project, assignment_type_dict, dispatchers_dict, workers_dict

def create_assignments(gis, fs_csv, workforce_project, assignment_type_dict, dispatchers_dict, workers_dict):
    #TODO add due date argument

    print("creating workforce assignments from csv")

    #append assignments from csv to list
    assignments_in_csv = []
    with open(fs_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            assignments_in_csv.append(row)

    assignments_to_add = []
    for assignment in assignments_in_csv:
        assignment_to_add = workforce.Assignment(workforce_project)
        # Create the geometry
        geometry = dict(x=float(assignment['x']),
                        y=float(assignment['y']),
                        spatialReference=dict(
                            wkid=int(3857)))
        assignment_to_add.geometry = geometry

        # Set the assignment type
        assignment_to_add.assignment_type = assignment_type_dict["Sewer Odor"]

        #add location??
        assignment_to_add.location = assignment['SHAPE']

        #set description
        assignment_to_add.description = "this is a test"

        #set priority
        assignment_to_add.priority = "High"

        #Set dispatcher
        (k, v), = dispatchers_dict.items()
        assignment_to_add.dispatcher = dispatchers_dict[k]

        #set worker and assign
        (k, v), workers_dict.items()
        assignment_to_add.worker = workers_dict[k]
        assignment_to_add.status = "assigned"

        #add date
        assignment_to_add.assigned_date = datetime.datetime.utcnow()

        # Add all assignments to the list created
        assignments_to_add.append(assignment_to_add)

        #load assignments
        assignments = workforce_project.assignments.batch_add(assignments_to_add)

    print("created new assignment")

if __name__ == '__main__':

    gis = authenticate("astrong_pnw", getpass())

    fs = '540eee4324df4ca4b890f497e64c6486'

    get_csv_from_fs(gis, fs, "new_log_point.csv")

    workforce_project, assignment_types_dict, dispatchers_dict, workers_dict = define_project(gis, '984c9203a8e64878a441e4dcbe8cf43a')

    create_assignments(gis, "new_log_point.csv", workforce_project, assignment_types_dict, dispatchers_dict, workers_dict)
