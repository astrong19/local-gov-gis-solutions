#-------------------------------------------------------------------------------
# Name: 		export_csv.py
#
# Purpose: 		simple gp tool to export GIS data to a csv (works for point
#				shapefiles, feature classes and services). Designed to be
#				published as a web tool/ work with a gp WAB widget
#
# Created:		3/12/18
#
# Helpful docs:
# https://community.esri.com/thread/110894
#-------------------------------------------------------------------------------

import arcpy
import csv

def get_rows(data_set, fields):

	with arcpy.da.SearchCursor(data_set, fields) as cursor:
		for row in cursor:
			yield row

def write_to_csv(output, fieldnames, rows):

	with open(output,'w') as out_file:
		arcpy.AddMessage("writing to %s" %(output))
		out_writer = csv.writer(out_file)
		out_writer.writerow(fieldnames)
		for row in rows:
			arcpy.AddMessage("writing row {}".format(row))
			out_writer.writerow(row)

		arcpy.AddMessage("write to csv complete")

if __name__ == '__main__':

	data_set = arcpy.GetParameterAsText(0) #input data
	desc = arcpy.Describe(data_set) #describe data

	#make output dest optional
	output_defined = arcpy.GetParameterAsText(1)
	if output_defined:
		output = output_defined
	else:
		output = "{}.csv".format(desc.name.split('.')[0]) #output csv

	fieldnames = [f.name for f in desc.fields if f.type not in ["Geometry", "Raster", "Blob"]] #list fields
	rows = get_rows(data_set, fieldnames) #get rows

	write_to_csv(output, fieldnames, rows) #write to csv
