# In[1]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Step 3: Get grid level 'population estimates' i.e. current concentration levels.
#   Here is the source: https://human-settlement.emergency.copernicus.eu/download.php?ds=pop
#   Product: GHS-POP, epoch: 2020, resolution: 30 arcsec, coordinate system: WGS84
   




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
# LOAD CURRENT POPULATION LEVELS DATA

# File path to the .tif file
tif_file = '1 - input/3 - population/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif'

# Define chunk size (adjust based on memory)
chunk_size = 1000  # Number of rows/columns to process per chunk

# Initialize an empty list to collect DataFrame chunks
df_chunks_combined = []

# Set the batch size for grouping
batch_size = 500

# Read the dataset in chunks
with rasterio.open(tif_file) as dataset:
    width, height = dataset.width, dataset.height
    transform = dataset.transform

    chunk_num = 1  # Initialize chunk counter
    
    # Iterate over the image in chunks
    for row_start in range(0, height, chunk_size):
        for col_start in range(0, width, chunk_size):
            # Step 1: Define the window to read
            window = rasterio.windows.Window(col_start, row_start, chunk_size, chunk_size)
            
            # Step 2: Read the data for the current window
            image_data = dataset.read(1, window=window)
            
            # Step 3: Create arrays for lon/lat
            rows, cols = np.indices(image_data.shape)
            lon, lat = rasterio.transform.xy(transform, rows + row_start, cols + col_start, offset='center')
            
            # Flatten the arrays
            lon_flat = np.array(lon).flatten()
            lat_flat = np.array(lat).flatten()
            pixel_values = image_data.flatten()
            
            # Create a Polars DataFrame
            df_chunk = pl.DataFrame({
                'Lon': lon_flat,
                'Lat': lat_flat,
                'population': pixel_values
            })
            
            # Step 4: Apply transformation to Lon and Lat (round to 2 decimal places)
            df_chunk = df_chunk.with_columns([
                (pl.col('Lon') * 100).floor() / 100,
                (pl.col('Lat') * 100).floor() / 100
            ])
            
            # Step 5: Enforce the Lon/Lat format
            df_chunk = df_chunk.with_columns([
                ((pl.col('Lon') - 0.05) / 0.1).round() * 0.1 + 0.05,
                ((pl.col('Lat') - 0.05) / 0.1).round() * 0.1 + 0.05
            ])
            
            # **Filtering: Remove rows where 'population' is zero or negative**
            df_chunk = df_chunk.filter(pl.col('population') > 0)
            
            # Step 6: Group by Lon and Lat within this chunk and sum the population
            chunk_grouped = df_chunk.group_by(['Lon', 'Lat']).agg(
                pl.col('population').sum()
            )
            
            # Step 7: Accumulate the chunk
            df_chunks_combined.append(chunk_grouped)
            
            # Step 8: Every `batch_size` chunks, concatenate and group
            if chunk_num % batch_size == 0:
                # Concatenate accumulated chunks
                batch_df = pl.concat(df_chunks_combined)
                
                # Group by Lon and Lat for the accumulated batch
                df_overall = batch_df.group_by(['Lon', 'Lat']).agg(
                    pl.col('population').sum()
                )
                
                # Clear the accumulated chunks list
                df_chunks_combined = [df_overall]
                
                # Print progress
                print(f"Processed batch {chunk_num}")
            
            # Increment the chunk counter
            chunk_num += 1
            


# Step 9: Process any remaining accumulated chunks
if df_chunks_combined:
    batch_df = pl.concat(df_chunks_combined)
    df_overall = batch_df.group_by(['Lon', 'Lat']).agg(
        pl.col('population').sum()
    )



# delete
del batch_df, batch_size, chunk_grouped, chunk_size, col_start, cols
del dataset, df_chunk, df_chunks_combined, image_data, lat, lat_flat, lon, lon_flat
del pixel_values, row_start, rows, tif_file, transform, window


# Run results:
print(df_overall['population'].sum()/10**9)
# 7.840952947013648

print(chunk_num)
# 969

# Print the first 10 rows of the final DataFrame
print(df_overall.head(10))

# ┌─────────┬────────┬─────────────┐
# │ Lon     ┆ Lat    ┆ population  │
# │ ---     ┆ ---    ┆ ---         │
# │ f64     ┆ f64    ┆ f64         │
# ╞═════════╪════════╪═════════════╡
# │ 45.85   ┆ 36.65  ┆ 4.575215    │
# │ -63.35  ┆ -10.05 ┆ 1617.909378 │
# │ 8.95    ┆ 47.95  ┆ 6487.507689 │
# │ 30.95   ┆ -25.75 ┆ 6394.52442  │
# │ -71.55  ┆ -45.55 ┆ 178.591444  │
# │ 37.15   ┆ -1.85  ┆ 6820.011595 │
# │ -69.75  ┆ 1.75   ┆ 1792.402471 │
# │ 71.95   ┆ 35.15  ┆ 77740.84904 │
# │ -112.85 ┆ 34.65  ┆ 1.449659    │
# │ 46.55   ┆ 42.45  ┆ 8255.225532 │
# └─────────┴────────┴─────────────┘


# Remove NAs if any
df_overall = df_overall.drop_nulls()

# Save the final aggregated DataFrame to a CSV file
df_overall.write_csv('2 - output/script 1.3 - population - global/1.3 - population - global.csv')

