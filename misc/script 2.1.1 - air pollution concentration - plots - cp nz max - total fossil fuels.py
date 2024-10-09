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
# LOAD SCRIPT DATA 2.1 (version 2)

# change columd name
df_concentration_cp_total.rename(columns={"CP_2050": "2050"}, inplace=True)
df_concentration_nz_total.rename(columns={"NZ_2050": "2050"}, inplace=True)




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


# FIND RANGE FOR CONCETRATION LEVELS
# Calculate the mean and standard deviation for 'concentration'
mean_concentration = df_concentration_cp_total['concentration'].mean()
std_concentration = df_concentration_cp_total['concentration'].std()

# Define the lower and upper bounds using ± standard deviation
vmin_std = mean_concentration - 1 * std_concentration
vmax_std = mean_concentration + 1 * std_concentration

# Display the mean, standard deviation, and the derived range
mean_concentration, std_concentration, vmin_std, vmax_std

# Define the min and max values for the color scale
vmin = vmin_std  # Set this to your desired minimum value
vmax = vmax_std  # Set this to your desired maximum value





##################################################################################################
##################### SECTION 1: CURRENT POLICIES ################################################
##################################################################################################




# Create a figure with 2 rows and 1 column for the combined top and bottom layout
fig, axs = plt.subplots(2, 1, figsize=(15, 20), constrained_layout=True)

# Load the world map using GeoPandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Define the scenarios and the dataframes to be used
scenarios = ["Current Policies", "Net Zero 1.5°C warming *"]
dataframes = [df_concentration_cp_total, df_concentration_nz_total]

# Iterate over axes, scenarios, and dataframes to plot each
for ax, scenario, df in zip(axs, scenarios, dataframes):
    # Plot the world map for context
    world.plot(ax=ax, color='lightgrey', edgecolor='black')


    # Plot the points for PM2.5 concentrations using scatter plot
    sc = ax.scatter(df['Lon'], df['Lat'],
                    c=df['2050'], cmap='viridis', s=1,
                    vmin=5, vmax=35)  # Set vmin and vmax based on reasonable global values

    # Add titles for each subplot
    ax.set_title(f"{scenario}", fontsize=16, pad=20)
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)

# Add a single colorbar to the figure that is shared across both plots
fig.colorbar(sc, ax=axs, orientation='horizontal', fraction=0.05, pad=0.05, label="PM2.5 Concentration (mg/m$^3$)")

