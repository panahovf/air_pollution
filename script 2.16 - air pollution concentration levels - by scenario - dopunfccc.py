# In[1]:
# Date: Oct 19, 2024
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

df_frac_contribution = pd.read_csv('2 - output/script 1.1.1 - fractional distribution - global - country specified/1.1 - frac dist - global - by country.csv')
df_frac_contribution['Lat'] = df_frac_contribution['Lat'].round(2)
df_frac_contribution['Lon'] = df_frac_contribution['Lon'].round(2)


df_concentration_baseline = pd.read_csv('2 - output/script 1.2 - concentration levels - global/1.2 - pm concentration - global.csv')
df_concentration_baseline['Lat'] = df_concentration_baseline['Lat'].round(2)
df_concentration_baseline['Lon'] = df_concentration_baseline['Lon'].round(2)


df_population = pd.read_csv('2 - output/script 1.3 - population - global/1.3 - population - global.csv')
df_population['Lat'] = df_population['Lat'].round(2)
df_population['Lon'] = df_population['Lon'].round(2)









# In[3]: FILTER FOR REGION --- EMDE
#####################################################

# Get list of EMDE countries

# load datasets
temp_directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\1 - input\Country Datasets'
df_country_developed = pd.read_excel(temp_directory + r'\UNFCCC classification.xlsx')
df_country_developed = df_country_developed[df_country_developed["classification"] == "All Developed"]

# get and combine lists
v_countrycodes_developed = list(df_country_developed['iso_3'].unique())

# delete
del temp_directory, df_country_developed


# Filter Fractional Contribution data
df_frac_contribution = df_frac_contribution[df_frac_contribution['GU_A3'].isin(v_countrycodes_developed)]






# In[3]: LOAD AND EDIT ALL DATASETS
# --------------
# MERGE THESE DATAFRAMES
df_overall = df_frac_contribution.merge(
    df_concentration_baseline, on=['Lat', 'Lon'], how='inner')

df_overall = df_overall.merge(
    df_population, on=['Lat', 'Lon'], how = "inner")


# print
print(df_overall['population'].sum()/10**9)   # 1.2960064085273795
# ChatGPT: roughly 1.36 billion people residing in developed countries


print(df_overall.head(10))

#       Lon    Lat   ENEcoal  ENEother GU_A3  concentration  population
# 0 -140.85  62.35  0.003720  0.010080   CAN       5.200466  128.949104
# 1 -140.85  62.45  0.003652  0.009920   CAN       4.344431    0.011026
# 2 -140.85  63.95  0.003020  0.008440   CAN       4.306307   22.060369
# 3 -140.85  64.05  0.002620  0.007288   CAN       4.240409    0.283743
# 4 -140.85  64.25  0.002520  0.007000   CAN       4.396662    1.842341
# 5 -140.85  64.35  0.002520  0.007000   CAN       4.451655    4.974515
# 6 -140.85  64.85  0.001940  0.005310   CAN       4.502975    0.953917
# 7 -140.75  64.05  0.002620  0.007288   CAN       4.254942    0.003901
# 8 -140.65  61.15  0.004090  0.009830   CAN       4.031073    7.046824
# 9 -140.65  61.35  0.004090  0.009830   CAN       4.036796    0.669814




# --------------
# delete --- to save memory
del df_population, df_frac_contribution, df_concentration_baseline










# In[4]: NOW LOAD EMISSIONS DATA AND GET PHASE OUT PACE
#######################################################

# --------------
# LOAD EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\9.1 - Current policy - Secondary - annual.xlsx')
df_nz_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')


# Filter for EMDE countries only
df_cp_power = df_cp_power[df_cp_power['Region'].isin(v_countrycodes_developed)]
df_nz_power = df_nz_power[df_nz_power['Region'].isin(v_countrycodes_developed)]


# Identify the year columns
year_columns = [str(year) for year in range(2024, 2051)]
year_columns_nz = [f'NZ_{year}' for year in range(2024, 2051)]
year_columns_cp = [f'CP_{year}' for year in range(2024, 2051)]






# In[4]: GET COAL AND OIL/GAS EMISSIONS
#######################################################

# --------------
# Get total for EMDE
df_cp_power = df_cp_power.groupby(['fuel_type'])[year_columns].sum().reset_index()
df_nz_power = df_nz_power.groupby(['fuel_type'])[year_columns].sum().reset_index()


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



# --------------
# Get CP vs NZ difference: (1-NZ)/Current levels
# i.e. emissions reduction under NZ as a share of current level
df_nz_power_reduction = df_nz_power.copy()
df_nz_power_reduction[year_columns] = 1 - df_nz_power[year_columns].div(df_nz_power['2024'], axis=0)


# Get CP vs NZ difference: (1-CP)/Current levels
# i.e. emissions reduction under CP as a share of current level
df_cp_power_reduction = df_cp_power.copy()
df_cp_power_reduction[year_columns] = 1 - df_cp_power[year_columns].div(df_cp_power['2024'], axis=0)


# delete
del df_cp_power, df_nz_power, temp











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
# 1296006408

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
df_concentration_cp_annual.to_excel('2 - output/script 2.1.4 - air pollition concentration levels - by scenario - dopunfccc/1.1 - annual concentration levels - current policy.xlsx', index = False)
df_concentration_nz_annual.to_excel('2 - output/script 2.1.4 - air pollition concentration levels - by scenario - dopunfccc/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx', index = False)




