'''example sript of how to customize an automated report using arcpy mapping'''

from arcpy import mapping

def define_parameters(mxd, data_frame, layer_name):

    map_document = mapping.MapDocument(mxd)

    df = mapping.ListDataFrames(map_document, data_frame)[0]

    lyr = mapping.ListLayers(map_document, layer_name, df)[0]

    return lyr

if __name__ == '__main__':

    #specify custom params
    layer_name = #layer name (string)
    data_frame = #data frame name (string)
    mxd = #path to ArcMap Doc (string)
    rlf = #path to report layer file (.rlf) (string)
    pdf_output = #path to output pdf location
    title = #Title of your report 

    lyr = define_parameters(mxd, data_frame, layer_name)

    #export report
    mapping.ExportReport(lyr, rlf, pdf_output, "ALL", title)
    print "report generated for %s" %(title)
