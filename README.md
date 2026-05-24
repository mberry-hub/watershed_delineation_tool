# Watershed Delineation Tool

A Python/ArcPy geospatial analysis tool that automates watershed delineation using a digital elevation model (DEM) and a user-defined pour point.

## Features

- Fills sinks in a DEM
- Generates flow direction raster
- Generates flow accumulation raster
- Snaps pour points to highest flow accumulation cells
- Delineates watershed boundaries
- Converts watershed raster to polygon
- Optionally clips additional input layers
- Optionally creates a watershed buffer

## Tools Used

- Python
- ArcPy
- ArcGIS Pro
- Spatial Analyst Extension

## Project Structure

```text
watershedtool/
├── src/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
