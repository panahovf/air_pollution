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
import rasterio
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
with rasterio.open('999 - Data for Rudy - Global/IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19.tif') as dataset:
    # Read the image data
    image_data = dataset.read(1)  # Reading the first band (1 for grayscale or multi-band data can be handled separately)

    # Get the coordinate transform from the dataset
    transform = dataset.transform

    # Create arrays for lon/lat
    rows, cols = np.indices(image_data.shape)
    lon, lat = rasterio.transform.xy(transform, rows, cols, offset='center')


# Flatten the arrays if needed
lon_flat = np.array(lon).flatten()
lat_flat = np.array(lat).flatten()
pixel_values = image_data.flatten()

# Create a Polars DataFrame with lon, lat, and pixel values
df_concentration_baseline = pl.DataFrame({
    'Lon': lon_flat,
    'Lat': lat_flat,
    'concentration': pixel_values
})


# delete
del cols, dataset, image_data, lat, lat_flat, lon, lon_flat, pixel_values, rows, transform


# remove extreme values that represent 'no data'
df_concentration_baseline = df_concentration_baseline.filter(pl.col('concentration') >= 0)


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

# ┌─────────┬───────┬───────────────┐
# │ Lon     ┆ Lat   ┆ concentration │
# │ ---     ┆ ---   ┆ ---           │
# │ f64     ┆ f64   ┆ f32           │
# ╞═════════╪═══════╪═══════════════╡
# │ -162.65 ┆ 69.95 ┆ 1.403364      │
# │ -162.55 ┆ 69.95 ┆ 1.403014      │
# │ -162.45 ┆ 69.95 ┆ 1.403001      │
# │ -162.35 ┆ 69.95 ┆ 1.403157      │
# │ -162.25 ┆ 69.95 ┆ 1.403211      │
# │ -162.15 ┆ 69.95 ┆ 1.403182      │
# │ -162.05 ┆ 69.95 ┆ 1.403155      │
# │ -161.95 ┆ 69.95 ┆ 1.403179      │
# │ -161.85 ┆ 69.95 ┆ 1.403131      │
# │ -161.75 ┆ 69.95 ┆ 1.403195      │
# └─────────┴───────┴───────────────┘










# --------------
# LOAD FRACTIONAL CONTRIBUTION DATA

# load data in chunks, apply edits to LON & LAT --- currently given with 3 decimal places
# this code strips away 3rd decimal place, and round values to 0.05 with 0.1 increment
# ie. 5.05 5.15 5.25 etc.

# Step 1: Lazily load the CSV file in chunks
df_frac_contribution = pl.scan_csv('999 - Data for Rudy - Global/fractional contribution - germany - TEST.csv')

# Step 2: Apply transformation to Lon and Lat (round to 2 decimals)
df_frac_contribution = df_frac_contribution.with_columns([
    (pl.col("Lon") * 100).floor() / 100,  # Scale up by 100, floor it, and then scale back down
    (pl.col("Lat") * 100).floor() / 100   # Same for Lat
])

# Step 3: Enforce the format for Lon/Lat columns (matching the original logic)
df_frac_contribution = df_frac_contribution.with_columns([
    ((pl.col("Lon") - 0.05) / 0.1).round(0) * 0.1 + 0.05,
    ((pl.col("Lat") - 0.05) / 0.1).round(0) * 0.1 + 0.05
])

# Step 4: Group by Lon/Lat and calculate mean of ENEcoal and ENEother
df_frac_contribution = df_frac_contribution.group_by("Lon", "Lat").agg(
    pl.col("ENEcoal", "ENEother").mean()
)

# Step 5: Collect the result into a DataFrame
df_frac_contribution = df_frac_contribution.collect()

# print
print(df_frac_contribution.head(10))

# ┌───────┬───────┬─────────┬──────────┐
# │ Lon   ┆ Lat   ┆ ENEcoal ┆ ENEother │
# │ ---   ┆ ---   ┆ ---     ┆ ---      │
# │ f64   ┆ f64   ┆ f64     ┆ f64      │
# ╞═══════╪═══════╪═════════╪══════════╡
# │ 9.25  ┆ 49.75 ┆ 0.04664 ┆ 0.06363  │
# │ 10.75 ┆ 50.55 ┆ 0.05449 ┆ 0.0622   │
# │ 9.45  ┆ 48.45 ┆ 0.03976 ┆ 0.05751  │
# │ 12.15 ┆ 53.75 ┆ 0.04456 ┆ 0.05489  │
# │ 13.45 ┆ 52.15 ┆ 0.05241 ┆ 0.07116  │
# │ 8.15  ┆ 52.15 ┆ 0.0454  ┆ 0.07465  │
# │ 8.75  ┆ 53.25 ┆ 0.03768 ┆ 0.07119  │
# │ 8.95  ┆ 50.05 ┆ 0.04961 ┆ 0.07227  │
# │ 9.85  ┆ 52.55 ┆ 0.0436  ┆ 0.07414  │
# │ 9.35  ┆ 47.65 ┆ 0.03351 ┆ 0.05016  │
# └───────┴───────┴─────────┴──────────┘










# --------------
# LOAD POPULATION DATA

# load data in chunks, apply edits to LON & LAT --- currently given with 3 decimal places
# this code strips away 3rd decimal place, and round values to 0.05 with 0.1 increment
# ie. 5.05 5.15 5.25 etc.

