# In[1]:
# Date: Sep 2, 2024
# Project: Map pollution level in 2050 Poland: CP vs NZ 1.5C 67% adjusted
# Author: Farhad Panahov










# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point








# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory


# --------------
# LOAD SCRIPT 1.1 DATA










# In[11]

#####################################################################
#####################################################################
#####################################################################
#####################################################################
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################
#####################################################################
#####################################################################

sns.set_theme(style="ticks")

# Define the min and max values for the color scale
vmin = 5  # Set this to your desired minimum value
vmax = 35  # Set this to your desired maximum value


##################################################################################################
##################### SECTION 1: CURRENT LEVEL ###################################################
##################################################################################################

# Convert the dataframe to a GeoDataFrame
gdf_cp = gpd.GeoDataFrame(
    df_concentration_cp, 
    geometry=gpd.points_from_xy(df_concentration_cp.lon2, df_concentration_cp.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp.plot(column='Current_level', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "PM 2.5 concentration level", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(5, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Current Levels of PM 2.5 Concentration in Poland", fontsize=20, pad=40)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





##################################################################################################
##################### SECTION 2: NZ 2050 #########################################################
##################################################################################################

# Convert the dataframe to a GeoDataFrame
gdf_nz = gpd.GeoDataFrame(
    df_concentration_nz, 
    geometry=gpd.points_from_xy(df_concentration_nz.lon2, df_concentration_nz.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz.plot(column='NZ_2050', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "PM 2.5 concentration level", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(5, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Net Zero 2050 PM 2.5 Concentration in Poland", fontsize=20, pad=40)
plt.text(0.5, 1.04, 'Adjusted global Net Zero scenario aligned with 1.5C warming limitation with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=15)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()









