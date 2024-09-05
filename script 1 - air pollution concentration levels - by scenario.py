# In[1]:
# Date: Sep 2, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Step 1: Get grid level 'fractional contribution source' from each type of fossil fuels. 
#   Here is the source: https://zenodo.org/records/4739100
#   Sources included: ENEcoal, ENEother, coal, oilgas
#   Note: this data has been sampled for the time being for Poland as a case study
#           based on max/min lat and long of Poland
#           for simplification, it is now in rectangular shape

# Step 2: Get grid level 'air pollution exposure estimates' i.e. current concentration levels.
#   Here is the source: https://ghdx.healthdata.org/record/ihme-data/gbd-2021-air-pollution-exposure-estimates-1990-2021
#   Use PM2.5 mean values
#   Note: data is given in .tif format (IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19)
#           using QGIC software, convert .tif file to a .csv with Long/Lat and grid values.
#           This data has been sampled for the time being for Poland as a case study same as above


   







# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory


# --------------
# LOAD FRACTIONAL CONTRIBUTION DATA

### (1)
# import pandas as pd
# import json
# indices = []
# index = 0
# # https://worldpopulationreview.com/countries/poland/location
# lat_min = 49
# lat_max = 54 + 50 / 60
# long_min = 14 + 7 / 60
# long_max = 24 + 9 / 60
# # Specify the file path
# file_path = "./GBD-MAPS_Gridded_Fractional_Contributions_LatLon.csv"
# # Define the chunk size (number of rows per chunk)
# chunk_size = 100_000
# # Iterate over the file in chunks
# chunk_num = 0
# for chunk in pd.read_csv(file_path, chunksize=chunk_size):
#     if chunk_num < 5000:
#         chunk_num += 1
#         continue
#     # Process each chunk here
#     # For example, print the first few rows of each chunk
#     filtered = chunk[(chunk.Lat >= lat_min) & (chunk.Lat <= lat_max) & (chunk.Lon >= long_min) & (chunk.Lon <= long_max)]
#     if len(filtered) > 0:
#         indices += list(filtered.index)
#     chunk_num += 1
#     print(chunk_num)
# with open("indices.json", "w") as f:
#     json.dump(indices, f)

### (2)
# import pandas as pd
# import json
# with open("indices.json") as f:
#     indices = json.load(f)
# length = len(indices)
# indices = set(indices)
# assert len(indices) == length
# file_path = "./GBD-MAPS_Gridded_Fractional_Contributions_COAL.csv"
# file_path = "GBD-MAPS_Gridded_Fractional_Contributions_LatLon.csv"
# file_path = "GBD-MAPS_Gridded_Fractional_Contributions_ENEcoal.csv"
# file_path = "GBD-MAPS_Gridded_Fractional_Contributions_ENEother.csv"
# file_path = "GBD-MAPS_Gridded_Fractional_Contributions_OILGAS.csv"
# chunk_size = 100_000
# chunk_num = 0
# dfs = []
# for chunk in pd.read_csv(file_path, chunksize=chunk_size):
#     if chunk_num < 5000:
#         chunk_num += 1
#         continue
#     filtered = chunk[chunk.index.isin(indices)]
#     if len(filtered) > 0:
#         dfs.append(filtered.copy())
#     chunk_num += 1
#     print(chunk_num)
# df = pd.concat(dfs, axis=0)
# df.to_csv(file_path + "_reduced.csv")

## (3)
# import pandas as pd
# files = [
#     "GBD-MAPS_Gridded_Fractional_Contributions_LatLon.csv",
#     "GBD-MAPS_Gridded_Fractional_Contributions_COAL.csv",
#     "GBD-MAPS_Gridded_Fractional_Contributions_ENEcoal.csv",
#     "GBD-MAPS_Gridded_Fractional_Contributions_ENEother.csv",
#     "GBD-MAPS_Gridded_Fractional_Contributions_OILGAS.csv",
# ]
# dfs = [pd.read_csv(fname + "_reduced.csv", index_col=0) for fname in files]
# df = pd.concat(dfs, axis=1)
# df.to_csv("combined.csv")

df_frac_contribution = pd.read_csv('1 - input/fractional source contribution.csv')





# --------------
# LOAD CURRENT CONCENTRATION LEVELS DATA

# here are the steps to converting from .TIF to .CSV
# in QGIC program:

### (1) this code here imports the .tif data and converts to .xyz format --- run lines in QGIS consoler line by line
# import subprocess
# input_tif = r'YOUR DIRECTORY/IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19.TIF'
# output_xyz = r'YOUR DIRECTORY/output.xyz'
# cmd = [
#     'gdal_translate', 
#     '-of', 'XYZ', 
#     input_tif, 
#     output_xyz
# ]
# subprocess.run(cmd)

### (2) Now import .XYZ file
# Add the XYZ File as a Layer:
# Go to Layer -> Add Layer -> Add Delimited Text Layer....
# Browse to the XYZ file you just created (e.g., output.xyz).
# In the dialog box:
# Set File Format to Custom delimiters, and ensure that only Space is checked.
# Set X Field to the first column (X coordinate).
# Set Y Field to the second column (Y coordinate).
# Set Z Field to the third column (Z value), if applicable.
# Ensure that the Geometry CRS matches the coordinate system used in your original raster (if you know it's in WGS 84, set this to EPSG:4326).
# Click Add.

### (3) now save as .CSV
# Step 1: Right-Click on the Layer
# Locate the Layer: In the Layers panel on the left side of the QGIS window, find the layer you want to export. This should be the layer that was either originally loaded as XYZ or reprojected to WGS 84 (EPSG:4326).
# Right-Click: Right-click on the layer name.
# Step 2: Select "Export" -> "Save Features As..."
# Export Option: From the right-click menu, select Export -> Save Features As....
# Step 3: Configure Export Settings
# Format: In the Format dropdown, select CSV.
# File Name: Click the ... button next to the File name field to choose a location and name for the CSV file you are about to create. Make sure to specify the .csv extension.
# CRS: Ensure that the CRS (Coordinate Reference System) is set to EPSG:4326 - WGS 84. This CRS is necessary to get latitude and longitude coordinates.
# Layer Options:
# Under Layer Options, you should see a setting for Geometry. Make sure this is set to AS_XY. This setting will export the coordinates as X (longitude) and Y (latitude) columns.

# You can specify the export values by applying an expression that filters the data:
# Open the Expression Dialog:
# In the Save Features As... dialog, you should see an option for Subset expression or Filter.
# Click the ... button next to this field to open the Expression Dialog.

df_concentration_baseline = pd.read_csv('1 - input/concentration levels.csv')





# --------------
# LOAD POLAND EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 67% adjusted 
df_poland_cp_power = pd.read_excel('C:/Users/panah/OneDrive/Desktop/Work/2 - RA - Climate fin/2 - output/script 5/1.1 - annual emissions - current policy.xlsx')
df_poland_nz_power = pd.read_excel('C:/Users/panah/OneDrive/Desktop/Work/2 - RA - Climate fin/2 - output/script 5/3.1 - annual emissions - netzero modified 15C 67%.xlsx')

df_poland_cp_extraction = pd.read_excel('C:/Users/panah/OneDrive/Desktop/Work/2 - RA - Climate fin/2 - output/script 5.2/1.1 - annual emissions - current policy.xlsx')
df_poland_nz_extraction = pd.read_excel('C:/Users/panah/OneDrive/Desktop/Work/2 - RA - Climate fin/2 - output/script 5.2/3.1 - annual emissions - netzero modified 15C 67%.xlsx')





# --------------
# POPULATION ESTIMATES BY GRID & FILTER RIGHT AWAY TO AVOID LARGE FILES
# https://human-settlement.emergency.copernicus.eu/download.php?ds=pop
# Product: GHS-POP, epoch: 2020, resolution: 30 arcsec, coordinate system: WGS84
df_population1 = pd.read_csv('1 - input/population1_r4_c20.csv')
df_population2 = pd.read_csv('1 - input/population2_r4_c21.csv')
df_population3 = pd.read_csv('1 - input/population3_r5_c20.csv')
df_population4 = pd.read_csv('1 - input/population4_r5_c21.csv')










# In[4]: COMBINE POPULATION NUMBERS
#####################################

# --------------
# filter
df_population1 = df_population1[
    (df_population1['field_1'] >= min(df_frac_contribution['Lon'])) & 
    (df_population1['field_1'] <= max(df_frac_contribution['Lon']))]
df_population1 = df_population1[
    (df_population1['field_2'] >= min(df_frac_contribution['Lat'])) & 
    (df_population1['field_2'] <= max(df_frac_contribution['Lat']))]


df_population2 = df_population2[
    (df_population2['field_1'] >= min(df_frac_contribution['Lon'])) & 
    (df_population2['field_1'] <= max(df_frac_contribution['Lon']))]