# Add the main title and subtitle
fig.suptitle('Global PM2.5 Concentration Levels in 2050', fontsize=20, fontweight='bold', y=1.02)
fig.text(0.5, 0.99, 'Based on NGFS GCAM6 model emissions projections', ha='center', fontsize=12)
fig.text(0.5, 0.97, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Show the combined plot
plt.show()








# --------------
# 1.1 --- year 2030

# Convert the dataframe to a GeoDataFrame
gdf_cp_2030 = gpd.GeoDataFrame(
    df_concentration_cp_total, 
    geometry=gpd.points_from_xy(df_concentration_cp_total.Lon, df_concentration_cp_total.Lat)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2030.plot(column='CP_2030', ax=ax, legend=True, cmap='viridis', 
         markersize=1, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2030: Current Policies", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model\'s \"Current Policies\" scenario', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 1.2 --- year 2040

# Convert the dataframe to a GeoDataFrame
gdf_cp_2040 = gpd.GeoDataFrame(
    df_concentration_cp_total, 
    geometry=gpd.points_from_xy(df_concentration_cp_total.Lon, df_concentration_cp_total.Lat)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2040.plot(column='CP_2040', ax=ax, legend=True, cmap='viridis', 
         markersize=1, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2040: Current Policies", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model\'s \"Current Policies\" scenario', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 1.3 --- year 2050

# Convert the dataframe to a GeoDataFrame
gdf_cp_2050 = gpd.GeoDataFrame(
    df_concentration_cp_total, 
    geometry=gpd.points_from_xy(df_concentration_cp_total.Lon, df_concentration_cp_total.Lat)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_cp_2050.plot(column='CP_2050', ax=ax, legend=True, cmap='viridis', 
         markersize=1, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2050: Current Policies", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model\'s \"Current Policies\" scenario', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()










##################################################################################################
##################### SECTION 2: NET ZERO 1.5C 50% aligned #######################################
##################################################################################################

# --------------
# 2.1 --- year 2030

# Convert the dataframe to a GeoDataFrame
gdf_nz_2030 = gpd.GeoDataFrame(
    df_concentration_nz_total, 
    geometry=gpd.points_from_xy(df_concentration_nz_total.Lon, df_concentration_nz_total.Lat)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2030.plot(column='NZ_2030', ax=ax, legend=True, cmap='viridis', 
         markersize=1, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})


# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2030: Net Zero 1.5°C", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Emissions from current power plants in operation are projected using modified growth rates from NGFS GCAM6 model to align \n cumulative global emissions with carbon budget boundaries (50% likelyhood for global warming)', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 2.2 --- year 2040

# Convert the dataframe to a GeoDataFrame
gdf_nz_2040 = gpd.GeoDataFrame(
    df_concentration_nz_total, 
    geometry=gpd.points_from_xy(df_concentration_nz_total.Lon, df_concentration_nz_total.Lat)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2040.plot(column='NZ_2040', ax=ax, legend=True, cmap='viridis', 
         markersize=1, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2040: Net Zero 1.5°C", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Emissions from current power plants in operation are projected using modified growth rates from NGFS GCAM6 model to align \n cumulative global emissions with carbon budget boundaries (50% likelyhood for global warming)', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 2.3 --- year 2050

# Convert the dataframe to a GeoDataFrame
gdf_nz_2050 = gpd.GeoDataFrame(
    df_concentration_nz_total, 
    geometry=gpd.points_from_xy(df_concentration_nz_total.Lon, df_concentration_nz_total.Lat)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_nz_2050.plot(column='NZ_2050', ax=ax, legend=True, cmap='viridis', 
         markersize=1, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2050: Net Zero 1.5°C", fontsize=20, pad=40)
plt.text(0.5, 1.02, 'Emissions from current power plants in operation are projected using modified growth rates from NGFS GCAM6 model to align \n cumulative global emissions with carbon budget boundaries (50% likelyhood for global warming)', transform=ax.transAxes, ha='center', fontsize=12)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()










##################################################################################################
##################### SECTION 3: CURRENT AND MAX SHUT DOWN #######################################
##################################################################################################

# --------------
# 3.1 --- year 2024

# Convert the dataframe to a GeoDataFrame
gdf_year2024 = gpd.GeoDataFrame(
    df_concentration_cp_total, 
    geometry=gpd.points_from_xy(df_concentration_cp_total.lon2, df_concentration_cp_total.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_year2024.plot(column='CP_2024', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels in 2024", fontsize=20, pad=40)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()





# --------------
# 3.2 --- max shut down

# Convert the dataframe to a GeoDataFrame
gdf_max = gpd.GeoDataFrame(
    df_concentration_max_total, 
    geometry=gpd.points_from_xy(df_concentration_max_total.lon2, df_concentration_max_total.lat2)
)

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot the entire world map
world.plot(ax=ax, color='lightgrey')

# Plot the points on the map with fixed color scale
gdf_max.plot(column='MX_2024', ax=ax, legend=True, cmap='viridis', 
         markersize=50, vmin=vmin, vmax=vmax,
         legend_kwds={'shrink': 0.5, 'label': "mg/m$^3$", 'orientation': "vertical"})

# Set the limits to zoom into the area around Poland
ax.set_xlim(10, 30)  # Longitude limits (western and eastern Europe)
ax.set_ylim(45, 60)  # Latitude limits (central Europe)

# Add titles and labels
ax.set_title("Poland PM2.5 concentration levels: Complete phase-out of fossil fuels", fontsize=20, pad=40)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()