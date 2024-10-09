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
with rasterio.open('1 - input/2 - concentration levels/IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19.tif') as dataset:
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
df_frac_contribution = pl.scan_csv('1 - input/1 - fractional contribution/fractional contribution - germany.csv')

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
# │ 9.75  ┆ 47.75 ┆ 0.03506 ┆ 0.05252  │
# │ 8.35  ┆ 50.05 ┆ 0.04566 ┆ 0.07473  │
# │ 11.85 ┆ 49.65 ┆ 0.05894 ┆ 0.06314  │
# │ 10.95 ┆ 50.75 ┆ 0.05449 ┆ 0.0622   │
# │ 13.15 ┆ 52.25 ┆ 0.05241 ┆ 0.07116  │
# │ 8.45  ┆ 52.85 ┆ 0.03901 ┆ 0.06522  │
# │ 13.55 ┆ 54.05 ┆ 0.0403  ┆ 0.05288  │
# │ 8.85  ┆ 54.35 ┆ 0.03309 ┆ 0.05648  │
# │ 12.85 ┆ 53.05 ┆ 0.04858 ┆ 0.05661  │
# │ 9.85  ┆ 54.85 ┆ 0.0381  ┆ 0.0646   │
# └───────┴───────┴─────────┴──────────┘









# --------------
# LOAD POPULATION DATA

# load data in chunks, apply edits to LON & LAT --- currently given with 3 decimal places
# this code strips away 3rd decimal place, and round values to 0.05 with 0.1 increment
# ie. 5.05 5.15 5.25 etc.

# Step 1: open all idividual TIF files and combine
# Initialize empty arrays for combined data
lon_flat_list = []
lat_flat_list = []
pixel_values_list = []

# List all your .tif files in the directory
population_path = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution\1 - input\3 - population\1 - germany\tif files'
tif_files = os.listdir(population_path)

# run through file and loads them
for tif_file in tif_files:
    
    file_path = os.path.join(population_path, tif_file) # set file
    
    with rasterio.open(file_path) as dataset:

        image_data = dataset.read(1)
        transform = dataset.transform

        # Create arrays for lon/lat
        rows, cols = np.indices(image_data.shape)
        lon, lat = rasterio.transform.xy(transform, rows, cols, offset='center')

        # Flatten the arrays if needed
        lon_flat = np.array(lon).flatten()
        lat_flat = np.array(lat).flatten()
        pixel_values = image_data.flatten()

        # Append to list
        lon_flat_list.append(lon_flat)
        lat_flat_list.append(lat_flat)
        pixel_values_list.append(pixel_values)

# Concatenate all the data together
lon_flat_combined = np.concatenate(lon_flat_list)
lat_flat_combined = np.concatenate(lat_flat_list)
pixel_values_combined = np.concatenate(pixel_values_list)

# Create a DataFrame with the combined data
df_population = pl.DataFrame({
    'Lon': lon_flat_combined,
    'Lat': lat_flat_combined,
    'population': pixel_values_combined
})

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

# delete extras
del cols, dataset, file_path, image_data, pixel_values, pixel_values_combined, pixel_values_list
del lat, lat_flat, lat_flat_combined, lat_flat_list, lon, lon_flat, lon_flat_combined, lon_flat_list
del rows, tif_file, tif_files, transform, population_path

# Print the total sum of the population and the first 10 rows
print(df_population.select(pl.col('population').sum()))
print(df_population.head(10))

# ┌────────────┐
# │ population │
# │ ---        │
# │ f64        │
# ╞════════════╡
# │ 3.8348e8   │
# └────────────┘

# ┌─────────┬───────┬─────────────┐
# │ Lon     ┆ Lat   ┆ population  │
# │ ---     ┆ ---   ┆ ---         │
# │ f64     ┆ f64   ┆ f64         │
# ╞═════════╪═══════╪═════════════╡
# │ 8.05    ┆ 41.15 ┆ 0.0         │
# │ 16.55   ┆ 58.15 ┆ 564.552309  │
# │ 38.15   ┆ 54.15 ┆ 2125.121163 │
# │ -104.05 ┆ 31.45 ┆ 0.0         │
# │ 30.75   ┆ 52.15 ┆ 630.739443  │
# │ 29.95   ┆ 52.55 ┆ 0.831385    │
# │ 11.15   ┆ 56.95 ┆ 0.0         │
# │ 37.05   ┆ 53.05 ┆ 75.844097   │
# │ 5.45    ┆ 40.25 ┆ 0.0         │
# │ 2.35    ┆ 45.15 ┆ 1516.434773 │
# └─────────┴───────┴─────────────┘