df_population2 = df_population2[
    (df_population2['field_2'] >= min(df_frac_contribution['Lat'])) & 
    (df_population2['field_2'] <= max(df_frac_contribution['Lat']))]


df_population3 = df_population3[
    (df_population3['field_1'] >= min(df_frac_contribution['Lon'])) & 
    (df_population3['field_1'] <= max(df_frac_contribution['Lon']))]
df_population3 = df_population3[
    (df_population3['field_2'] >= min(df_frac_contribution['Lat'])) & 
    (df_population3['field_2'] <= max(df_frac_contribution['Lat']))]


df_population4 = df_population3[
    (df_population4['field_1'] >= min(df_frac_contribution['Lon'])) & 
    (df_population4['field_1'] <= max(df_frac_contribution['Lon']))]
df_population4 = df_population3[
    (df_population4['field_2'] >= min(df_frac_contribution['Lat'])) & 
    (df_population4['field_2'] <= max(df_frac_contribution['Lat']))]



# --------------
# combine population files into single doc
df_population = pd.concat([df_population1, df_population2, df_population3, df_population4], ignore_index=True)


# --------------
# delete extras
del df_population1, df_population2, df_population3, df_population4










# In[4]: GET EMISSIONS REDUCTION SHARE UNDER NZ SCENARIO
#####################################

# --------------
# Combine Oil and Gas emissions for both power and extraction to match fraction contribution data: enecoal, eneother, coal, oilgas

# get years columns
year_columns = df_poland_cp_power.columns[df_poland_cp_power.columns.str.isnumeric()]

