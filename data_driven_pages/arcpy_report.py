'''example sript of how to customize an automated report using arcpy mapping
based off: http://desktop.arcgis.com/en/arcmap/10.3/map/reports/exportreport.htm'''

import requests
from arcpy import mapping

def download_data(download_csv, output_csv):
    '''function to get csv from a download url and write to a local csv file
    :param download_csv: url to .csv endpoint
    :param output_csv: local path to a .csv file'''

    #get csv from download url
    r = requests.get(download_csv).content

    #write downloaded csv to local csv file
    with open(output_csv, 'wb') as mycsv:
        mycsv.write(r)

    print "CSV content written to {}".format(output_csv)

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
    download_csv = #http(s) url to a .csv file (string)
    output_csv = #path to a local .csv file (string)
    layer_name = #layer name (string)
    data_frame = #data frame name (string)
    mxd = #path to ArcMap Doc (string)
    rlf = #path to report layer file (.rlf) (string)
    pdf_output = #path to output pdf location (string)
    title = #Title of your report (string)

    lyr = define_parameters(mxd, data_frame, layer_name)

    #download csv file
    download_data(download_csv, output_csv)

    #export report
    mapping.ExportReport(lyr, rlf, pdf_output, "ALL", title)
    print "report generated for %s" %(title)