# --------------
# MERGE THESE DATAFRAMES
df_overall = df_concentration_baseline.join(
    df_frac_contribution, on=['Lat', 'Lon'], how = "inner")

df_overall = df_overall.join(
    df_population, on=['Lat', 'Lon'], how = "inner")

# print
print(df_overall.select(pl.col('population').sum()))
print(df_overall.head(10))

# ┌────────────┐
# │ population │
# │ ---        │
# │ f64        │
# ╞════════════╡
# │ 8.5029e7   │
# └────────────┘

# ┌───────┬───────┬───────────────┬─────────┬──────────┬──────────────┐
# │ Lon   ┆ Lat   ┆ concentration ┆ ENEcoal ┆ ENEother ┆ population   │
# │ ---   ┆ ---   ┆ ---           ┆ ---     ┆ ---      ┆ ---          │
# │ f64   ┆ f64   ┆ f32           ┆ f64     ┆ f64      ┆ f64          │
# ╞═══════╪═══════╪═══════════════╪═════════╪══════════╪══════════════╡
# │ 12.05 ┆ 51.45 ┆ 9.517048      ┆ 0.06206 ┆ 0.07975  ┆ 34468.606945 │
# │ 11.05 ┆ 50.15 ┆ 9.550855      ┆ 0.05684 ┆ 0.0626   ┆ 22587.661258 │
# │ 7.75  ┆ 51.95 ┆ 9.849114      ┆ 0.05841 ┆ 0.11525  ┆ 34676.574198 │
# │ 12.15 ┆ 48.85 ┆ 10.463086     ┆ 0.05121 ┆ 0.07357  ┆ 7939.793262  │
# │ 12.55 ┆ 53.25 ┆ 9.430255      ┆ 0.04858 ┆ 0.05661  ┆ 1166.358503  │
# │ 7.45  ┆ 52.95 ┆ 9.408301      ┆ 0.03917 ┆ 0.07378  ┆ 3668.919374  │
# │ 13.25 ┆ 53.15 ┆ 9.050261      ┆ 0.05038 ┆ 0.05827  ┆ 1867.469851  │
# │ 9.45  ┆ 54.85 ┆ 9.813777      ┆ 0.03731 ┆ 0.06714  ┆ 25792.940878 │
# │ 6.95  ┆ 50.65 ┆ 8.940134      ┆ 0.04644 ┆ 0.11876  ┆ 31562.676619 │
# │ 7.95  ┆ 49.55 ┆ 8.068864      ┆ 0.04027 ┆ 0.06562  ┆ 5072.934363  │
# └───────┴───────┴───────────────┴─────────┴──────────┴──────────────┘





# --------------
# delete --- to save memory
del df_population, df_frac_contribution, df_concentration_baseline










# In[4]: NOW LOAD EMISSIONS DATA AND GET PHASE OUT PACE
#######################################################

# --------------
# LOAD EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power = pl.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\9.1 - Current policy - Secondary - annual.xlsx')
df_nz_power = pl.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')


# Step 1
# filter to Germany
df_cp_power = df_cp_power.filter(pl.col("Region") == "DEU")
df_nz_power = df_nz_power.filter(pl.col("Region") == "DEU")


# Step 2
# Identify the year columns
year_columns = [str(year) for year in range(2024, 2051)]
year_columns_nz = [f'NZ_{year}' for year in range(2024, 2051)]
year_columns_cp = [f'CP_{year}' for year in range(2024, 2051)]


# Step 3
# --------------
# Combine Oil and Gas emissions for both power and extraction to match fraction contribution data

