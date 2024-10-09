# In[1]:
# Date: Sep 26, 2024
# Project: Identify grid level details and get global PM2.5 concentration pathways into 2050
# Author: Farhad Panahov

# description:
    # Combine Fractional Contribution, PM2.5 Concentration Levels and Population data




# In[2]:
# load packages

import polars as pl
import numpy as np
import pandas as pd
import rasterio
import os
import geopandas as gpd
from shapely.geometry import Point




# In[3]:
# directory

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory





# In[3]: LOAD AND EDIT ALL DATASETS
#####################################################

df_frac_contribution = pd.read_csv('2 - output/script 1.1 - fractional distribution - global/1.1 - frac dist - global.csv')
df_concentration_baseline = pd.read_csv('2 - output/script 1.2 - concentration levels - global/1.2 - pm concentration - global.csv')
df_population = pd.read_csv('2 - output/script 1.3 - population - global/1.3 - population - global.csv')










# In[3]: LOAD AND EDIT ALL DATASETS
# --------------
# MERGE THESE DATAFRAMES
df_overall = df_frac_contribution.merge(
    df_concentration_baseline, on=['Lat', 'Lon'], how='inner')

df_overall = df_overall.merge(
    df_population, on=['Lat', 'Lon'], how = "inner")


# print
print(df_overall['population'].sum()/10**9)   # 7.8310574085569975
print(df_overall.head(10))

# Lon    Lat  concentration   ENEcoal  ENEother   population
# 0 -147.65  69.95       1.309791  0.003980  0.027600     0.048179
# 1 -147.55  69.95       1.325693  0.003957  0.027342     0.229934
# 2  -51.35  69.95       4.283387  0.003870  0.007530    60.003880
# 3   18.85  69.95       3.861251  0.017910  0.029760     3.445463
# 4   18.95  69.95       3.872199  0.017901  0.029811     0.922600
# 5   19.35  69.95       3.455966  0.017820  0.030270    32.136378
# 6   19.45  69.95       3.441440  0.017812  0.030321    15.760664
# 7   19.55  69.95       3.381841  0.017740  0.030780     1.164293
# 8   19.65  69.95       3.520132  0.017740  0.030780  1345.717414
# 9   19.75  69.95       3.399943  0.017740  0.030780     7.559993





# --------------
# delete --- to save memory
del df_population, df_frac_contribution, df_concentration_baseline




geometry = [Point(xy) for xy in zip(df_overall['Lon'], df_overall['Lat'])]
gdf_points = gpd.GeoDataFrame(df_overall, geometry=geometry, crs="EPSG:4326")

# Load the world boundaries dataset from GeoPandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Perform a spatial join to match each point to a country
gdf_with_country = gpd.sjoin(gdf_points, world, how="left", op='within')

# Now gdf_with_country contains a column with country names
print(gdf_with_country[['Lon', 'Lat', 'name']])  # 'name' column has the country name
gdf_with_country.loc[gdf_with_country['iso_a3'].notna(), 'population'].sum()
gdf_with_country['population'].sum()




# In[4]: NOW LOAD EMISSIONS DATA AND GET PHASE OUT PACE
#######################################################

# --------------
# LOAD EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power_reduction = pd.read_csv('999 - Data for Rudy - Global/emissions vs base year - current policy -  power.csv')
df_nz_power_reduction = pd.read_csv('999 - Data for Rudy - Global/emissions vs base year - netzero 1.5C 50% adjsuted -  power.csv')


# Identify the year columns
year_columns = [str(year) for year in range(2024, 2051)]
year_columns_nz = [f'NZ_{year}' for year in range(2024, 2051)]
year_columns_cp = [f'CP_{year}' for year in range(2024, 2051)]










# In[4]: NOW ADJUST CONCENTRATION LEVELS TO EMISSIONS PATHWAYS OVER TIME
########################################################################

# add emissions pathways to total dataframe


# --------------
# 1 - NZ
# create dataframes with reduction for each fuel type individually
df_concentration_nz_coal_power = df_overall.copy()
df_concentration_nz_oilgas_power = df_overall.copy()
df_concentration_nz_total = df_overall.copy()


