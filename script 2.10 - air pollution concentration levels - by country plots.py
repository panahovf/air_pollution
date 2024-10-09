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
# germany
df_concentration_cp_pop = pd.read_excel('2 - output/script 2.2 - air pollution concentration levels - by scenario - germany/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_cp_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/1.1 - annual concentration levels - current policy - Germany.xlsx')

df_concentration_nz_pop = pd.read_excel('2 - output/script 2.2 - air pollution concentration levels - by scenario - germany/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')
df_concentration_nz_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted - Germany.xlsx')

df_germany = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp_pop['total_fossil'],
    'cp_nopop': df_concentration_cp_nopop['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz_pop['total_fossil'],
    'nz_nopop': df_concentration_nz_nopop['total_fossil_nonweight']
})




# indonesia
df_concentration_cp_pop = pd.read_excel('2 - output/script 2.3 - air pollution concentration levels - by scenario - indonesia/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_cp_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/2.1 - annual concentration levels - current policy - Indonesia.xlsx')

df_concentration_nz_pop = pd.read_excel('2 - output/script 2.3 - air pollution concentration levels - by scenario - indonesia/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')
df_concentration_nz_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/2.2 - annual concentration levels - netzero 1.5C 50% adjsuted - Indonesia.xlsx')

df_indonesia = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp_pop['total_fossil'],
    'cp_nopop': df_concentration_cp_nopop['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz_pop['total_fossil'],
    'nz_nopop': df_concentration_nz_nopop['total_fossil_nonweight']
})




# india
df_concentration_cp_pop = pd.read_excel('2 - output/script 2.4 - air pollution concentration levels - by scenario - india/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_cp_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/3.1 - annual concentration levels - current policy - India.xlsx')

df_concentration_nz_pop = pd.read_excel('2 - output/script 2.4 - air pollution concentration levels - by scenario - india/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')
df_concentration_nz_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/3.2 - annual concentration levels - netzero 1.5C 50% adjsuted - India.xlsx')

df_india = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp_pop['total_fossil'],
    'cp_nopop': df_concentration_cp_nopop['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz_pop['total_fossil'],
    'nz_nopop': df_concentration_nz_nopop['total_fossil_nonweight']
})




# turkeye
df_concentration_cp_pop = pd.read_excel('2 - output/script 2.5 - air pollution concentration levels - by scenario - turkeye/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_cp_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/4.1 - annual concentration levels - current policy - Turkeye.xlsx')

df_concentration_nz_pop = pd.read_excel('2 - output/script 2.5 - air pollution concentration levels - by scenario - turkeye/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')
df_concentration_nz_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/4.2 - annual concentration levels - netzero 1.5C 50% adjsuted - Turkeye.xlsx')

df_turkeye = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp_pop['total_fossil'],
    'cp_nopop': df_concentration_cp_nopop['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz_pop['total_fossil'],
    'nz_nopop': df_concentration_nz_nopop['total_fossil_nonweight']
})




# usa
df_concentration_cp_pop = pd.read_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_cp_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/5.1 - annual concentration levels - current policy - USA.xlsx')

df_concentration_nz_pop = pd.read_excel('2 - output/script 2.6 - air pollution concentration levels - by scenario - usa/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')
df_concentration_nz_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/5.2 - annual concentration levels - netzero 1.5C 50% adjsuted - USA.xlsx')

df_usa = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp_pop['total_fossil'],
    'cp_nopop': df_concentration_cp_nopop['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz_pop['total_fossil'],
    'nz_nopop': df_concentration_nz_nopop['total_fossil_nonweight']
})




# vietnam
df_concentration_cp_pop = pd.read_excel('2 - output/script 2.7 - air pollution concentration levels - by scenario - vietnam/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_cp_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/6.1 - annual concentration levels - current policy - Vietnam.xlsx')

df_concentration_nz_pop = pd.read_excel('2 - output/script 2.7 - air pollution concentration levels - by scenario - vietnam/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')
df_concentration_nz_nopop = pd.read_excel('2 - output/script 2.10 - air pollution concentration levels - by scenario - non-adjusted/6.2 - annual concentration levels - netzero 1.5C 50% adjsuted - Vietnam.xlsx')

df_vietnam = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp_pop['total_fossil'],
    'cp_nopop': df_concentration_cp_nopop['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz_pop['total_fossil'],
    'nz_nopop': df_concentration_nz_nopop['total_fossil_nonweight']
})




# global
df_concentration_cp = pd.read_excel('2 - output/script 2.1 - air pollution concentration levels - by scenario - global/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_nz = pd.read_excel('2 - output/script 2.1 - air pollution concentration levels - by scenario - global/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')

df_global = pd.DataFrame({
    'year': year_columns,
    'cp_pop': df_concentration_cp['total_fossil'],
    'cp_nopop': df_concentration_cp['total_fossil_nonweight'],
    'nz_pop': df_concentration_nz['total_fossil'],
    'nz_nopop': df_concentration_nz['total_fossil_nonweight']
})


del df_concentration_cp_nopop, df_concentration_cp_pop, df_concentration_nz_nopop, df_concentration_nz_pop
del df_concentration_nz, df_concentration_cp






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

def thousands_formatter_0dec(x, pos):
    return f'{x/1000:.0f}'

# colors
colors = {
    'death': '#800080',  # Dark Green
    'benefit': '#006400'  # Purple for Nuclear
}    





##################################################################################################
##################### SECTION 1: CURRENT POLICIES ################################################
##################################################################################################


    
# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    # Plot Current Policy scenarios with and without population
    ax.plot(df_country['year'], df_country['cp_pop'], label='Current Policies', color=colors["death"], linestyle='-')
    ax.plot(df_country['year'], df_country['cp_nopop'], label='', color=colors["death"], linestyle='--')
    
    # Plot Net Zero scenarios with and without population
    ax.plot(df_country['year'], df_country['nz_pop'], label='Net Zero*', color=colors["benefit"], linestyle='-')
    ax.plot(df_country['year'], df_country['nz_nopop'], label='', color=colors["benefit"], linestyle='--')
    
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    # Customize the x-axis to show ticks every 5 years
    plt.xticks([str(year) for year in range(2030, 2051, 10)])
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_global, 'Global', 'upper left', ylabel='μg/m3')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_germany, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_indonesia, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_india, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_turkeye, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_vietnam, 'Vietnam', 'upper left')

# Main title
fig.suptitle('PM 2.5 Concentration Levels', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.92, 'Polluction levels are estimated based on NGFS GCAM6 model projections', ha='center', fontsize=12)
fig.text(0.5, 0.88, 'Solid lines are population weighted averages of 1 x 1 km grid values; dashed lines are simple arithmetic averages', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.75, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()