# CP power
temp = df_cp_power.filter(pl.col('fuel_type') == 'Oil').with_columns(pl.lit('O&G').alias('fuel_type'))  # Copy and modify 'fuel_type'
sum_oil_gas = df_cp_power.filter(pl.col('fuel_type').is_in(['Oil', 'Gas'])).select(year_columns).sum()  # Sum the 'Oil' and 'Gas' rows for the year columns
temp = temp.with_columns([pl.lit(sum_oil_gas[column]).alias(column) for column in year_columns])   # Apply the summed values to the temp DataFrame
df_cp_power = df_cp_power.vstack(temp)   # Append the new row to the original DataFrame
df_cp_power = df_cp_power.filter(~pl.col('fuel_type').is_in(['Oil', 'Gas']))   # Remove the original 'Oil' and 'Gas' rows


# NZ power
temp = df_nz_power.filter(pl.col('fuel_type') == 'Oil').with_columns(pl.lit('O&G').alias('fuel_type'))  # Copy and modify 'fuel_type'
sum_oil_gas = df_nz_power.filter(pl.col('fuel_type').is_in(['Oil', 'Gas'])).select(year_columns).sum()   # Sum the 'Oil' and 'Gas' rows for the year columns
temp = temp.with_columns([pl.lit(sum_oil_gas[column]).alias(column) for column in year_columns])   # Apply the summed values to the temp DataFrame
df_nz_power = df_nz_power.vstack(temp)   # Append the new row to the original DataFrame
df_nz_power = df_nz_power.filter(~pl.col('fuel_type').is_in(['Oil', 'Gas']))   # Remove the original 'Oil' and 'Gas' rows


del temp, sum_oil_gas


# Step 4
# --------------
# Get CP vs NZ difference: (1-NZ)/Current levels
# i.e. emissions reduction under NZ as a share of current level
df_nz_power_reduction = df_nz_power.with_columns([
    (1 - pl.col(year_column) / pl.col('2024')).alias(year_column) for year_column in year_columns
])

# --------------
# Get CP vs NZ difference: (1-CP)/Current levels
# i.e. emissions reduction under CP as a share of current level
df_cp_power_reduction = df_cp_power.with_columns([
    (1 - pl.col(year_column) / pl.col('2024')).alias(year_column) for year_column in year_columns
])


# delete
del df_cp_power, df_nz_power


print(df_cp_power_reduction.head(10))
# ┌────────────┬────────────┬────────┬────────────┬───┬──────────┬───────────┬───────────┬───────────┐
# │ Model      ┆ Scenario   ┆ Region ┆ gca_region ┆ … ┆ 2047     ┆ 2048      ┆ 2049      ┆ 2050      │
# │ ---        ┆ ---        ┆ ---    ┆ ---        ┆   ┆ ---      ┆ ---       ┆ ---       ┆ ---       │
# │ str        ┆ str        ┆ str    ┆ str        ┆   ┆ f64      ┆ f64       ┆ f64       ┆ f64       │
# ╞════════════╪════════════╪════════╪════════════╪═══╪══════════╪═══════════╪═══════════╪═══════════╡
# │ Downscalin ┆ Current    ┆ DEU    ┆ Europe     ┆ … ┆ 0.151595 ┆ 0.193189  ┆ 0.234783  ┆ 0.276377  │
# │ g[GCAM 6.0 ┆ Policies   ┆        ┆            ┆   ┆          ┆           ┆           ┆           │
# │ NGFS]      ┆            ┆        ┆            ┆   ┆          ┆           ┆           ┆           │
# │ Downscalin ┆ Current    ┆ DEU    ┆ Europe     ┆ … ┆ 0.016317 ┆ -0.019274 ┆ -0.054865 ┆ -0.090455 │
# │ g[GCAM 6.0 ┆ Policies   ┆        ┆            ┆   ┆          ┆           ┆           ┆           │
# │ NGFS]      ┆            ┆        ┆            ┆   ┆          ┆           ┆           ┆           │
# └────────────┴────────────┴────────┴────────────┴───┴──────────┴───────────┴───────────┴───────────┘

