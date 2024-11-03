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
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.gridspec as gridspec
import scienceplots
import seaborn as sns
from matplotlib.ticker import MaxNLocator







# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory


year_columns = [str(year) for year in range(2024, 2051)]


# --------------
# LOAD SCRIPT DATA 2.1 (version 2)
df_germany = pd.read_excel('2 - output/script 2.2 - air pollution concentration levels - by scenario - germany/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx')
df_indonesia = pd.read_excel('2 - output/script 2.3 - air pollution concentration levels - by scenario - indonesia/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx')
df_india = pd.read_excel('2 - output/script 2.4 - air pollution concentration levels - by scenario - india/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx')
df_turkeye = pd.read_excel('2 - output/script 2.5 - air pollution concentration levels - by scenario - turkeye/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx')
df_usa = pd.read_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx')
df_vietnam = pd.read_excel('2 - output/script 2.7 - air pollution concentration levels - by scenario - vietnam/7.1 - concentration level - netzero 1.5C 50% adjusted - grid level.xlsx')

# Convert the dataframe to a GeoDataFrame
gdf_germany = gpd.GeoDataFrame(
    df_germany, 
    geometry=gpd.points_from_xy(df_germany.lon2, df_germany.lat2)
)

gdf_indonesia = gpd.GeoDataFrame(
    df_indonesia, 
    geometry=gpd.points_from_xy(df_indonesia.lon2, df_indonesia.lat2)
)

gdf_india = gpd.GeoDataFrame(
    df_india, 
    geometry=gpd.points_from_xy(df_india.lon2, df_india.lat2)
)

gdf_turkeye = gpd.GeoDataFrame(
    df_turkeye, 
    geometry=gpd.points_from_xy(df_turkeye.lon2, df_turkeye.lat2)
)

gdf_usa = gpd.GeoDataFrame(
    df_usa, 
    geometry=gpd.points_from_xy(df_usa.lon2, df_usa.lat2)
)

gdf_vietnam = gpd.GeoDataFrame(
    df_vietnam, 
    geometry=gpd.points_from_xy(df_vietnam.lon2, df_vietnam.lat2)
)


# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))











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

# Style
plt.style.use(['science'])

# Disable LaTeX rendering to avoid LaTeX-related errors
plt.rcParams['text.usetex'] = False



##################################################################################################
##################### SECTION 1: CURRENT POLICIES ################################################
##################################################################################################



# Sample data for demonstration purposes
countries = ['Germany', 'Indonesia', 'India', 'Turkiye', 'USA', 'Vietnam']
years = ['2024', '2035', '2050']
dataframes = [gdf_germany, gdf_indonesia, gdf_india, gdf_turkeye, gdf_usa, gdf_vietnam]

# Set up colormap themes for each country
country_cmaps = ['viridis', 'plasma', 'cividis', 'viridis', 'plasma', 'cividis']


# Define the min and max values for each country dynamically
# Set mean + 3std as max
for country, df_country in zip(countries, dataframes):
    globals()[f'min_{country}'] = df_country[['NZ_2024', 'NZ_2035', 'NZ_2050']].min().min()
    globals()[f'max_{country}'] = df_country[['NZ_2024', 'NZ_2035', 'NZ_2050']].mean().mean() + 3*df_country[['NZ_2024', 'NZ_2035', 'NZ_2050']].std().mean()


# Create a figure with 6 rows and 3 columns (countries x years) without constrained_layout
fig, axs = plt.subplots(6, 3, figsize=(18, 24), constrained_layout=True)

# Iterate over each country and each year
for i, (country, df_country, cmap) in enumerate(zip(countries, dataframes, country_cmaps)):
    for j, year in enumerate(years):
        ax = axs[i, j]

        # Plot the entire world map as background
        world.plot(ax=ax, color='lightgrey', edgecolor='black')

        # Retrieve min and max values for color scaling using globals()
        vmin = globals()[f'min_{country}']
        vmax = globals()[f'max_{country}']
        
        # Plot the data for the specific country and year without the world background
        df_country.plot(column=f'NZ_{year}', ax=ax, legend=(j == 2), cmap=cmap, 
                        markersize= 5, vmin=vmin, vmax=vmax,
                        legend_kwds={'shrink': 0.75, 'orientation': "vertical"})

        # Set title only for the first row of each column
        if i == 0:
            ax.set_title(f"Year {year}", fontsize=14, pad=15)
        
        # Set ylabel for the first column (country name)
        if j == 0:
            ax.annotate(country, xy=(-0.1, 0.5), xycoords='axes fraction', fontsize=20, fontweight='bold',
                        ha='right', va='center', rotation=90)

        # Set the limits to zoom into the area around the country
        ax.set_xlim(df_country['lon2'].min() - 2, df_country['lon2'].max() + 2)  # Longitude limits 
        ax.set_ylim(df_country['lat2'].min() - 2, df_country['lat2'].max() + 2)  # Latitude limits

        # Remove x and y axis labels and ticks for better visualization
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")

# Show the plot
plt.show()








