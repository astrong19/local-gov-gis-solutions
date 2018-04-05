#------------------------------------------------------------------------------------------------------------------------------
# Name:        gp_tool_buffer.py
#
# Purpose:     Example buffer tool that can be added to a ArcGIS toolbox or
#              published as a geoprocessing service to Portal
#
# Created:     2/8/18
#
# Helpful Docs:
# Creating tools with Python: http://pro.arcgis.com/en/pro-app/arcpy/geoprocessing_and_python/a-quick-tour-of-creating-tools-in-python.htm
# Authoring web tools from python scripts: https://pro.arcgis.com/en/pro-app/help/analysis/geoprocessing/share-analysis/authoring-web-tools-with-python-scripts.htm
# Documenting tools: https://pro.arcgis.com/en/pro-app/help/analysis/geoprocessing/share-analysis/create-a-geoprocessing-package.htm#OL_2428C92E604D4162A9FF2E78F5462054
#---------------------------------------------------------------------------------------------------------------------------------

import arcpy

def buffer_point(data, output, distance_unit):

    try:
        arcpy.Buffer_analysis(data, output, distance_unit)
        arcpy.AddMessage("Buffer Completed: {}".format(output))

    except:
        arcpy.AddError("Error buffering data")
        raise arcpy.ExecuteError

if __name__ == '__main__':

    #input point
    input_point = arcpy.GetParameterAsText(0)

    #output buffer (polygon)
    output_buff = arcpy.GetParameterAsText(1)

    #input distance (string)
    distance = arcpy.GetParameterAsText(2)

    #input units (string)
    unit = arcpy.GetParameterAsText(3)

    #create string
    distance_unit = "{} {}".format((str(distance)), (str(unit)))

    #run buffer
    buffer_point(input_point, output_buff, distance_unit)
