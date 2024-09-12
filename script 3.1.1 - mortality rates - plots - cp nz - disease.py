# In[1]:
# Date: Sep 9, 2024
# Project: Map mortality rates across scenarios and diseases
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
# LOAD SCRIPT 3.1 DATA










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
vmin_stroke = 100  # Set this to your desired minimum value
vmax_stroke = 150 # Set this to your desired maximum value




##################################################################################################
##################### SECTION 1: CURRENT POLICIES: STROKE ########################################
##################################################################################################


# --------------
# 1.1 --- year 2024
# Convert the dataframe to a GeoDataFrame
gdf_cp_2024 = gpd.GeoDataFrame(
    df_annual_mortalityrate_cp_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_cp_total_stroke.lon2, df_annual_mortalityrate_cp_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2024.plot(column='CP_2024', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland current mortality rate from: Stroke", fontsize=20, pad=40)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 1.2 --- year 2030

# Convert the dataframe to a GeoDataFrame
gdf_cp_2030 = gpd.GeoDataFrame(
    df_annual_mortalityrate_cp_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_cp_total_stroke.lon2, df_annual_mortalityrate_cp_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2030.plot(column='CP_2030', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland mortality rates from stroke in 2030: Current Policies", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Prjection based on changes in PM2.5 concentration levels', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 1.3 --- year 2040

# Convert the dataframe to a GeoDataFrame
gdf_cp_2040 = gpd.GeoDataFrame(
    df_annual_mortalityrate_cp_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_cp_total_stroke.lon2, df_annual_mortalityrate_cp_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2040.plot(column='CP_2040', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland mortality rates from stroke in 2040: Current Policies", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Prjection based on changes in PM2.5 concentration levels', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 1.4 --- year 2050

# Convert the dataframe to a GeoDataFrame
gdf_cp_2050 = gpd.GeoDataFrame(
    df_annual_mortalityrate_cp_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_cp_total_stroke.lon2, df_annual_mortalityrate_cp_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2050.plot(column='CP_2050', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland mortality rates from stroke in 2050: Current Policies", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Prjection based on changes in PM2.5 concentration levels', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()










##################################################################################################
##################### SECTION 2: NET ZERO 1.5C 50%: STROKE #######################################
##################################################################################################

# --------------
# 2.1 --- year 2024
# Convert the dataframe to a GeoDataFrame
gdf_nz_2024 = gpd.GeoDataFrame(
    df_annual_mortalityrate_nz_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_nz_total_stroke.lon2, df_annual_mortalityrate_nz_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2024.plot(column='NZ_2024', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland current mortality rate from: Stroke", fontsize=20, pad=40)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 2.2 --- year 2030

# Convert the dataframe to a GeoDataFrame
gdf_nz_2030 = gpd.GeoDataFrame(
    df_annual_mortalityrate_nz_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_nz_total_stroke.lon2, df_annual_mortalityrate_nz_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2030.plot(column='NZ_2030', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland mortality rates from stroke in 2030: Net Zero*", fontsize=20, pad=40)
plt.text(0.5, 1.05, 'Prjection based on changes in PM2.5 concentration levels', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, 'Scenario aligned with global carbon budget limiting global warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 2.3 --- year 2040

# Convert the dataframe to a GeoDataFrame
gdf_nz_2040 = gpd.GeoDataFrame(
    df_annual_mortalityrate_nz_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_nz_total_stroke.lon2, df_annual_mortalityrate_nz_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2040.plot(column='NZ_2040', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland mortality rates from stroke in 2040: Net Zero*", fontsize=20, pad=40)
plt.text(0.5, 1.05, 'Prjection based on changes in PM2.5 concentration levels', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, 'Scenario aligned with global carbon budget limiting global warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 2.4 --- year 2050

# Convert the dataframe to a GeoDataFrame
gdf_nz_2050 = gpd.GeoDataFrame(
    df_annual_mortalityrate_nz_total_stroke, 
    geometry=gpd.points_from_xy(df_annual_mortalityrate_nz_total_stroke.lon2, df_annual_mortalityrate_nz_total_stroke.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2050.plot(column='NZ_2050', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin_stroke, vmax=vmax_stroke,
         legend_kwds={'shrink': 0.5, 'label': "Death per 100k population", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland mortality rates from stroke in 2050: Net Zero*", fontsize=20, pad=40)
plt.text(0.5, 1.05, 'Prjection based on changes in PM2.5 concentration levels', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, 'Scenario aligned with global carbon budget limiting global warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()