print(df_nz_power_reduction.head(10))
# ┌───────────────────┬──────────┬────────┬────────────┬───┬──────────┬──────────┬──────────┬────────┐
# │ Model             ┆ Scenario ┆ Region ┆ gca_region ┆ … ┆ 2047     ┆ 2048     ┆ 2049     ┆ 2050   │
# │ ---               ┆ ---      ┆ ---    ┆ ---        ┆   ┆ ---      ┆ ---      ┆ ---      ┆ ---    │
# │ str               ┆ str      ┆ str    ┆ str        ┆   ┆ f64      ┆ f64      ┆ f64      ┆ f64    │
# ╞═══════════════════╪══════════╪════════╪════════════╪═══╪══════════╪══════════╪══════════╪════════╡
# │ Downscaling[GCAM  ┆ Net Zero ┆ DEU    ┆ Europe     ┆ … ┆ 1.0      ┆ 1.0      ┆ 1.0      ┆ 1.0    │
# │ 6.0 NGFS]         ┆ 2050     ┆        ┆            ┆   ┆          ┆          ┆          ┆        │
# │ Downscaling[GCAM  ┆ Net Zero ┆ DEU    ┆ Europe     ┆ … ┆ 0.997458 ┆ 0.998282 ┆ 0.998933 ┆ 0.9994 │
# │ 6.0 NGFS]         ┆ 2050     ┆        ┆            ┆   ┆          ┆          ┆          ┆        │
# └───────────────────┴──────────┴────────┴────────────┴───┴──────────┴──────────┴──────────┴────────┘




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

print(df_concentration_nz_total.head(10))
┌───────┬───────┬───────────────┬─────────┬───┬──────────┬──────────┬──────────┬──────────┐
│ Lon   ┆ Lat   ┆ concentration ┆ ENEcoal ┆ … ┆ NZ_2047  ┆ NZ_2048  ┆ NZ_2049  ┆ NZ_2050  │
│ ---   ┆ ---   ┆ ---           ┆ ---     ┆   ┆ ---      ┆ ---      ┆ ---      ┆ ---      │
│ f64   ┆ f64   ┆ f32           ┆ f64     ┆   ┆ f64      ┆ f64      ┆ f64      ┆ f64      │
╞═══════╪═══════╪═══════════════╪═════════╪═══╪══════════╪══════════╪══════════╪══════════╡
│ 7.65  ┆ 50.35 ┆ 8.749325      ┆ 0.04369 ┆ … ┆ 7.549863 ┆ 7.549188 ┆ 7.548654 ┆ 7.548272 │
│ 14.55 ┆ 51.35 ┆ 10.392959     ┆ 0.07921 ┆ … ┆ 8.725793 ┆ 8.725095 ┆ 8.724544 ┆ 8.724149 │
│ 8.35  ┆ 50.85 ┆ 8.485989      ┆ 0.04846 ┆ … ┆ 7.41047  ┆ 7.409922 ┆ 7.409487 ┆ 7.409177 │
│ 8.45  ┆ 50.65 ┆ 9.73105       ┆ 0.04846 ┆ … ┆ 8.497733 ┆ 8.497103 ┆ 8.496605 ┆ 8.496249 │
│ 12.65 ┆ 49.05 ┆ 9.600057      ┆ 0.05619 ┆ … ┆ 8.429977 ┆ 8.429456 ┆ 8.429044 ┆ 8.428749 │
│ 10.35 ┆ 50.85 ┆ 8.653901      ┆ 0.0532  ┆ … ┆ 7.651862 ┆ 7.651414 ┆ 7.65106  ┆ 7.650807 │
│ 11.55 ┆ 48.55 ┆ 9.76349       ┆ 0.05096 ┆ … ┆ 8.493471 ┆ 8.492833 ┆ 8.492328 ┆ 8.491967 │
│ 8.55  ┆ 54.95 ┆ 6.07165       ┆ 0.03282 ┆ … ┆ 5.454257 ┆ 5.453912 ┆ 5.453638 ┆ 5.453443 │
│ 13.65 ┆ 51.35 ┆ 9.735868      ┆ 0.07045 ┆ … ┆ 8.249877 ┆ 8.249216 ┆ 8.248693 ┆ 8.248319 │
│ 12.85 ┆ 53.55 ┆ 9.191581      ┆ 0.04456 ┆ … ┆ 8.278761 ┆ 8.278345 ┆ 8.278016 ┆ 8.277781 │
└───────┴───────┴───────────────┴─────────┴───┴──────────┴──────────┴──────────┴──────────┘








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
    coal_reduction = df_cp_power_reduction.filter(pl.col('fuel_type') == 'Coal').select(pl.col(year)).item(0, 0)
    oilgas_reduction = df_cp_power_reduction.filter(pl.col('fuel_type') == 'O&G').select(pl.col(year)).item(0, 0)

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