# CP power
temp = df_poland_cp_power[df_poland_cp_power['fuel_type'] == 'Oil'].copy()   # Copy one of the rows
temp['fuel_type'] = 'O&G'  # Change the 'type' column value to 'O&G'
temp[year_columns] = df_poland_cp_power[df_poland_cp_power['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()   #Add the values of 'oil' and 'gas' rows for the year columns
df_poland_cp_power = pd.concat([df_poland_cp_power, temp], ignore_index=True)   # Append the new row to the DataFrame
df_poland_cp_power = df_poland_cp_power[~df_poland_cp_power['fuel_type'].isin(['Oil', 'Gas'])]   # Remove the original 'oil' and 'gas' rows

# NZ power
temp = df_poland_nz_power[df_poland_nz_power['fuel_type'] == 'Oil'].copy()   # Copy one of the rows
temp['fuel_type'] = 'O&G'  # Change the 'type' column value to 'O&G'
temp[year_columns] = df_poland_nz_power[df_poland_nz_power['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()   #Add the values of 'oil' and 'gas' rows for the year columns
df_poland_nz_power = pd.concat([df_poland_nz_power, temp], ignore_index=True)   # Append the new row to the DataFrame
df_poland_nz_power = df_poland_nz_power[~df_poland_nz_power['fuel_type'].isin(['Oil', 'Gas'])]   # Remove the original 'oil' and 'gas' rows

# CP extraction
temp = df_poland_cp_extraction[df_poland_cp_extraction['fuel_type'] == 'Oil'].copy()   # Copy one of the rows
temp['fuel_type'] = 'O&G'  # Change the 'type' column value to 'O&G'
temp[year_columns] = df_poland_cp_extraction[df_poland_cp_extraction['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()   #Add the values of 'oil' and 'gas' rows for the year columns
df_poland_cp_extraction = pd.concat([df_poland_cp_extraction, temp], ignore_index=True)   # Append the new row to the DataFrame
df_poland_cp_extraction = df_poland_cp_extraction[~df_poland_cp_extraction['fuel_type'].isin(['Oil', 'Gas'])]   # Remove the original 'oil' and 'gas' rows

# NZ extraction
temp = df_poland_nz_extraction[df_poland_nz_extraction['fuel_type'] == 'Oil'].copy()   # Copy one of the rows
temp['fuel_type'] = 'O&G'  # Change the 'type' column value to 'O&G'
temp[year_columns] = df_poland_nz_extraction[df_poland_nz_extraction['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()   #Add the values of 'oil' and 'gas' rows for the year columns
df_poland_nz_extraction = pd.concat([df_poland_nz_extraction, temp], ignore_index=True)   # Append the new row to the DataFrame
df_poland_nz_extraction = df_poland_nz_extraction[~df_poland_nz_extraction['fuel_type'].isin(['Oil', 'Gas'])]   # Remove the original 'oil' and 'gas' rows

del temp


# --------------
# Get CP vs NZ difference: (1-NZ)/Current levels
# i.e. emissions reduction under NZ as a share of current level
df_poland_nz_power_reduction = df_poland_nz_power.copy()
df_poland_nz_power_reduction[year_columns] = 1 - df_poland_nz_power[year_columns].div(df_poland_nz_power['2024'], axis=0)

df_poland_nz_extraction_reduction = df_poland_nz_extraction.copy()
df_poland_nz_extraction_reduction[year_columns] = 1 - df_poland_nz_extraction[year_columns].div(df_poland_nz_extraction['2024'], axis=0)


# --------------
# Get CP vs NZ difference: (1-CP)/Current levels
# i.e. emissions reduction under CP as a share of current level
df_poland_cp_power_reduction = df_poland_cp_power.copy()
df_poland_cp_power_reduction[year_columns] = 1 - df_poland_cp_power[year_columns].div(df_poland_cp_power['2024'], axis=0)

df_poland_cp_extraction_reduction = df_poland_cp_extraction.copy()
df_poland_cp_extraction_reduction[year_columns] = 1 - df_poland_cp_extraction[year_columns].div(df_poland_cp_extraction['2024'], axis=0)










# In[4]: COMBINE FRACTION CONTRUBITIONS AND CONCENTRATION
#####################################

# --------------
# create 2 digit decimal for fractional dataframe to math concentration dataframe
# truncate in fraction due to number stucture
df_frac_contribution['lat2'] = np.trunc(df_frac_contribution['Lat']*100)/100
df_frac_contribution['lon2'] = np.trunc(df_frac_contribution['Lon']*100)/100

# round in concentration due to number structure
df_concentration_baseline['X'] = df_concentration_baseline['X'].round(2)
df_concentration_baseline['Y'] = df_concentration_baseline['Y'].round(2)


# filter fraction data to match concentration data
df_frac_contribution = df_frac_contribution[df_frac_contribution['lat2'].isin(df_concentration_baseline['Y'])]
df_frac_contribution = df_frac_contribution[df_frac_contribution['lon2'].isin(df_concentration_baseline['X'])]


# --------------
# merge these 2 dataframes
# NZ
df_concentration_nz = pd.merge(df_frac_contribution, df_concentration_baseline[['X', 'Y', 'field_3']],
                     left_on=['lat2', 'lon2'], right_on=['Y', 'X'], how='left')

df_concentration_nz = df_concentration_nz.drop(columns=['X', 'Y', 'Unnamed: 0', 'Lon', 'Lat'])
df_concentration_nz.rename(columns={'field_3': 'Current_level'}, inplace=True)


# CP
df_concentration_cp = pd.merge(df_frac_contribution, df_concentration_baseline[['X', 'Y', 'field_3']],
                     left_on=['lat2', 'lon2'], right_on=['Y', 'X'], how='left')

df_concentration_cp = df_concentration_cp.drop(columns=['X', 'Y', 'Unnamed: 0', 'Lon', 'Lat'])
df_concentration_cp.rename(columns={'field_3': 'Current_level'}, inplace=True)


# delete
del df_poland_cp_extraction, df_poland_cp_power, df_poland_nz_power, df_poland_nz_extraction










# In[4]: GET NET ZERO ADJUSTED AIR POLLUTION CONCENTRATION STATS
##################################

# iterate over each year to get concentration statistics

# --------------
# NZ
for year in year_columns:
    
    new_column_name = f'NZ_{year}'

    df_concentration_nz[new_column_name] = df_concentration_nz['Current_level'] - df_concentration_nz['Current_level'] * (
        df_concentration_nz['COAL'] * df_poland_nz_extraction_reduction[df_poland_nz_extraction_reduction['fuel_type'] == 'Coal'][year].values[0] + 
        df_concentration_nz['OILGAS'] * df_poland_nz_extraction_reduction[df_poland_nz_extraction_reduction['fuel_type'] == 'O&G'][year].values[0] + 
        df_concentration_nz['ENEcoal'] * df_poland_nz_power_reduction[df_poland_nz_power_reduction['fuel_type'] == 'Coal'][year].values[0] + 
        df_concentration_nz['ENEcoal'] * df_poland_nz_power_reduction[df_poland_nz_power_reduction['fuel_type'] == 'O&G'][year].values[0]
        )

del new_column_name, year

# remove extreme values that represent 'no data'
df_concentration_nz = df_concentration_nz[df_concentration_nz['Current_level'] > 0]
                                   

# --------------
# CP
for year in year_columns:
    
    new_column_name = f'CP_{year}'

    df_concentration_cp[new_column_name] = df_concentration_cp['Current_level'] - df_concentration_cp['Current_level'] * (
        df_concentration_cp['COAL'] * df_poland_cp_extraction_reduction[df_poland_cp_extraction_reduction['fuel_type'] == 'Coal'][year].values[0] + 
        df_concentration_cp['OILGAS'] * df_poland_cp_extraction_reduction[df_poland_cp_extraction_reduction['fuel_type'] == 'O&G'][year].values[0] + 
        df_concentration_cp['ENEcoal'] * df_poland_cp_power_reduction[df_poland_cp_power_reduction['fuel_type'] == 'Coal'][year].values[0] + 
        df_concentration_cp['ENEcoal'] * df_poland_cp_power_reduction[df_poland_cp_power_reduction['fuel_type'] == 'O&G'][year].values[0]
        )

del new_column_name, year

# remove extreme values that represent 'no data'
df_concentration_cp = df_concentration_cp[df_concentration_cp['Current_level'] > 0]
             









# In[4]: SYNCHORNIZE LAT LON VALUES FOR POPULATION AND AIRSTAT
#####################################

# --------------
# create 2 digit level lat lon
# set increments for rounding
increments_lon = np.arange(df_concentration_nz['lon2'].min(), df_concentration_nz['lon2'].max(), 0.10)  # Adjust the range as needed
increments_lat = np.arange(df_concentration_nz['lat2'].min(), df_concentration_nz['lat2'].max(), 0.10)  # Adjust the range as needed

# Function to map each value to the nearest increment
def map_to_nearest_increment_lon(value, increments_lon):
    return increments_lon[np.abs(increments_lon - value).argmin()].round(2)
def map_to_nearest_increment_lat(value, increments_lat):
    return increments_lat[np.abs(increments_lat - value).argmin()].round(2)

# apply rounding to the population data
df_population['lon2'] = df_population['field_1'].apply(lambda x: map_to_nearest_increment_lon(x, increments_lon))
df_population['lat2'] = df_population['field_2'].apply(lambda x: map_to_nearest_increment_lat(x, increments_lat))


# delete
del increments_lat, increments_lon


# group by lat log and sum population
df_population = df_population.groupby(['lon2', 'lat2'])['field_3'].sum().reset_index()
df_population.rename(columns={'field_3': 'population'}, inplace=True)









# In[4]: GET POPULATION WEIGHTED CONCENTRATION VALUES
########################################

# --------------
# keep only common pairs of lat long
df_concentration_nz_total = pd.merge(df_concentration_nz, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_cp_total = pd.merge(df_concentration_cp, df_population, on=['lat2', 'lon2'], how='inner')


# --------------
# find population-weights

# Identify the year columns
year_columns_nz = [f'NZ_{year}' for year in range(2024, 2051)]  # Adjust the range as necessary
year_columns_cp = [f'CP_{year}' for year in range(2024, 2051)]  # Adjust the range as necessary


# total population
var_total_population = df_concentration_nz_total['population'].sum()


# concentration X population in that grid    /   total population
for year in year_columns_nz:
    df_concentration_nz_total[year] = df_concentration_nz_total[year].multiply(df_concentration_nz_total['population'], axis=0).div(var_total_population)

for year in year_columns_cp:
    df_concentration_cp_total[year] = df_concentration_cp_total[year].multiply(df_concentration_cp_total['population'], axis=0).div(var_total_population)


# Calculate the sum for each column
df_concentration_nz_annual = df_concentration_nz_total[year_columns_nz].sum(axis=0)
df_concentration_nz_annual = df_concentration_nz_annual.reset_index()
df_concentration_nz_annual.columns = ['Year', 'Concentration_level']
df_concentration_nz_annual['Year'] = df_concentration_nz_annual['Year'].str.replace('NZ_', '')

df_concentration_cp_annual = df_concentration_cp_total[year_columns_cp].sum(axis=0)
df_concentration_cp_annual = df_concentration_cp_annual.reset_index()
df_concentration_cp_annual.columns = ['Year', 'Concentration_level']
df_concentration_cp_annual['Year'] = df_concentration_cp_annual['Year'].str.replace('CP_', '')


# delete
del year, var_total_population, year_columns_nz, year_columns_cp











# In[]

# export data

# --------------
# annual concentration levels
df_concentration_cp_annual.to_excel('2 - output/script 1.1/1.1 - annual concentration levels - current policy.xlsx', index = False)
df_concentration_nz_annual.to_excel('2 - output/script 1.1/1.2 - annual concentration levels - netzero 1.5C 67% adjsuted.xlsx', index = False)


