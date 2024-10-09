# In[1]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Step 1: Get grid level 'fractional contribution source' from each type of fossil fuels. 
#   Here is the source: https://zenodo.org/records/4739100
#   Sources included: Coal and Other (oil & gas)


# Step 2: Get grid level 'air pollution exposure estimates' i.e. current concentration levels.
#   Here is the source: https://ghdx.healthdata.org/record/ihme-data/gbd-2021-air-pollution-exposure-estimates-1990-2021
#   Use PM2.5 mean values
#   Note: data is given in .tif format (IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19)
#           using QGIC software, convert .tif file to a .csv with Long/Lat and grid values.


# Step 3: Get grid level 'population estimates' i.e. current concentration levels.
#   Here is the source: https://human-settlement.emergency.copernicus.eu/download.php?ds=pop
#   Product: GHS-POP, epoch: 2020, resolution: 30 arcsec, coordinate system: WGS84
#           using QGIC software, convert .tif file to a .csv with Long/Lat and grid values.
   




# In[2]:
# load packages

import polars as pl
import numpy as np
import pandas as pd
import os





# In[3]:
# directory

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory





# In[3]: LOAD AND EDIT ALL DATASETS
#####################################################


# --------------
# LOAD CURRENT CONCENTRATION LEVELS DATA
df_concentration_baseline = pl.read_csv('999 - Data for Rudy - Global/concentration levels - germany - TEST.csv')

# remove extreme values that represent 'no data'
df_concentration_baseline = df_concentration_baseline.filter(pl.col('concentration') > 0)

# this data is already given in 0.1 increment for 2 decimal level Lon/Lat starting at 0.05 level
# i.e. 0.05, 0.15, 0.25 etc.
# rounding in case there are more digits in come numbers
df_concentration_baseline = df_concentration_baseline.with_columns([
    ((pl.col("Lon").round(2))),
    ((pl.col("Lat").round(2)))
])

# enfortcing the formatof 0.05 + 0.1 start and increments
df_concentration_baseline = df_concentration_baseline.with_columns([
    ((pl.col("Lon") - 0.05) / 0.1).round(0) * 0.1 + 0.05,
    ((pl.col("Lat") - 0.05) / 0.1).round(0) * 0.1 + 0.05
])

# print
print(df_concentration_baseline.head(10))

# ┌──────┬───────┬───────────────┐
# │ Lon  ┆ Lat   ┆ concentration │
# │ ---  ┆ ---   ┆ ---           │
# │ f64  ┆ f64   ┆ f64           │
# ╞══════╪═══════╪═══════════════╡
# │ 8.35 ┆ 54.95 ┆ 9.298724      │
# │ 8.45 ┆ 54.95 ┆ 6.043303      │
# │ 8.55 ┆ 54.95 ┆ 6.07165       │
# │ 8.65 ┆ 54.95 ┆ 8.33053       │
# │ 8.75 ┆ 54.95 ┆ 8.571401      │
# │ 8.85 ┆ 54.95 ┆ 9.111351      │
# │ 8.95 ┆ 54.95 ┆ 8.908991      │
# │ 9.05 ┆ 54.95 ┆ 8.451098      │
# │ 9.15 ┆ 54.95 ┆ 8.5695858     │
# │ 9.25 ┆ 54.95 ┆ 8.787505      │
# └──────┴───────┴───────────────┘










# --------------
# LOAD FRACTIONAL CONTRIBUTION DATA
df_frac_contribution = pl.read_csv('999 - Data for Rudy - Global/fractional contribution - germany - TEST.csv')

# convert to 2 digit decimal lat/lon for 'fractional contribution' dataframe to match 'concentration' dataframe
df_frac_contribution = df_frac_contribution.with_columns([
    ((pl.col("Lon").round(2))),
    ((pl.col("Lat").round(2)))
])

# enforce the format as above
df_frac_contribution = df_frac_contribution.with_columns([
    ((pl.col("Lon") - 0.05) / 0.1).round(0) * 0.1 + 0.05,
    ((pl.col("Lat") - 0.05) / 0.1).round(0) * 0.1 + 0.05
])

# group across all locations within same 2 decimal grids & Print
df_frac_contribution = df_frac_contribution.group_by("Lon", "Lat").agg(pl.col("ENEcoal", "ENEother").mean())
print(df_frac_contribution.head(10))

