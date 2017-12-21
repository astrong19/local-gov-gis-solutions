'''Solution to copy fields from a Feature Class to a Table
field mappings docs: http://pro.arcgis.com/en/pro-app/arcpy/classes/fieldmappings.htm'''

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

    #path to working environment
    arcpy.env.workspace = r"C:\Users\asa7362\Desktop\dev\tahoe_tables\test_table.gdb"

    #input tables
    input_data = "fire_stations"

    #output tables
    output_table = "fire_table"

    #List of the Field names you want to export to table
    table_fields = ['Status', 'Council']

    #run table to table conversion
    fields_to_table(input_data, table_fields, arcpy.env.workspace, output_table)
