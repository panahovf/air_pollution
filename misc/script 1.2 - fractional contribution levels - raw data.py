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










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory


# --------------
# LOAD FRACTIONAL CONTRIBUTION DATA

# STEP 2 --- use the indexes from script 1.1 to load and filter all files

# load indexes from previous step
with open("2 - output/script 1.1 - fractional contribution levels - raw data/indices.json") as f:
    indices = json.load(f)


# Convert the indices list into a set to ensure unique values 
length = len(indices) # This stores the length of the indices list
indices = set(indices) # Converts the indices list into a set to ensure unique values
assert len(indices) == length # This ensures that no indices were duplicated by converting the list to a set


# Define the file paths
file_paths = [
    "1 - input/1 - fractional contribution/GBD-MAPS_Gridded_Fractional_Contributions_LatLon.csv",
    "1 - input/1 - fractional contribution/GBD-MAPS_Gridded_Fractional_Contributions_INDcoal.csv",
    "1 - input/1 - fractional contribution/GBD-MAPS_Gridded_Fractional_Contributions_INDother.csv",
]


# Set chunk size and output folder
chunk_size = 100_000
output_folder = "2 - output/script 1.2 - fractional contribution levels - raw data/"


# Iterate over each file to process
for file_path in file_paths:
    
    # Set chunk number and header tracking
    chunk_num = 0
    first_chunk = True  # Write the header only once per file
    
    # Create the output file path
    output_file = os.path.join(output_folder, os.path.basename(file_path).replace(".csv", "_reduced.csv"))
    
    print(f"Processing file: {file_path}")
    
    # Process the file in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Filter data by index
        filtered = chunk[chunk.index.isin(indices)]
        
        # If the filtered chunk has data, write to the output CSV
        if not filtered.empty:
            filtered.to_csv(output_file, mode='a', index=False, header=first_chunk)
            first_chunk = False  # Ensure the header is written only once

        # Print the chunk number only every 1000 chunks
        chunk_num += 1
        if chunk_num % 1000 == 0:
            print(f"Processed chunk {chunk_num} for {os.path.basename(file_path)}")

    print(f"Finished processing file: {file_path}")