# ┌───────┬───────┬──────────┬──────────┐
# │ Lon   ┆ Lat   ┆ ENEcoal  ┆ ENEother │
# │ ---   ┆ ---   ┆ ---      ┆ ---      │
# │ f64   ┆ f64   ┆ f64      ┆ f64      │
# ╞═══════╪═══════╪══════════╪══════════╡
# │ 7.95  ┆ 49.55 ┆ 0.04079  ┆ 0.06748  │
# │ 11.75 ┆ 47.65 ┆ 0.04477  ┆ 0.06812  │
# │ 10.95 ┆ 50.55 ┆ 0.054479 ┆ 0.062097 │
# │ 13.45 ┆ 51.55 ┆ 0.060478 ┆ 0.076503 │
# │ 13.25 ┆ 52.55 ┆ 0.051123 ┆ 0.062241 │
# │ 9.85  ┆ 52.85 ┆ 0.0436   ┆ 0.07414  │
# │ 14.55 ┆ 51.85 ┆ 0.07061  ┆ 0.073282 │
# │ 10.05 ┆ 52.35 ┆ 0.05008  ┆ 0.06668  │
# │ 13.05 ┆ 52.45 ┆ 0.052366 ┆ 0.070073 │
# │ 13.15 ┆ 50.75 ┆ 0.0733   ┆ 0.07906  │
# └───────┴───────┴──────────┴──────────┘










# --------------
# LOAD POPULATION DATA
df_population = pl.read_csv('999 - Data for Rudy - Global/population.csv')

# convert to 2 digit decimal lat/lon for 'fractional contribution' dataframe to match 'concentration' dataframe
df_population = df_population.with_columns([
    ((pl.col("Lon").round(2))),
    ((pl.col("Lat").round(2)))
])

# enforce the format as above
df_population = df_population.with_columns([
    ((pl.col("Lon") - 0.05) / 0.1).round(0) * 0.1 + 0.05,
    ((pl.col("Lat") - 0.05) / 0.1).round(0) * 0.1 + 0.05
])

# sum all populations across same grids
df_population = df_population.group_by("Lon", "Lat").agg(pl.col("population").sum())

# print
print(df_population.select(pl.col('population').sum()))
print(df_population.head(10))

# ┌────────────┐
# │ population │
# │ ---        │
# │ f64        │
# ╞════════════╡
# │ 3.2584e8   │
# └────────────┘

# ┌───────┬───────┬──────────────┐
# │ Lon   ┆ Lat   ┆ population   │
# │ ---   ┆ ---   ┆ ---          │
# │ f64   ┆ f64   ┆ f64          │
# ╞═══════╪═══════╪══════════════╡
# │ 6.65  ┆ 47.75 ┆ 6218.58528   │
# │ 2.45  ┆ 43.85 ┆ 1513.027889  │
# │ 1.65  ┆ 58.35 ┆ 0.0          │
# │ 12.35 ┆ 58.65 ┆ 872.763997   │
# │ 14.05 ┆ 51.05 ┆ 8300.746306  │
# │ 7.85  ┆ 57.15 ┆ 0.0          │
# │ 4.35  ┆ 48.95 ┆ 52806.88896  │
# │ 9.95  ┆ 39.65 ┆ 0.0          │
# │ 4.55  ┆ 53.95 ┆ 0.0          │
# │ 9.65  ┆ 50.55 ┆ 70686.047904 │
# └───────┴───────┴──────────────┘










# --------------
# MERGE THESE DATAFRAMES
df_overall = df_concentration_baseline.join(
    df_frac_contribution, on=['Lat', 'Lon'], how = "left")

df_overall = df_overall.join(
    df_population, on=['Lat', 'Lon'], how = "left")

# print
print(df_overall.select(pl.col('population').sum()))
print(df_overall.head(10))

# ┌────────────┐
# │ population │
# │ ---        │
# │ f64        │
# ╞════════════╡
# │ 1.2211e8   │
# └────────────┘