# get reduction shares
for year in year_columns:
    
    # Create the new column names for different types
    year_column_name = f'NZ_{year}'

    # Get the reduction values for Coal and Oil & Gas for the given year
    coal_reduction = df_nz_power_reduction.loc[df_nz_power_reduction['fuel_type'] == 'Coal', year].values[0]
    oilgas_reduction = df_nz_power_reduction.loc[df_nz_power_reduction['fuel_type'] == 'O&G', year].values[0]

    # Calculate and add new column for coal power reduction
    df_concentration_nz_coal_power[year_column_name] = df_concentration_nz_coal_power['concentration'] - (
        df_concentration_nz_coal_power['concentration'] * df_concentration_nz_coal_power['ENEcoal'] * coal_reduction)
    
    # Calculate and add new column for oil & gas power reduction
    df_concentration_nz_oilgas_power[year_column_name] = df_concentration_nz_oilgas_power['concentration'] - (
        df_concentration_nz_oilgas_power['concentration'] * df_concentration_nz_oilgas_power['ENEother'] * oilgas_reduction)

    # Calculate total reduction for both Coal and Oil & Gas and add the column
    df_concentration_nz_total[year_column_name] = df_concentration_nz_total['concentration'] - (
        df_concentration_nz_total['concentration'] * (
            df_concentration_nz_total['ENEcoal'] * coal_reduction + 
            df_concentration_nz_total['ENEother'] * oilgas_reduction
        )
    )


# delete
del year_column_name, year
del coal_reduction, oilgas_reduction










# --------------
# 2 - CP
# create dataframes with reduction for each fuel type individually
df_concentration_cp_coal_power = df_overall.copy()
df_concentration_cp_oilgas_power = df_overall.copy()
df_concentration_cp_total = df_overall.copy()


# Iterate over the year columns
for year in year_columns:
    year_column_name = f'CP_{year}'

    # Get the reduction values for Coal and Oil & Gas for the given year
    coal_reduction = df_cp_power_reduction.loc[df_cp_power_reduction['fuel_type'] == 'Coal', year].values[0]
    oilgas_reduction = df_cp_power_reduction.loc[df_cp_power_reduction['fuel_type'] == 'O&G', year].values[0]

    # Calculate and add the new column for coal power reduction
    df_concentration_cp_coal_power[year_column_name] = df_concentration_cp_coal_power['concentration'] - (
        df_concentration_cp_coal_power['concentration'] * df_concentration_cp_coal_power['ENEcoal'] * coal_reduction)
    
    # Calculate and add the new column for oil & gas power reduction
    df_concentration_cp_oilgas_power[year_column_name] = df_concentration_cp_oilgas_power['concentration'] - (
        df_concentration_cp_oilgas_power['concentration'] * df_concentration_cp_oilgas_power['ENEother'] * oilgas_reduction)

    # Calculate total reduction for both Coal and Oil & Gas, then add the new column
    df_concentration_cp_total[year_column_name] = df_concentration_cp_total['concentration'] - (
        df_concentration_cp_total['concentration'] * (
            df_concentration_cp_total['ENEcoal'] * coal_reduction + 
            df_concentration_cp_total['ENEother'] * oilgas_reduction
        )
    )

# Clean up temporary variables
del year_column_name, year
del coal_reduction, oilgas_reduction










# In[4]: GET OVERALL BASED ON POPULATION WEIGHTS
################################################


# find population-weights
var_total_population = df_overall['population'].sum()
#7831057408.556997

# --------------
# NZ

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_nz_coal_power.copy()
temp_power_oilgas = df_concentration_nz_oilgas_power.copy()
temp_total = df_concentration_nz_total.copy()

temp_power_coal_notweighted = df_concentration_nz_coal_power.copy()
temp_power_oilgas_notweighted = df_concentration_nz_oilgas_power.copy()
temp_total_notweighted = df_concentration_nz_total.copy()


# concentration X population in that grid    /   total population
for year in year_columns_nz:
    temp_power_coal[year] = (temp_power_coal[year] * temp_power_coal['population']) / var_total_population
    temp_power_oilgas[year] = (temp_power_oilgas[year] * temp_power_oilgas['population']) / var_total_population
    temp_total[year] = (temp_total[year] * temp_total['population']) / var_total_population


# Sum across all grid cells for each year
temp_power_coal_sum = temp_power_coal[year_columns_nz].sum()
temp_power_oilgas_sum = temp_power_oilgas[year_columns_nz].sum()
temp_total_sum = temp_total[year_columns_nz].sum()

temp_power_coal_notweighted_sum = temp_power_coal_notweighted[year_columns_nz].mean()
temp_power_oilgas_notweighted_sum = temp_power_oilgas_notweighted[year_columns_nz].mean()
temp_total_notweighted_sum = temp_total_notweighted[year_columns_nz].mean()


# Extract the sum values for each year as a list
temp_power_coal_sum_list = temp_power_coal_sum.values.tolist()
temp_power_oilgas_sum_list = temp_power_oilgas_sum.values.tolist()
temp_total_sum_list = temp_total_sum.values.tolist()

