# GEG238 Final Project, Matt Berry

import arcpy
from arcpy.sa import *

# Allow outputs to overwrite
arcpy.env.overwriteOutput = True

# Check out Spatial Analyst
arcpy.CheckOutExtension("Spatial")

# Inputs as ARCGIS Parameters
input_dem = arcpy.GetParameterAsText(0)
input_pour_point = arcpy.GetParameterAsText(1)

# Buffer distance parameter
buffer_distance = arcpy.GetParameterAsText(2)

# Optional additional layers: roads, parcels, etc.
optional_layers = arcpy.GetParameterAsText(3)

# Output geodatabase
output_gdb = arcpy.GetParameterAsText(4)

# Set workspace
arcpy.env.workspace = output_gdb
arcpy.env.scratchWorkspace = output_gdb

# Create output names
filled_dem_output = output_gdb + r"\FilledDEM"
flow_dir_output = output_gdb + r"\FlowDir"
flow_accum_output = output_gdb + r"\FlowAccum"
snapped_pour_output = output_gdb + r"\SnappedPourPoint"
watershed_raster_output = output_gdb + r"\WatershedRaster"
watershed_polygon_output = output_gdb + r"\WatershedPolygon"
watershed_buffer_output = output_gdb + r"\WatershedBuffer"

# Step 1: Fill sinks in DEM
filled_dem = Fill(arcpy.Raster(input_dem))
filled_dem.save(filled_dem_output)

# Step 2: Create flow direction raster from filled DEM
flow_dir = FlowDirection(filled_dem)
flow_dir.save(flow_dir_output)

# Step 3: Create flow accumulation raster from flow direction
flow_accum = FlowAccumulation(flow_dir)
flow_accum.save(flow_accum_output)

# Step 4: Snap pour point to highest flow accumulation nearby
snapped_pour = SnapPourPoint(input_pour_point, flow_accum, 30)
snapped_pour.save(snapped_pour_output)

# Step 5: Create watershed raster
watershed = Watershed(flow_dir, snapped_pour)
watershed.save(watershed_raster_output)

# Step 6: Convert watershed raster to polygon
arcpy.RasterToPolygon_conversion(
    watershed_raster_output,
    watershed_polygon_output
)

# Step 7: Buffer watershed polygon using tool parameter
arcpy.Buffer_analysis(
    watershed_polygon_output,
    watershed_buffer_output,
    buffer_distance
)

# Step 8: Clip optional layers only if there are inputs
if optional_layers != "":
    layers = optional_layers.split(";")

    for layer in layers:
        layer_name = arcpy.Describe(layer).baseName
        clip_output = output_gdb + "\\" + layer_name + "_Clip"

        arcpy.analysis.PairwiseClip(
            layer,
            watershed_polygon_output,
            clip_output
        )

# Outputs to display on map once complete
arcpy.SetParameterAsText(5, watershed_polygon_output)
arcpy.SetParameterAsText(6, watershed_buffer_output)

arcpy.AddMessage("Watershed analysis complete.")

# Check Spatial Analyst back in
arcpy.CheckInExtension("Spatial")