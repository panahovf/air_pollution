# In[1]:
# Date: Sep 2, 2024
# Project: Identify grid level fractional contribution
# Author: Farhad Panahov

# description: The data is given as following:
    # Lat and Lon data are given in separate .csv file
    # Fractional contribution factors are given separately for individual type of fossil fuels but without respective lat&lon locations

# Steps: Get grid level 'fractional contribution source' from each type of fossil fuels:
    # Here is the source: https://zenodo.org/records/4739100
    # Sources included: ENEcoal, ENEother, INDcoal, INDother
    # Definitions: ENEcoal - Energy Production (coal combustion only) - Includes electricity and heat production, fuel production and transformation, oil and gas fugitive/flaring, and fossil fuel fires:
        # ENEother - Energy Production (all non-coal combustion) - Includes electricity and heat production, fuel production and transformation, oil and gas fugitive/flaring, and fossil fuel fires
        # INDcoal - Industry (coal combustion only) - Includes Industrial combustion (iron and steel, non-ferrous metals, chemicals, pulp and paper, food and tobacco, non-metallic minerals, construction, transportation equipment, machinery, mining and quarrying, wood products, textile and leather, and other industry combustion) and non-combustion industrial processes and product use (cement production, lime production, other minerals, chemical industry, metal production, food, beverage, wood, pulp, and paper, and other non-combustion industrial emissions)
        # INDother - Industry (all non-coal combustion) - Includes Industrial combustion (iron and steel, non-ferrous metals, chemicals, pulp and paper, food and tobacco, non-metallic minerals, construction, transportation equipment, machinery, mining and quarrying, wood products, textile and leather, and other industry combustion) and non-combustion industrial processes and product use (cement production, lime production, other minerals, chemical industry, metal production, food, beverage, wood, pulp, and paper, and other non-combustion industrial emissions)
    # Usage:
        # ENEcoal for power related emissions from coal combustion, and ENEother for power from oil and gas
        # INDcoal for extration related emissions from coal, and INDother for oil and gas extraction emissions
    # Note: this data has been sampled for the time being for Poland as a case study
    # How: 
        # select indexes from LAT LON data that correspond to max/min lat and lon of Poland
        # save the indexes, and then load these indexes from individual fractional contribution files
        # and combine into a single dataframe




   





# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import json
import zipfile
import os
import geopandas as gpd
import fiona
from shapely.geometry import shape
from pyproj import Transformer









# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory





# --------------
# EXTRACT POLAND POPULATION DATA

# part to ZIP file
zip_file_path = r'1 - input\3 - population\BUILT-POP_PROJ_GLOBE_SSP_R2020.zip'

# Path to extract Poland's GDB files to
extract_path = r'1 - input\3 - population'

# Initialize ZipFile object and extract specific directory
with zipfile.ZipFile(zip_file_path, 'r') as z:
    for file_info in z.namelist():
        if 'EasternEurope/POL/POL_POPProject_2015_2100.gdb' in file_info:
            z.extract(file_info, extract_path)

# get the final folder path
gdb_path = r'1 - input\3 - population\Pop_builtup_projections_SSP2_2015_2100\EasternEurope\POL\POL_POPProject_2015_2100.gdb'

# List the layers in the geodatabase
layers = fiona.listlayers(gdb_path)
print(f"Layers in {gdb_path}: {layers}")




# Open the 'POP2015' layer and read the data
with fiona.open(gdb_path, layer='POP2015') as layer:
    for feature in layer:
        print(feature)  # Prints each feature in the POP2015 layer


with fiona.open(gdb_path, layer='POP2015') as layer:
    # This will print out the CRS information
    print(layer.crs)



source_crs = 'ESRI:54009'  # Replace XXXX with the actual EPSG code from your data
target_crs = 'EPSG:4326'  # WGS84 Lat/Long



# Transformer to convert from source CRS to WGS84 (lat/lon)
transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

with fiona.open(gdb_path, layer='POP2015') as layer:
    # Check the CRS of the data
    print(f"Source CRS: {layer.crs}")

    for feature in layer:
        # Extract geometry as a shapely object
        geom = shape(feature['geometry'])

        # If geometry type is Point, convert it directly
        if geom.geom_type == 'Point':
            x, y = geom.x, geom.y  # Extract the original coordinates
            lon, lat = transformer.transform(x, y)  # Convert to long/lat
            print(f"Original coordinates: {(x, y)}")
            print(f"Converted to Long/Lat: {(lon, lat)}")
        
        # If geometry type is Polygon or MultiPolygon, convert the whole geometry
        else:
            lon_lat_geom = shapely.ops.transform(lambda x, y: transformer.transform(x, y), geom)
            print(f"Original geometry: {geom}")
            print(f"Converted geometry to Long/Lat: {lon_lat_geom}")










