# Title: generate_assignments_from_points.py
#
# Purpose: create a new workforce assignment when a point is added to an application
# such as the water service request app: https://solutions.arcgis.com/utilities/water/help/water-service-request/
# Or a survey 123 form:
#
# Helpful links:
# https://github.com/Esri/workforce-scripts/blob/master/create_assignments_from_csv_readme.md
# https://github.com/Esri/workforce-scripts/blob/master/scripts/create_assignments_from_csv.py
# https://gis.stackexchange.com/questions/143781/getting-items-from-ordereddict-to-parse-addresses?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
import csv
import os
import ast
import dateutil
import datetime
import pandas as pd
from arcgis.gis import GIS
from getpass import getpass
from arcgis.apps import workforce
from collections import OrderedDict

def authenticate(user, password, portal_url=None):
    '''authenticate with ArcGIS Online or portal
    :param user: username to agol or portal
    :param password: password for agol or portal
    :param portal_url: if using portal, specify enterprise url here
    :return: instance with permissions to the named user account
    '''

    if portal_url:
        gis = GIS(portal_url, user, password)
        print("[DEBUG]: Using Portal for ArcGIS")
    elif user and not portal_url:
        gis = GIS("https://www.arcgis.com", user, password)
        print(f"[DEBUG]: Using ArcGIS Online: {gis}")
    else:
        gis = GIS()
        print("[DEBUG]: Using anonymous access to ArcGIS Online")

    return gis

def get_csv_from_fs(gis, fs, output):
    '''download a csv from feature service
    :param gis: authenticated instance
    :param fs: id to the feature service item in ArcGIS Online or Porta
    :param fs_csv: the output path and file name for the csv'''

    print("download app fs as csv")
    fservice = gis.content.get(fs)
    flayer = fservice.layers[0]
    features = flayer.query()
    df = features.df
    #df = df.where((pd.notnull(df)), None) change all nans to None
    fs_csv = df.to_csv(output)
    print(f"csv exported to {output}")

    #send to reformat method
    reformat_shape_field(output)

def reformat_shape_field(output):
    '''add x, y from the dictionary in the csv's shape field
    :param fs_csv: output path and file name of edited csv'''

    pd_csv = pd.read_csv(output)

    #iterative over rows
    for index, row in pd_csv.iterrows():
        xy_dict = ast.literal_eval(row['SHAPE'])
        print(f"xy_dict: {xy_dict}")
        x = xy_dict['x']
        y = xy_dict['y']
        pd_csv.set_value(index, 'x', x)
        pd_csv.set_value(index, 'y', y)

    pd_csv = pd_csv.to_csv(output)
    print(f"added x, y fields to {output}")

def list_assignments_incsv(fs_csv):
    '''append each row in csv to a dictionary in a list and return the list
    :param fs_csv: csv generated from feature service
    :return assignments_in_csv: list of each row in csv'''

    print("creating workforce assignments from csv")

    #append assignments from csv to list
    assignments_in_csv = []
    with open(fs_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"row: {row}")
            assignments_in_csv.append(row)

    print(f"assignments_in_csv: {assignments_in_csv}")

    return assignments_in_csv

def define_project(gis, project_id):
    '''read workforce project and add parameters to dictionaries
    :param gis: instance authenticated with AGOL or Portal account
    :param project_id: workforce item id
    :return: three dictionaries describing workforce parameters'''

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

    return workforce_project, assignment_type_dict, dispatchers_dict, workers_dict

def create_assignments(assignments_in_csv, workforce_project, assignment_types_dict, dispatchers_dict, workers_dict):
    '''add assignments to workforce project
    :param assignments in csv: list of dictionaries of each record in feature fservice
    :param workforce_project: workforce project defined in define_project
    :param assignment_type_dict: assignment types dict defined in define_project
    :param dispatchers_dict: dispatchers dictionary defined in define_project
    :param workers_dict: workers dictionary defined in define_project'''

    assignments_to_add = []
    for assignment in assignments_in_csv:
        print(f"assignment: {assignment}")
        assignment_to_add = workforce.Assignment(workforce_project)
        # Create the geometry
        geometry = dict(x=float(assignment['x']),
                        y=float(assignment['y']),
                        spatialReference=dict(
                            wkid=int(4326)))
        print(geometry)
        assignment_to_add.geometry = geometry

        fs_assignment_type = assignment['type_of_issue']
        assignment_to_add.assignment_type = assignment_types_dict[fs_assignment_type]
        print(f"Added type {fs_assignment_type}")

        assignment_to_add.location = assignment['address']
        print("Added address")

        assignment_to_add.description = assignment['add_details']
        print("Added details")

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
    '''USER DEFINED PARAMETERS- this is the important stuff, that make this script run'''

    '''USER SPECIFIED VARIABLES'''
    #specify AGOL username and password here
    gis = authenticate("astrong_pnw", getpass())

    #specify feature service ArcGIS Online Item ID here
    fs = '48357ff7b632461bb99b7f51b14fcd71'

    #specify workforce project ID here
    project_id = 'cd726615306f407396bacfbe1b5019e8'

    #specify output directory here
    output = r"data/new_log_point.csv"

    '''RUN SCRIPT'''
    get_csv_from_fs(gis, fs, output)
    assignments_in_csv = list_assignments_incsv(output)
    print(f"assignments in csv: {assignments_in_csv}")
    workforce_project, assignment_types_dict, dispatchers_dict, workers_dict = define_project(gis, project_id)
    create_assignments(assignments_in_csv, workforce_project, assignment_types_dict, dispatchers_dict, workers_dict)
