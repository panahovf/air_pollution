# In[1]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Step 1: Get grid level 'fractional contribution source' from each type of fossil fuels. 
#   Here is the source: https://zenodo.org/records/4739100
#   Sources included: Coal and Other (oil & gas)
#   Note: this data has been sampled for the time being for Poland as a case study
#           based on max/min lat and long of Poland
#           for simplification, it is now in rectangular shape

# Step 2: Get grid level 'air pollution exposure estimates' i.e. current concentration levels.
#   Here is the source: https://ghdx.healthdata.org/record/ihme-data/gbd-2021-air-pollution-exposure-estimates-1990-2021
#   Use PM2.5 mean values
#   Note: data is given in .tif format (IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19)
#           using QGIC software, convert .tif file to a .csv with Long/Lat and grid values.
#           This data has been sampled for the time being for Poland as a case study same as above

# Step 3: Get grid level 'population estimates' i.e. current concentration levels.
#   Here is the source: https://human-settlement.emergency.copernicus.eu/download.php?ds=pop
#   Product: GHS-POP, epoch: 2020, resolution: 30 arcsec, coordinate system: WGS84
#   Note: Get following squares: r4 c20, r4 c21, r5 c20, r5 c21
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
df_frac_contribution = pd.read_csv('1 - input/1 - fractional contribution/fractional contribution - usa.csv')



# --------------
# LOAD CURRENT CONCENTRATION LEVELS DATA
{
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

# CHECK the max / min coordinates for specified countries
# print(df_frac_contribution_deu['Lat'].max()) # 54.975
# print(df_frac_contribution_deu['Lat'].min()) # 47.315
# print(df_frac_contribution_deu['Lon'].max()) # 15.005
# print(df_frac_contribution_deu['Lon'].min()) # 5.995

# print(df_frac_contribution_idn['Lat'].max()) # 5.475
# print(df_frac_contribution_idn['Lat'].min()) # -10.355
# print(df_frac_contribution_idn['Lon'].max()) # 141.025
# print(df_frac_contribution_idn['Lon'].min()) # 95.295

# print(df_frac_contribution_ind['Lat'].max()) # 35.485
# print(df_frac_contribution_ind['Lat'].min()) # 7.975
# print(df_frac_contribution_ind['Lon'].max()) # 97.395
# print(df_frac_contribution_ind['Lon'].min()) # 68.185

# print(df_frac_contribution_tur['Lat'].max()) # 42.135
# print(df_frac_contribution_tur['Lat'].min()) # 35.835
# print(df_frac_contribution_tur['Lon'].max()) # 44.785
# print(df_frac_contribution_tur['Lon'].min()) # 26.045

# print(df_frac_contribution_usa['Lat'].max()) # 71.355
# print(df_frac_contribution_usa['Lat'].min()) # 18.925
# print(df_frac_contribution_usa['Lon'].max()) # -66.975
# print(df_frac_contribution_usa['Lon'].min()) # -171.785

# print(df_frac_contribution_vnm['Lat'].max()) # 23.345
# print(df_frac_contribution_vnm['Lat'].min()) # 8.605
# print(df_frac_contribution_vnm['Lon'].max()) # -109.335
# print(df_frac_contribution_vnm['Lon'].min()) # 102.175
}
df_concentration_baseline = pd.read_csv('1 - input/2 - concentration levels/concentration levels - usa.csv')





# --------------
# LOAD POLAND EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\9.1 - Current policy - Secondary - annual.xlsx')
df_nz_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')





















# In[4]: GET EMISSIONS REDUCTION SHARE UNDER NZ SCENARIO
#####################################

# --------------
# first get total emissions data for NZ adjusted scenarios
year_columns = [str(year) for year in range(2024, 2051)]


df_cp_power = df_cp_power.loc[df_cp_power['Region'] == "USA"]
df_nz_power = df_nz_power.loc[df_nz_power['Region'] == "USA"]





# --------------
# Combine Oil and Gas emissions for both power and extraction to match fraction contribution data

