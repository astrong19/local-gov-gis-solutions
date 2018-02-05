#---------------------------------------------------------------------------------------------------------------
# Name:         data_driven_pages_arcmap.py
#
# Purpose:      automate report generation using arcpy mapping
#
# Notes:        Written to be used with ArcMap and Python 2.7
#               Requires arcpy
#               All params are specified under if __name__ == __main__:
#               This script is designed to run from the command line (e.g., python data_driven_ages_arcmap.py)
#
# Helpful Links:
# http://desktop.arcgis.com/en/arcmap/10.3/map/reports/exportreport.htm
#----------------------------------------------------------------------------------------------------------------

from arcpy import mapping

def define_parameters(mxd, data_frame, layer_name):
    '''function to identify the layer for generating reports
    :param mxd: path to a ArcMap Document
    :param data_frame: data frame name
    :param layer_name: name of the layer to be used in reports'''

    map_document = mapping.MapDocument(mxd)

    df = mapping.ListDataFrames(map_document, data_frame)[0]

    lyr = mapping.ListLayers(map_document, layer_name, df)[0]

    return lyr

if __name__ == '__main__':

    #specify custom params
    layer_name = None #layer name (string)
    data_frame = None #data frame name (string)
    mxd = None #path to ArcMap Doc (string)
    rlf = None #path to report layer file (.rlf) (string)
    pdf_output = None #path to output pdf location (string)
    title = None #Title of your report (string)

    #get lyr from define_parameters function
    lyr = define_parameters(mxd, data_frame, layer_name)

    #export report
    mapping.ExportReport(lyr, rlf, pdf_output, "ALL", title)
    print("report generated for %s" %(title))
