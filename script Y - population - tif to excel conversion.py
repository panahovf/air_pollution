# In[1]:
# Date: Sep 15, 2024
# Project: Identify population level by grids for select countries
# Author: Farhad Panahov

#   Get grid level 'population estimates' i.e. current concentration levels.
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
import subprocess
from concurrent.futures import ThreadPoolExecutor
import subprocess










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory










# In[4]: CONVERTING TIF FILES TO EXCEL FILES
############################################

# --------
# CHANGE FOLDER FOR EACH COUNTRY

# Directory containing input .tif files
input_dir = r'C:/Users/panah/OneDrive/Desktop/Work/3 - RA - Air pollution/1 - input/3 - population/5 - usa'


# Directory to save output .xyz files
output_dir = r'C:/Users/panah/OneDrive/Desktop/Work/3 - RA - Air pollution/1 - input/3 - population/5 - usa/output_xyz'
os.makedirs(output_dir, exist_ok=True)





# Step 1: Load all .tif files in the directory
tif_files = os.listdir(input_dir)





# Step 2: Convert each .tif file to an .xyz file using gdal_translate
for tif_file in tif_files:
    input_path = os.path.join(input_dir, tif_file)
    layer_name = os.path.splitext(tif_file)[0]
    output_xyz = os.path.join(output_dir, f"{layer_name}.xyz")
    
    cmd = [
        'gdal_translate',
        '-of', 'XYZ',
        input_path,
        output_xyz
    ]
    
    # Run the command
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode == 0:
        print(f"Successfully converted {tif_file} to {output_xyz}")
    else:
        print(f"Failed to convert {input_path} to .xyz. Error: {process.stderr}")

print("Conversion to .xyz completed.")





# Step 3
# Path to the directory containing .xyz files
output_dir2 = r'C:/Users/panah/OneDrive/Desktop/Work/3 - RA - Air pollution/1 - input/3 - population/5 - usa/output_excel'
os.makedirs(output_dir2, exist_ok=True)


# Get the first .xyz file in the directory
xyz_files = [f for f in os.listdir(output_dir) if f.endswith('.xyz')]


# loop through each XYZ file to save in chunks into excel
if not xyz_files:
    print("No .xyz files found in the directory.")
else:
    for xyz_file in xyz_files:
        first_xyz_file = os.path.join(output_dir, xyz_file)
        base_name = os.path.splitext(xyz_file)[0]
        
        # Step 1: Read the .xyz file into a DataFrame
        try:
            df = pd.read_csv(first_xyz_file, delim_whitespace=True, header=None, names=['X', 'Y', 'Value'])
            
            # Step 2: Write the DataFrame to Excel files in chunks of 1 million rows
            max_rows = 1000000  # 1 million rows
            
            for i in range(0, len(df), max_rows):
                df_chunk = df.iloc[i:i + max_rows]
                output_excel = os.path.join(output_dir2, f"{base_name}_part_{i // max_rows + 1}.xlsx")
                df_chunk.to_excel(output_excel, index=False)
                print(f"Successfully wrote {output_excel} with {len(df_chunk)} rows.")
            
            print(f"Successfully converted {first_xyz_file} into multiple Excel files.")
        
        except Exception as e:
            print(f"Error converting {first_xyz_file} to Excel: {e}")