# Step 1: Lazily load the CSV file in chunks
df_population = pl.scan_csv('999 - Data for Rudy - Global/population - germany - TEST.csv')

# Step 2: Round Lon and Lat to 2 decimal places by scaling, flooring, and scaling back
df_population = df_population.with_columns([
    (pl.col("Lon") * 100).floor() / 100,  # Scale up, floor, then scale down
    (pl.col("Lat") * 100).floor() / 100   # Same for Lat
])

# Step 3: Enforce the Lon/Lat format (round down as per your original logic)
df_population = df_population.with_columns([
    ((pl.col("Lon") - 0.05) / 0.1).round(0) * 0.1 + 0.05,
    ((pl.col("Lat") - 0.05) / 0.1).round(0) * 0.1 + 0.05
])

# Step 4: Group by Lon and Lat and sum the population
df_population = df_population.group_by("Lon", "Lat").agg(
    pl.col("population").sum()
)

# Step 5: Collect and process in chunks (streaming)
df_population = df_population.collect(streaming=True)

# Step 6: Print the total sum of the population and the first 10 rows
print(df_population.select(pl.col('population').sum()))
print(df_population.head(10))

# ┌────────────┐
# │ population │
# │ ---        │
# │ f64        │
# ╞════════════╡
# │ 3.2584e8   │
# └────────────┘

# ┌───────┬───────┬─────────────┐
# │ Lon   ┆ Lat   ┆ population  │
# │ ---   ┆ ---   ┆ ---         │
# │ f64   ┆ f64   ┆ f64         │
# ╞═══════╪═══════╪═════════════╡
# │ 17.15 ┆ 58.35 ┆ 0.0         │
# │ 4.95  ┆ 55.75 ┆ 0.0         │
# │ 12.25 ┆ 56.25 ┆ 0.0         │
# │ 1.45  ┆ 49.75 ┆ 6675.954552 │
# │ 14.85 ┆ 53.35 ┆ 3903.063167 │
# │ 16.65 ┆ 51.45 ┆ 3575.241886 │
# │ 4.95  ┆ 40.45 ┆ 0.0         │
# │ 4.75  ┆ 47.05 ┆ 1956.937256 │
# │ 14.65 ┆ 57.65 ┆ 9800.301166 │
# │ 15.75 ┆ 55.45 ┆ 0.0         │
# └───────┴───────┴─────────────┘










# --------------
# MERGE THESE DATAFRAMES
df_overall = df_concentration_baseline.join(
    df_frac_contribution, on=['Lat', 'Lon'], how = "left")

df_overall = df_overall.join(
    df_population, on=['Lat', 'Lon'], how = "left")


# remove areas with no population & contribution exists
df_overall = df_overall.filter(pl.col('population').is_not_null())
#df_overall = df_overall.filter(pl.col('ENEcoal').is_not_null())


# print
print(df_overall.select(pl.col('population').sum()))
print(df_overall.head(10))

# ┌────────────┐
# │ population │
# │ ---        │
# │ f64        │
# ╞════════════╡
# │ 3.2561e8   │
# └────────────┘

# ┌──────┬───────┬───────────────┬─────────┬──────────┬─────────────┐
# │ Lon  ┆ Lat   ┆ concentration ┆ ENEcoal ┆ ENEother ┆ population  │
# │ ---  ┆ ---   ┆ ---           ┆ ---     ┆ ---      ┆ ---         │
# │ f64  ┆ f64   ┆ f32           ┆ f64     ┆ f64      ┆ f64         │
# ╞══════╪═══════╪═══════════════╪═════════╪══════════╪═════════════╡
# │ 5.55 ┆ 59.05 ┆ 5.521869      ┆ null    ┆ null     ┆ 581.544263  │
# │ 5.65 ┆ 59.05 ┆ 5.705568      ┆ null    ┆ null     ┆ 6713.139046 │
# │ 5.75 ┆ 59.05 ┆ 5.908964      ┆ null    ┆ null     ┆ 4113.096908 │
# │ 5.85 ┆ 59.05 ┆ 4.955344      ┆ null    ┆ null     ┆ 40.327717   │
# │ 5.95 ┆ 59.05 ┆ 5.403357      ┆ null    ┆ null     ┆ 4616.310061 │
# │ 6.05 ┆ 59.05 ┆ 5.475357      ┆ null    ┆ null     ┆ 7930.459688 │
# │ 6.15 ┆ 59.05 ┆ 5.438486      ┆ null    ┆ null     ┆ 46.075294   │
# │ 6.25 ┆ 59.05 ┆ 5.106876      ┆ null    ┆ null     ┆ 5.211449    │
# │ 6.35 ┆ 59.05 ┆ 4.694145      ┆ null    ┆ null     ┆ 17.085554   │
# │ 6.45 ┆ 59.05 ┆ 4.688889      ┆ null    ┆ null     ┆ 6.582034    │
# └──────┴───────┴───────────────┴─────────┴──────────┴─────────────┘





# --------------
# delete --- to save memory
del df_population, df_frac_contribution, df_concentration_baseline










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
# 85028610.46618432

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










# convert to panda DF
#df_pandas = df_concentration_cp_annual.to_pandas()