print(df_concentration_cp_total.head(10))
# ┌───────┬───────┬───────────────┬─────────┬───┬───────────┬───────────┬──────────┬───────────┐
# │ Lon   ┆ Lat   ┆ concentration ┆ ENEcoal ┆ … ┆ CP_2047   ┆ CP_2048   ┆ CP_2049  ┆ CP_2050   │
# │ ---   ┆ ---   ┆ ---           ┆ ---     ┆   ┆ ---       ┆ ---       ┆ ---      ┆ ---       │
# │ f64   ┆ f64   ┆ f32           ┆ f64     ┆   ┆ f64       ┆ f64       ┆ f64      ┆ f64       │
# ╞═══════╪═══════╪═══════════════╪═════════╪═══╪═══════════╪═══════════╪══════════╪═══════════╡
# │ 7.65  ┆ 50.35 ┆ 8.749325      ┆ 0.04369 ┆ … ┆ 8.678008  ┆ 8.691267  ┆ 8.704527 ┆ 8.717787  │
# │ 14.55 ┆ 51.35 ┆ 10.392959     ┆ 0.07921 ┆ … ┆ 10.254356 ┆ 10.250228 ┆ 10.2461  ┆ 10.241972 │
# │ 8.35  ┆ 50.85 ┆ 8.485989      ┆ 0.04846 ┆ … ┆ 8.412781  ┆ 8.419379  ┆ 8.425977 ┆ 8.432575  │
# │ 8.45  ┆ 50.65 ┆ 9.73105       ┆ 0.04846 ┆ … ┆ 9.647102  ┆ 9.654668  ┆ 9.662234 ┆ 9.669801  │
# │ 12.65 ┆ 49.05 ┆ 9.600057      ┆ 0.05619 ┆ … ┆ 9.507965  ┆ 9.508031  ┆ 9.508097 ┆ 9.508163  │
# │ 10.35 ┆ 50.85 ┆ 8.653901      ┆ 0.0532  ┆ … ┆ 8.575248  ┆ 8.575425  ┆ 8.575603 ┆ 8.575781  │
# │ 11.55 ┆ 48.55 ┆ 9.76349       ┆ 0.05096 ┆ … ┆ 9.675427  ┆ 9.682295  ┆ 9.689163 ┆ 9.696031  │
# │ 8.55  ┆ 54.95 ┆ 6.07165       ┆ 0.03282 ┆ … ┆ 6.034601  ┆ 6.041232  ┆ 6.047862 ┆ 6.054493  │
# │ 13.65 ┆ 51.35 ┆ 9.735868      ┆ 0.07045 ┆ … ┆ 9.618801  ┆ 9.618821  ┆ 9.618841 ┆ 9.618861  │
# │ 12.85 ┆ 53.55 ┆ 9.191581      ┆ 0.04456 ┆ … ┆ 9.121258  ┆ 9.122179  ┆ 9.1231   ┆ 9.12402   │
# └───────┴───────┴───────────────┴─────────┴───┴───────────┴───────────┴──────────┴───────────┘










# In[4]: GET OVERALL BASED ON POPULATION WEIGHTS
################################################


# find population-weights
var_total_population = df_overall.select(pl.col('population').sum()).item(0, 0)
# 85028610.45799617

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










# In[]

# convert to panda DF & export data
df_pandas_cp = df_concentration_cp_annual.to_pandas()
df_pandas_nz = df_concentration_nz_annual.to_pandas()


# annual concentration levels
df_pandas_cp.to_excel('2 - output/script 2.2 - air pollution concentration levels - by scenario - germany/1.1 - annual concentration levels - current policy - polars.xlsx', index = False)
df_pandas_nz.to_excel('2 - output/script 2.2 - air pollution concentration levels - by scenario - germany/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted - polars.xlsx', index = False)


