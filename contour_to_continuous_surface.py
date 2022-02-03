# Import libraries
import arcpy
from arcpy import *


geodatabase= r"..\sample.gdb\\"
arcpy.env.workspace  = geodatabase
arcpy.env.overwriteOutput = True

#Assign the contours to a variables
project_contours= arcpy.ListFeatureClasses()

#Iterate over the contours... 
for project in project_contours:
    
    arcpy.env.workspace = geodatabase
    
    #...create the bounding box
    arcpy.management.MinimumBoundingGeometry(project, geodatabase+ "%s_Box"%(project), "CONVEX_HULL", "ALL", None, "NO_MBG_FIELDS")
    
    #...use the bounding box as a mask for the raster 
    arcpy.env.mask = geodatabase+ "%s_Box"%(project)
    raster= arcpy.sa.TopoToRaster(project, 10, "", 20, None, None, "ENFORCE_WITH_SINK", "CONTOUR", 40, None, 1, 0, 2.5, 100, None, None, None, None, None, None, None, None)
    raster.save(geodatabase+ "%s_raster"%(project))

#Assign all rasters to a variable and convert each one to a contour polygon
all_rasters= arcpy.ListRasters('*_rst',  arcpy.ListFeatureClasses())
for each_raster in each_raster:
    arcpy.sa.Contour(each_raster, geodatabase+ "%s_contour_polygon"%(each_raster), 1, 0, 1, "CONTOUR_POLYGON", None)