# ┌──────┬───────┬───────────────┬─────────┬──────────┬──────────────┐
# │ Lon  ┆ Lat   ┆ concentration ┆ ENEcoal ┆ ENEother ┆ population   │
# │ ---  ┆ ---   ┆ ---           ┆ ---     ┆ ---      ┆ ---          │
# │ f64  ┆ f64   ┆ f64           ┆ f64     ┆ f64      ┆ f64          │
# ╞══════╪═══════╪═══════════════╪═════════╪══════════╪══════════════╡
# │ 8.35 ┆ 54.95 ┆ 9.298724      ┆ null    ┆ null     ┆ 13811.634194 │
# │ 8.45 ┆ 54.95 ┆ 6.043303      ┆ null    ┆ null     ┆ 0.0          │
# │ 8.55 ┆ 54.95 ┆ 6.07165       ┆ 0.03282 ┆ 0.06904  ┆ 0.0          │
# │ 8.65 ┆ 54.95 ┆ 8.33053       ┆ 0.03282 ┆ 0.06904  ┆ 1554.186642  │
# │ 8.75 ┆ 54.95 ┆ 8.571401      ┆ 0.03282 ┆ 0.06904  ┆ 859.639075   │
# │ 8.85 ┆ 54.95 ┆ 9.111351      ┆ 0.03282 ┆ 0.06904  ┆ 9183.960452  │
# │ 8.95 ┆ 54.95 ┆ 8.908991      ┆ 0.03282 ┆ 0.06904  ┆ 1581.540223  │
# │ 9.05 ┆ 54.95 ┆ 8.451098      ┆ null    ┆ null     ┆ 2270.779026  │
# │ 9.15 ┆ 54.95 ┆ 8.5695858     ┆ null    ┆ null     ┆ 1260.756223  │
# │ 9.25 ┆ 54.95 ┆ 8.787505      ┆ null    ┆ null     ┆ 3845.95761   │
# └──────┴───────┴───────────────┴─────────┴──────────┴──────────────┘





# --------------
# delete --- optional
# del df_population, df_frac_contribution, df_concentration_baseline










# In[4]: NOW LOAD EMISSIONS DATA AND GET PHASE OUT PACE
#######################################################

# --------------
# LOAD EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power_reduction = pl.read_csv('999 - Data for Rudy - Global/emissions vs base year - current policy -  power.csv')
df_nz_power_reduction = pl.read_csv('999 - Data for Rudy - Global/emissions vs base year - netzero 1.5C 50% adjsuted -  power.csv')


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
df_concentration_nz_coal_power = df_overall.clone()
df_concentration_nz_oilgas_power = df_overall.clone()
df_concentration_nz_total = df_overall.clone()


# get reduction shares
for year in year_columns:
    
    # Create the new column names for different types
    year_column_name = f'NZ_{year}'

    # Get the reduction values for Coal and Oil & Gas for the given year
    coal_reduction = df_nz_power_reduction.filter(pl.col('fuel_type') == 'Coal').select(pl.col(year)).item(0, 0)
    oilgas_reduction = df_nz_power_reduction.filter(pl.col('fuel_type') == 'O&G').select(pl.col(year)).item(0, 0)

    # Calculate and add new column for coal power reduction
    df_concentration_nz_coal_power = df_concentration_nz_coal_power.with_columns([
        (pl.col('concentration') - (pl.col('concentration') * pl.col('ENEcoal') * coal_reduction)).alias(year_column_name)
    ])
    
    # Calculate and add new column for oil & gas power reduction
    df_concentration_nz_oilgas_power = df_concentration_nz_oilgas_power.with_columns([
        (pl.col('concentration') - (pl.col('concentration') * pl.col('ENEother') * oilgas_reduction)).alias(year_column_name)
    ])

    # Calculate total reduction for both Coal and Oil & Gas and add the column
    df_concentration_nz_total = df_concentration_nz_total.with_columns([
        (pl.col('concentration') - (
            pl.col('concentration') * (
                pl.col('ENEcoal') * coal_reduction + 
                pl.col('ENEother') * oilgas_reduction
            )
        )).alias(year_column_name)
    ])


# delete
del year_column_name, year
del coal_reduction, oilgas_reduction










# --------------
# 2 - CP
# create dataframes with reduction for each fuel type individually
df_concentration_cp_coal_power = df_overall.clone()
df_concentration_cp_oilgas_power = df_overall.clone()
df_concentration_cp_total = df_overall.clone()


# get reduction shares
for year in year_columns:
    
    year_column_name = f'CP_{year}'

    # Get the reduction values for Coal and Oil & Gas for the given year
    coal_reduction = df_nz_power_reduction.filter(pl.col('fuel_type') == 'Coal').select(pl.col(year)).item(0, 0)
    oilgas_reduction = df_nz_power_reduction.filter(pl.col('fuel_type') == 'O&G').select(pl.col(year)).item(0, 0)

    # Calculate and add the new column for coal power reduction
    df_concentration_cp_coal_power = df_concentration_cp_coal_power.with_columns([
        (pl.col('concentration') - (pl.col('concentration') * pl.col('ENEcoal') * coal_reduction)).alias(year_column_name)
    ])
    
    # Calculate and add the new column for oil & gas power reduction
    df_concentration_cp_oilgas_power = df_concentration_cp_oilgas_power.with_columns([
        (pl.col('concentration') - (pl.col('concentration') * pl.col('ENEother') * oilgas_reduction)).alias(year_column_name)
    ])

    # Calculate total reduction for both Coal and Oil & Gas, then add the new column
    df_concentration_cp_total = df_concentration_cp_total.with_columns([
        (pl.col('concentration') - (
            pl.col('concentration') * (
                pl.col('ENEcoal') * coal_reduction + 
                pl.col('ENEother') * oilgas_reduction
            )
        )).alias(year_column_name)
    ])


