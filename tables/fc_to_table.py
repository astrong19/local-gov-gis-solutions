#-----------------------------------------------------------------------------------------------
# Name:         fc_to_table.py
#
# Purpose:      Copy fields from a gdb feature class to a table
#
# Notes:        Written in Python 3.5 but should work in 2.7 (just rework print statements)
#               Requires ArcPy
#               All params are specified under if __name__ == '__main__'
#               This script is designed to run from the command line (e.g., python fc_to_table.py)
#
# Created:      12/21/2017
#
# Helpful links:
# http://pro.arcgis.com/en/pro-app/arcpy/classes/fieldmappings.htm
#-------------------------------------------------------------------------------------------------

import arcpy

def fields_to_table(input_data, fields, workspace, output_table):
    '''function creates field mappings object then uses the table to tables
    conversion tool to export a table to your gdb from your FC fields
    :param input_data: your feature class in your geodatabase
    :param fields: a list of your field names (string)
    :param workspace: your arcpy.env.workspace
    :output_table: the name of your output table'''

    #create empty field mapping object
    fms = arcpy.FieldMappings()

    #define fieldmaps and add to field mapping objects (fms)
    for field in fields:
        fm = arcpy.FieldMap()
        fm.addInputField(input_data, field)
        output_field = fm.outputField
        output_field.name = field
        fm.outputField = output_field

        # add the field map to the field mappings object
        fms.addFieldMap(fm)

    #print field map object
    print(fms)

    #run table to table conversion tool with field mappings parameter
    arcpy.TableToTable_conversion(input_data, workspace, output_table, "", fms)
    print("converted %s to table" %(input_data))


if __name__ == '__main__':

    #Set params here!
    arcpy.env.workspace = None #REQUIRED: path param to your geodatabase e.g., r"C:\Users\username\Desktop\databasename.gdb"

    input_data = None #REQUIRED: string param of the name of your dataset e.g., "fire_stations"

    output_table = None #REQUIRED: string name of your output table, e.g., "fire_table"

    table_fields = None #REQUIRED: #List of the Field names you want to export to table e.g,  ['Status', 'Council']

    #run table to table conversion
    fields_to_table(input_data, table_fields, arcpy.env.workspace, output_table)