# CP power
temp = df_cp_power[df_cp_power['fuel_type'] == 'Oil'].copy()   # Copy one of the rows
temp['fuel_type'] = 'O&G'  # Change the 'type' column value to 'O&G'
temp[year_columns] = df_cp_power[df_cp_power['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()   #Add the values of 'oil' and 'gas' rows for the year columns
df_cp_power = pd.concat([df_cp_power, temp], ignore_index=True)   # Append the new row to the DataFrame
df_cp_power = df_cp_power[~df_cp_power['fuel_type'].isin(['Oil', 'Gas'])]   # Remove the original 'oil' and 'gas' rows

# NZ power
temp = df_nz_power[df_nz_power['fuel_type'] == 'Oil'].copy()   # Copy one of the rows
temp['fuel_type'] = 'O&G'  # Change the 'type' column value to 'O&G'
temp[year_columns] = df_nz_power[df_nz_power['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()   #Add the values of 'oil' and 'gas' rows for the year columns
df_nz_power = pd.concat([df_nz_power, temp], ignore_index=True)   # Append the new row to the DataFrame
df_nz_power = df_nz_power[~df_nz_power['fuel_type'].isin(['Oil', 'Gas'])]   # Remove the original 'oil' and 'gas' rows

del temp





# --------------
# Get CP vs NZ difference: (1-NZ)/Current levels
# i.e. emissions reduction under NZ as a share of current level
df_nz_power_reduction = df_nz_power.copy()
df_nz_power_reduction[year_columns] = 1 - df_nz_power[year_columns].div(df_nz_power['2024'], axis=0)


# --------------
# Get CP vs NZ difference: (1-CP)/Current levels
# i.e. emissions reduction under CP as a share of current level
df_cp_power_reduction = df_cp_power.copy()
df_cp_power_reduction[year_columns] = 1 - df_cp_power[year_columns].div(df_cp_power['2024'], axis=0)



# delete
del df_cp_power, df_nz_power










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

df_concentration_nz = df_concentration_nz.drop(columns=['X', 'Y', 'Lon', 'Lat'])
df_concentration_nz.rename(columns={'field_3': 'Current_level'}, inplace=True)


# CP
df_concentration_cp = pd.merge(df_frac_contribution, df_concentration_baseline[['X', 'Y', 'field_3']],
                     left_on=['lat2', 'lon2'], right_on=['Y', 'X'], how='left')

df_concentration_cp = df_concentration_cp.drop(columns=['X', 'Y', 'Lon', 'Lat'])
df_concentration_cp.rename(columns={'field_3': 'Current_level'}, inplace=True)


# MAX
df_concentration_max = pd.merge(df_frac_contribution, df_concentration_baseline[['X', 'Y', 'field_3']],
                     left_on=['lat2', 'lon2'], right_on=['Y', 'X'], how='left')

df_concentration_max = df_concentration_max.drop(columns=['X', 'Y',  'Lon', 'Lat'])
df_concentration_max.rename(columns={'field_3': 'Current_level'}, inplace=True)

# delete
del df_concentration_baseline, df_frac_contribution










# In[4]: GET NET ZERO ADJUSTED AIR POLLUTION CONCENTRATION STATS
##################################

# iterate over each year to get concentration statistics



# --------------
# NZ

# remove extreme values that represent 'no data'
df_concentration_nz = df_concentration_nz[df_concentration_nz['Current_level'] > 0]
                  

# create dataframes with reduction for each fuel type individually
df_concentration_nz_coal_power = df_concentration_nz.copy()
df_concentration_nz_oilgas_power = df_concentration_nz.copy()
df_concentration_nz_total = df_concentration_nz.copy()


# get reduction shares
for year in year_columns:
    
    new_column_name = f'NZ_{year}'

    df_concentration_nz_coal_power[new_column_name] = df_concentration_nz['Current_level'] - df_concentration_nz['Current_level'] * (
        df_concentration_nz['ENEcoal'] * df_nz_power_reduction[df_nz_power_reduction['fuel_type'] == 'Coal'][year].values[0]
        )
    
    df_concentration_nz_oilgas_power[new_column_name] = df_concentration_nz['Current_level'] - df_concentration_nz['Current_level'] * (
        df_concentration_nz['ENEother'] * df_nz_power_reduction[df_nz_power_reduction['fuel_type'] == 'O&G'][year].values[0]
        )
    
    # this is for total change in concentration across all fossil fuel types --- CHANGE "ENE" to a different type if needed
    df_concentration_nz_total[new_column_name] = df_concentration_nz['Current_level'] - df_concentration_nz['Current_level'] * (
        df_concentration_nz['ENEcoal'] * df_nz_power_reduction[df_nz_power_reduction['fuel_type'] == 'Coal'][year].values[0] + 
        df_concentration_nz['ENEother'] * df_nz_power_reduction[df_nz_power_reduction['fuel_type'] == 'O&G'][year].values[0]
        )

del new_column_name, year

                 



# --------------
# CP

# remove extreme values that represent 'no data'
df_concentration_cp = df_concentration_cp[df_concentration_cp['Current_level'] > 0]
             

# create dataframes with reduction for each fuel type individually
df_concentration_cp_coal_power = df_concentration_cp.copy()
df_concentration_cp_oilgas_power = df_concentration_cp.copy()
df_concentration_cp_total = df_concentration_cp.copy()


# get reduction shares
for year in year_columns:
    
    new_column_name = f'CP_{year}'

    df_concentration_cp_coal_power[new_column_name] = df_concentration_cp['Current_level'] - df_concentration_cp['Current_level'] * (
        df_concentration_cp['ENEcoal'] * df_cp_power_reduction[df_cp_power_reduction['fuel_type'] == 'Coal'][year].values[0]
        )
    
    df_concentration_cp_oilgas_power[new_column_name] = df_concentration_cp['Current_level'] - df_concentration_cp['Current_level'] * (
        df_concentration_cp['ENEother'] * df_cp_power_reduction[df_cp_power_reduction['fuel_type'] == 'O&G'][year].values[0]
        )
    
    # this is for total change in concentration across all fossil fuel types --- CHANGE "ENE" to a different type if needed
    df_concentration_cp_total[new_column_name] = df_concentration_cp['Current_level'] - df_concentration_cp['Current_level'] * (
        df_concentration_cp['ENEcoal'] * df_cp_power_reduction[df_cp_power_reduction['fuel_type'] == 'Coal'][year].values[0] + 
        df_concentration_cp['ENEother'] * df_cp_power_reduction[df_cp_power_reduction['fuel_type'] == 'O&G'][year].values[0] 
        )

del new_column_name, year





# --------------
# MAX

# remove extreme values that represent 'no data'
df_concentration_max = df_concentration_max[df_concentration_max['Current_level'] > 0]
             

# create dataframes with reduction for each fuel type individually
df_concentration_max_coal_power = df_concentration_max.copy()
df_concentration_max_oilgas_power = df_concentration_max.copy()
df_concentration_max_total = df_concentration_max.copy()


# get reduction shares
for year in year_columns:
    
    new_column_name = f'MX_{year}'

    df_concentration_max_coal_power[new_column_name] = df_concentration_max['Current_level'] * (1 - df_concentration_max['ENEcoal'])
    
    df_concentration_max_oilgas_power[new_column_name] = df_concentration_max['Current_level'] * (1 - df_concentration_max['ENEother'])
               
    # this is for total change in concentration across all fossil fuel types --- CHANGE "ENE" to a different type if needed
    df_concentration_max_total[new_column_name] = df_concentration_max['Current_level'] * (1 -  df_concentration_max['ENEcoal'] -   # coal power
                                                                                          df_concentration_max['ENEother']    # oilgas power
                                                                                          )

del new_column_name, year










# In[4]: SYNCHORNIZE LAT LON VALUES FOR POPULATION AND AIRSTAT
#####################################

# --------------
# create 2 digit level lat lon
# set increments for rounding
increments_lon = np.arange(df_concentration_nz_coal_power['lon2'].min(), df_concentration_nz_coal_power['lon2'].max(), 0.10)  # Adjust the range as needed
increments_lat = np.arange(df_concentration_nz_coal_power['lat2'].min(), df_concentration_nz_coal_power['lat2'].max(), 0.10)  # Adjust the range as needed

# Function to map each value to the nearest increment
def map_to_nearest_increment_lon(value, increments_lon):
    return increments_lon[np.abs(increments_lon - value).argmin()].round(2)
def map_to_nearest_increment_lat(value, increments_lat):
    return increments_lat[np.abs(increments_lat - value).argmin()].round(2)










# In[4]: NOW LOAD AND FILTER EACH POPULATION DATAFILE RIGHT AWAY
################################################################

# here as we load population data files, we filter them right by :
    # 1: rounding to 2 digit level with increments matching values from 'concentration data'
    # 2: grouping by --- that is summing population values across rounded grids

population_path = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution\1 - input\3 - population\5 - usa\output_excel'
population_files = os.listdir(population_path)


# create empty population file
df_population = pd.DataFrame()


# loop through each populatino file, filter right away and combine
for file in population_files:
    
    file_path = os.path.join(population_path, file)
    temp_df = pd.read_excel(file_path)
   
   # Apply mapping functions to columns
    temp_df['lon2'] = temp_df['X'].apply(lambda x: map_to_nearest_increment_lon(x, increments_lon))
    temp_df['lat2'] = temp_df['Y'].apply(lambda x: map_to_nearest_increment_lat(x, increments_lat))
    
    # group by grid (since now grid is aggregated to higher level --- larger area) & rename
    temp_df = temp_df.groupby(['lon2', 'lat2'])['Value'].sum().reset_index()
    temp_df.rename(columns={'Value': 'population'}, inplace=True)

    # Add the processed DataFrame to the cumulative DataFrame
    df_population = pd.concat([df_population, temp_df], ignore_index=True)
    
    # print progress
    print("Finished file " + file)


# delete
del increments_lat, increments_lon
del population_files, population_path, temp_df, file, file_path


# group by lat log and sum population --- in case lon lat were repetitive in different file batches
df_population = df_population.groupby(['lon2', 'lat2'])['population'].sum().reset_index()


# print
print(df_population['population'].sum())
# 461565175.4529414





# In[4]: GET POPULATION WEIGHTED CONCENTRATION VALUES
########################################

# --------------
# keep only common pairs of lat long
df_concentration_nz_coal_power = pd.merge(df_concentration_nz_coal_power, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_nz_oilgas_power = pd.merge(df_concentration_nz_oilgas_power, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_nz_total = pd.merge(df_concentration_nz_total, df_population, on=['lat2', 'lon2'], how='inner')

df_concentration_cp_coal_power = pd.merge(df_concentration_cp_coal_power, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_cp_oilgas_power = pd.merge(df_concentration_cp_oilgas_power, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_cp_total = pd.merge(df_concentration_cp_total, df_population, on=['lat2', 'lon2'], how='inner')

df_concentration_max_coal_power = pd.merge(df_concentration_max_coal_power, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_max_oilgas_power = pd.merge(df_concentration_max_oilgas_power, df_population, on=['lat2', 'lon2'], how='inner')
df_concentration_max_total = pd.merge(df_concentration_max_total, df_population, on=['lat2', 'lon2'], how='inner')

# check sum total of population
print(df_concentration_nz_coal_power['population'].sum())
# 332495104.18830895




# --------------
# find population-weights

# Identify the year columns
year_columns_nz = [f'NZ_{year}' for year in range(2024, 2051)]  # Adjust the range as necessary
year_columns_cp = [f'CP_{year}' for year in range(2024, 2051)]  # Adjust the range as necessary
year_columns_max = [f'MX_{year}' for year in range(2024, 2051)]  # Adjust the range as necessary


# total population
var_total_population = df_concentration_nz_coal_power['population'].sum()


# --------------
# NZ

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_nz_coal_power.copy()
temp_power_oilgas = df_concentration_nz_oilgas_power.copy()
temp_total = df_concentration_nz_total.copy()


# concentration X population in that grid    /   total population
for year in year_columns_nz:
    temp_power_coal[year] = temp_power_coal[year].multiply(temp_power_coal['population'], axis=0).div(var_total_population)
    temp_power_oilgas[year] = temp_power_oilgas[year].multiply(temp_power_oilgas['population'], axis=0).div(var_total_population)
    temp_total[year] = temp_total[year].multiply(temp_total['population'], axis=0).div(var_total_population)



# Sum across all grid cells and combine fuel types into single dataframe
temp_power_coal = temp_power_coal[year_columns_nz].sum(axis=0)
temp_power_oilgas = temp_power_oilgas[year_columns_nz].sum(axis=0)
temp_total = temp_total[year_columns_nz].sum(axis=0)

df_concentration_nz_annual = pd.DataFrame({
    'power_coal': temp_power_coal,
    'power_oilgas': temp_power_oilgas,
    'total_fossil': temp_total
})

df_concentration_nz_annual = df_concentration_nz_annual.reset_index()
df_concentration_nz_annual.rename(columns={'index': 'Year'}, inplace=True)
df_concentration_nz_annual['Year'] = df_concentration_nz_annual['Year'].str.replace('NZ_', '')





# --------------
# CP

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_cp_coal_power.copy()
temp_power_oilgas = df_concentration_cp_oilgas_power.copy()
temp_total = df_concentration_cp_total.copy()


# concentration X population in that grid    /   total population
for year in year_columns_cp:
    temp_power_coal[year] = temp_power_coal[year].multiply(temp_power_coal['population'], axis=0).div(var_total_population)
    temp_power_oilgas[year] = temp_power_oilgas[year].multiply(temp_power_oilgas['population'], axis=0).div(var_total_population)
    temp_total[year] = temp_total[year].multiply(temp_total['population'], axis=0).div(var_total_population)


# Sum across all grid cells and combine fuel types into single dataframe
temp_power_coal = temp_power_coal[year_columns_cp].sum(axis=0)
temp_power_oilgas = temp_power_oilgas[year_columns_cp].sum(axis=0)
temp_total = temp_total[year_columns_cp].sum(axis=0)

df_concentration_cp_annual = pd.DataFrame({
    'power_coal': temp_power_coal,
    'power_oilgas': temp_power_oilgas,
    'total_fossil': temp_total
})

df_concentration_cp_annual = df_concentration_cp_annual.reset_index()
df_concentration_cp_annual.rename(columns={'index': 'Year'}, inplace=True)
df_concentration_cp_annual['Year'] = df_concentration_cp_annual['Year'].str.replace('CP_', '')







# --------------
# MAX

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_max_coal_power.copy()
temp_power_oilgas = df_concentration_max_oilgas_power.copy()
temp_total = df_concentration_max_total.copy()


# concentration X population in that grid    /   total population
for year in year_columns_max:
    temp_power_coal[year] = temp_power_coal[year].multiply(temp_power_coal['population'], axis=0).div(var_total_population)
    temp_power_oilgas[year] = temp_power_oilgas[year].multiply(temp_power_oilgas['population'], axis=0).div(var_total_population)
    temp_total[year] = temp_total[year].multiply(temp_total['population'], axis=0).div(var_total_population)


# Sum across all grid cells and combine fuel types into single dataframe
temp_power_coal = temp_power_coal[year_columns_max].sum(axis=0)
temp_power_oilgas = temp_power_oilgas[year_columns_max].sum(axis=0)
temp_total = temp_total[year_columns_max].sum(axis=0)

df_concentration_max_annual = pd.DataFrame({
    'power_coal': temp_power_coal,
    'power_oilgas': temp_power_oilgas,
    'total_fossil': temp_total
})

df_concentration_max_annual = df_concentration_max_annual.reset_index()
df_concentration_max_annual.rename(columns={'index': 'Year'}, inplace=True)
df_concentration_max_annual['Year'] = df_concentration_max_annual['Year'].str.replace('MX_', '')





# delete
del year, var_total_population, year_columns_nz, year_columns_cp, year_columns_max
del temp_power_coal, temp_power_oilgas, temp_total










# In[]

# export data

# --------------
# annual concentration levels
df_concentration_cp_annual.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/1.1 - annual concentration levels - current policy.xlsx', index = False)
df_concentration_nz_annual.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx', index = False)
df_concentration_max_annual.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/1.3 - annual concentration levels - full shut down.xlsx', index = False)


# --------------
# annual concentration levels --- by fuel type --- CP
df_concentration_cp_coal_power.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/2.1 - annual concentration levels - current policy - coal - power.xlsx', index = False)
df_concentration_cp_oilgas_power.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/2.3 - annual concentration levels - current policy - oilgas - power.xlsx', index = False)
df_concentration_cp_total.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/2.5 - annual concentration levels - current policy - total fossil.xlsx', index = False)


# --------------
# annual concentration levels --- by fuel type --- NZ
df_concentration_nz_coal_power.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/3.1 - annual concentration levels - netzero 1.5C 50% adjsuted - coal - power.xlsx', index = False)
df_concentration_nz_oilgas_power.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/3.3 - annual concentration levels - netzero 1.5C 50% adjsuted - oilgas - power.xlsx', index = False)
df_concentration_nz_total.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/3.5 - annual concentration levels - netzero 1.5C 50% adjsuted - total fossil.xlsx', index = False)


# --------------
# annual concentration levels --- by fuel type --- MAX
df_concentration_max_coal_power.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/4.1 - annual concentration levels - full shut down - coal - power.xlsx', index = False)
df_concentration_max_oilgas_power.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/4.3 - annual concentration levels - full shut down - oilgas - power.xlsx', index = False)
df_concentration_max_total.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/4.5 - annual concentration levels - full shut down - total fossil.xlsx', index = False)


# --------------
# emissions changes by type
df_cp_power_reduction.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/5.1 - emissions vs base year - current policy -  power.xlsx', index = False)
df_nz_power_reduction.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/5.3 - emissions vs base year - netzero 1.5C 50% adjsuted -  power.xlsx', index = False)


# --------------
# population
df_population.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/6.1 - population - 2020 - unfiltered.xlsx', index = False)


# --------------
# grid level NZ
df_concentration_nz_total.to_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx', index = False)