temp_power_coal_notweighted_sum_list = temp_power_coal_notweighted_sum.values.tolist()
temp_power_oilgas_notweighted_sum_list = temp_power_oilgas_notweighted_sum.values.tolist()
temp_total_notweighted_sum_list = temp_total_notweighted_sum.values.tolist()


# Convert the summed results into a single Pandas DataFrame
df_concentration_nz_annual = pd.DataFrame({
    'Year': year_columns_nz,
    'power_coal': temp_power_coal_sum_list,
    'power_oilgas': temp_power_oilgas_sum_list,
    'total_fossil': temp_total_sum_list,
    'power_coal_nonweight': temp_power_coal_notweighted_sum_list,
    'power_oilgas_nonweight': temp_power_oilgas_notweighted_sum_list,
    'total_fossil_nonweight': temp_total_notweighted_sum_list
})


# Remove 'NZ_' prefix from the 'Year' column
df_concentration_nz_annual['Year'] = df_concentration_nz_annual['Year'].str.replace('NZ_', '')





# --------------
# CP

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_cp_coal_power.copy()
temp_power_oilgas = df_concentration_cp_oilgas_power.copy()
temp_total = df_concentration_cp_total.copy()

temp_power_coal_notweighted = df_concentration_cp_coal_power.copy()
temp_power_oilgas_notweighted = df_concentration_cp_oilgas_power.copy()
temp_total_notweighted = df_concentration_cp_total.copy()


# Calculate concentration × population / total population for each year
for year in year_columns_cp:
    temp_power_coal[year] = (temp_power_coal[year] * temp_power_coal['population']) / var_total_population
    temp_power_oilgas[year] = (temp_power_oilgas[year] * temp_power_oilgas['population']) / var_total_population
    temp_total[year] = (temp_total[year] * temp_total['population']) / var_total_population


# Sum across all grid cells for each year
temp_power_coal_sum = temp_power_coal[year_columns_cp].sum()
temp_power_oilgas_sum = temp_power_oilgas[year_columns_cp].sum()
temp_total_sum = temp_total[year_columns_cp].sum()

temp_power_coal_notweighted_sum = temp_power_coal_notweighted[year_columns_cp].mean()
temp_power_oilgas_notweighted_sum = temp_power_oilgas_notweighted[year_columns_cp].mean()
temp_total_notweighted_sum = temp_total_notweighted[year_columns_cp].mean()


# Extract the sum values for each year as a list
temp_power_coal_sum_list = temp_power_coal_sum.values.tolist()
temp_power_oilgas_sum_list = temp_power_oilgas_sum.values.tolist()
temp_total_sum_list = temp_total_sum.values.tolist()

temp_power_coal_notweighted_sum_list = temp_power_coal_notweighted_sum.values.tolist()
temp_power_oilgas_notweighted_sum_list = temp_power_oilgas_notweighted_sum.values.tolist()
temp_total_notweighted_sum_list = temp_total_notweighted_sum.values.tolist()


# Convert the summed results into a single Pandas DataFrame
df_concentration_cp_annual = pd.DataFrame({
    'Year': year_columns_cp,
    'power_coal': temp_power_coal_sum_list,
    'power_oilgas': temp_power_oilgas_sum_list,
    'total_fossil': temp_total_sum_list,
    'power_coal_nonweight': temp_power_coal_notweighted_sum_list,
    'power_oilgas_nonweight': temp_power_oilgas_notweighted_sum_list,
    'total_fossil_nonweight': temp_total_notweighted_sum_list
})

# Remove 'CP_' prefix from the 'Year' column
df_concentration_cp_annual['Year'] = df_concentration_cp_annual['Year'].str.replace('CP_', '')






# delete
del year, var_total_population, year_columns_nz, year_columns_cp, 
del temp_power_coal, temp_power_oilgas, temp_total
del temp_power_coal_sum, temp_power_coal_sum_list, temp_power_oilgas_sum, temp_power_oilgas_sum_list
del temp_total_sum, temp_total_sum_list
del df_overall, df_nz_power_reduction, df_cp_power_reduction
del temp_power_coal_notweighted, temp_power_coal_notweighted_sum, temp_power_coal_notweighted_sum_list
del temp_power_oilgas_notweighted, temp_power_oilgas_notweighted_sum, temp_power_oilgas_notweighted_sum_list
del temp_total_notweighted, temp_total_notweighted_sum, temp_total_notweighted_sum_list







# In[]

# export data

# --------------
# annual concentration levels
df_concentration_cp_annual.to_excel('2 - output/script 2.1 - air pollution concentration levels - by scenario - global/1.1 - annual concentration levels - current policy.xlsx', index = False)
df_concentration_nz_annual.to_excel('2 - output/script 2.1 - air pollution concentration levels - by scenario - global/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx', index = False)