# delete
del year_column_name, year
del coal_reduction, oilgas_reduction










# In[4]: GET OVERALL BASED ON POPULATION WEIGHTS
################################################


# find population-weights
var_total_population = df_overall.select(pl.col('population').sum()).item(0, 0)


# --------------
# NZ

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_nz_coal_power.clone()
temp_power_oilgas = df_concentration_nz_oilgas_power.clone()
temp_total = df_concentration_nz_total.clone()


# concentration X population in that grid    /   total population
for year in year_columns_nz:
    temp_power_coal = temp_power_coal.with_columns([
        (pl.col(year) * pl.col('population') / var_total_population).alias(year)])
    
    temp_power_oilgas = temp_power_oilgas.with_columns([
        (pl.col(year) * pl.col('population') / var_total_population).alias(year)])
    
    temp_total = temp_total.with_columns([
        (pl.col(year) * pl.col('population') / var_total_population).alias(year)])



# Sum across all grid cells for each year
temp_power_coal_sum = temp_power_coal.select([pl.col(year).sum().alias(year) for year in year_columns_nz])
temp_power_oilgas_sum = temp_power_oilgas.select([pl.col(year).sum().alias(year) for year in year_columns_nz])
temp_total_sum = temp_total.select([pl.col(year).sum().alias(year) for year in year_columns_nz])


# Extract the sum values for each year as a list
temp_power_coal_sum_list = temp_power_coal_sum.row(0)
temp_power_oilgas_sum_list = temp_power_oilgas_sum.row(0)
temp_total_sum_list = temp_total_sum.row(0)


# Convert the summed results into a single Polars DataFrame
df_concentration_nz_annual = pl.DataFrame({
    'Year': year_columns_nz,
    'power_coal': temp_power_coal_sum_list,
    'power_oilgas': temp_power_oilgas_sum_list,
    'total_fossil': temp_total_sum_list})


# Remove 'NZ_' prefix from the 'Year' column
df_concentration_nz_annual = df_concentration_nz_annual.with_columns([
    pl.col('Year').str.replace('NZ_', '')
])





# --------------
# CP

# concentration X population in that grid    /   total population
# first create temp files
temp_power_coal = df_concentration_cp_coal_power.clone()
temp_power_oilgas = df_concentration_cp_oilgas_power.clone()
temp_total = df_concentration_cp_total.clone()


# concentration X population in that grid / total population
for year in year_columns_cp:
    temp_power_coal = temp_power_coal.with_columns([
        (pl.col(year) * pl.col('population') / var_total_population).alias(year)])
    
    temp_power_oilgas = temp_power_oilgas.with_columns([
        (pl.col(year) * pl.col('population') / var_total_population).alias(year)])

    temp_total = temp_total.with_columns([
        (pl.col(year) * pl.col('population') / var_total_population).alias(year)])


# Sum across all grid cells for each year
temp_power_coal_sum = temp_power_coal.select([pl.col(year).sum().alias(year) for year in year_columns_cp])
temp_power_oilgas_sum = temp_power_oilgas.select([pl.col(year).sum().alias(year) for year in year_columns_cp])
temp_total_sum = temp_total.select([pl.col(year).sum().alias(year) for year in year_columns_cp])


# Extract the sum values for each year as a list
temp_power_coal_sum_list = temp_power_coal_sum.row(0)
temp_power_oilgas_sum_list = temp_power_oilgas_sum.row(0)
temp_total_sum_list = temp_total_sum.row(0)


# Convert the summed results into a single Polars DataFrame
df_concentration_cp_annual = pl.DataFrame({
    'Year': year_columns_cp,
    'power_coal': temp_power_coal_sum_list,
    'power_oilgas': temp_power_oilgas_sum_list,
    'total_fossil': temp_total_sum_list
})


# Remove 'CP_' prefix from the 'Year' column
df_concentration_cp_annual = df_concentration_cp_annual.with_columns([
    pl.col('Year').str.replace('CP_', '')
])











# delete
del year, var_total_population, year_columns_nz, year_columns_cp, 
del temp_power_coal, temp_power_oilgas, temp_total
del temp_power_coal_sum, temp_power_coal_sum_list, temp_power_oilgas_sum, temp_power_oilgas_sum_list
del temp_total_sum, temp_total_sum_list
del df_overall, df_nz_power_reduction, df_cp_power_reduction
del df_nz_power_reduction, df_cp_power_reduction




