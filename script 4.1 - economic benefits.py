# In[1]:
# Date: Sep 2, 2024
# Project: Identify mortality rates based on response function to PM levels and share of mortality attibuted to PM
# Author: Farhad Panahov










# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
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


# --------------
# MORTALITY DATA
df_annual_mortality_cp_total_deu = pd.read_excel('2 - output/script 3.2.1 - mortality - by scenario and disease - 2020-50 annual - germany/5.1.1 - annual mortality - current policy.xlsx')
df_annual_mortality_cp_total_idn = pd.read_excel('2 - output/script 3.2.2 - mortality - by scenario and disease - 2020-50 annual - indonesia/5.1.1 - annual mortality - current policy.xlsx')
df_annual_mortality_cp_total_ind = pd.read_excel('2 - output/script 3.2.3 - mortality - by scenario and disease - 2020-50 annual - india/5.1.1 - annual mortality - current policy.xlsx')
df_annual_mortality_cp_total_tur = pd.read_excel('2 - output/script 3.2.4 - mortality - by scenario and disease - 2020-50 annual - turkeye/5.1.1 - annual mortality - current policy.xlsx')
df_annual_mortality_cp_total_usa = pd.read_excel('2 - output/script 3.2.5 - mortality - by scenario and disease - 2020-50 annual - usa/5.1.1 - annual mortality - current policy.xlsx')
df_annual_mortality_cp_total_vnm = pd.read_excel('2 - output/script 3.2.6 - mortality - by scenario and disease - 2020-50 annual - vietnam/5.1.1 - annual mortality - current policy.xlsx')
df_annual_mortality_cp_total_glb = pd.read_excel('2 - output/script 3.2.0 - mortality - by scenario and disease - 2020-50 annual - global/5.1.1 - annual mortality - current policy.xlsx')


df_annual_mortality_nz_total_deu = pd.read_excel('2 - output/script 3.2.1 - mortality - by scenario and disease - 2020-50 annual - germany/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_idn = pd.read_excel('2 - output/script 3.2.2 - mortality - by scenario and disease - 2020-50 annual - indonesia/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_ind = pd.read_excel('2 - output/script 3.2.3 - mortality - by scenario and disease - 2020-50 annual - india/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_tur = pd.read_excel('2 - output/script 3.2.4 - mortality - by scenario and disease - 2020-50 annual - turkeye/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_usa = pd.read_excel('2 - output/script 3.2.5 - mortality - by scenario and disease - 2020-50 annual - usa/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_vnm = pd.read_excel('2 - output/script 3.2.6 - mortality - by scenario and disease - 2020-50 annual - vietnam/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_glb = pd.read_excel('2 - output/script 3.2.0 - mortality - by scenario and disease - 2020-50 annual - global/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')


# --------------
# ECONOMIC DATA
#df_inflation = pd.read_excel('1 - input/5 - econ data/inflation - annual change.xlsx', skiprows = 3)
#df_gdpcapita = pd.read_csv('1 - input/5 - econ data/gdp per capita ppp - WB.csv', skiprows = 4)
df_vsl = pd.read_excel('1 - input/5 - econ data/1-Age-adjusted and age-invariant VSL.xlsx', skiprows = 3)


# --------------
# GLOBAL POPULATION DATA
df_population = pd.read_excel('1 - input/3 - population/wb - global population.xlsx', skiprows = 4)





# In[4]: SET ANNUAL VSL
# #####################################

# # --------------
# this is 2019 $
df_vsl['Age-invariant VSL-Mean'].describe()

# count    2.040000e+02
# mean     1.445539e+06
# std      1.559110e+06
# min      2.213960e+03
# 25%      2.209735e+05
# 50%      7.842381e+05
# 75%      2.495280e+06
# max      8.139747e+06
# Name: Age-invariant VSL-Mean, dtype: float64


# get global weighted VSL by population
df_vsl_population = df_vsl.copy()
df_vsl_population = df_vsl_population.merge(
    df_population[['Country Code', 2019]], 
    left_on='Country - iso3c', 
    right_on='Country Code', 
    how='left'
)

vsl_weighted_average = (df_vsl_population['Age-invariant VSL-Mean'] * df_vsl_population[2019]).sum() / df_vsl_population[2019].sum()


# add median value as global value
vsl_global_row = pd.DataFrame({'Country - iso3c': ['GLB'], 'Age-invariant VSL-Mean': [vsl_weighted_average]})
df_vsl = pd.concat([df_vsl, vsl_global_row], ignore_index=True)


# delete
del vsl_global_row, vsl_weighted_average, df_vsl_population, df_population








# In[4]: GET TOTAL BENEFIT
#####################################

# country names & ilness for loop
country_codes = ['deu', 'idn', 'ind', 'tur', 'usa', 'vnm', 'glb']
columns_to_sum = ['ihd', 'copd', 'lri', 'lung', 'stroke']

# variable 
discount_rate = 1.028 # 2.8%
code = country_codes[1]
# loop through each country 
for code in country_codes:
    
    # get VSL for the country
    vsl = df_vsl.loc[df_vsl['Country - iso3c'] == code.upper(), 'Age-invariant VSL-Mean']
    
    # empty datafram
    df_temp = pd.DataFrame()
    
    # add years to it
    df_temp['Year'] = list(range(2024, 2051))

    # add total mortality across all diseases --- annual
    df_temp['mortality_cp'] =  globals()[f'df_annual_mortality_cp_total_{code}'][columns_to_sum].sum(axis=1) 
    df_temp['mortality_nz'] = globals()[f'df_annual_mortality_nz_total_{code}'][columns_to_sum].sum(axis=1) 
    
    # create difference CP vs NZ15 50%
    df_temp['diff_annual'] = df_temp['mortality_cp'] - df_temp['mortality_nz']
    df_temp['diff_cumulative'] = df_temp['diff_annual'].cumsum()

    # calculate economic benefit
    df_temp['econ_benefit (mln)'] = df_temp['diff_cumulative'] * vsl.values[0] / 1000000 # in millions
    df_temp['econ_benefit_discounted (mln)'] = df_temp['econ_benefit (mln)'] / (discount_rate ** df_temp.index)

    # assign this toa respective country
    globals()[f'df_econbenefit_{code}'] = df_temp


# delete
del vsl, df_temp, code, columns_to_sum, country_codes










# In[4]: GET OVERALL TABLE
#####################################

# Example list of country names
countries = ['Global', 'Germany', 'Indonesia', 'India', 'Turkiye', 'USA', 'Vietnam']

# List to store country DataFrames (this is just an example; replace with your actual DataFrames)
country_dfs = [df_econbenefit_glb, df_econbenefit_deu, df_econbenefit_idn, df_econbenefit_ind,
               df_econbenefit_tur, df_econbenefit_usa, df_econbenefit_vnm]  # Replace df1, df2, etc., with your actual DataFrames

# Initialize an empty list to collect the data
temp_data_benefit = []
temp_data_death = []

# Iterate over each country DataFrame
for country_name, df in zip(countries, country_dfs):
    # Extract values for the years 2035 and 2050 --- BENEFIT
    value_2035_benefit = df.loc[df['Year'] == 2035, 'econ_benefit_discounted (mln)'].values[0]  # Replace 'value_column_name' with the column name you want
    value_2050_benefit = df.loc[df['Year'] == 2050, 'econ_benefit_discounted (mln)'].values[0]  # Replace 'value_column_name' with the column name you want
    
    # Extract values for the years 2035 and 2050 --- DEATH
    value_2035_death = df.loc[df['Year'] == 2035, 'diff_cumulative'].values[0]  # Replace 'value_column_name' with the column name you want
    value_2050_death = df.loc[df['Year'] == 2050, 'diff_cumulative'].values[0]  # Replace 'value_column_name' with the column name you want
    
    # Append the data as a dictionary
    temp_data_benefit.append({'Country': country_name, 'Cumulative economic benefit (mln $2019): 2035': value_2035_benefit, 'Cumulative economic benefit (mln $2019): 2050': value_2050_benefit})
    temp_data_death.append({'Country': country_name, 'Cumulative avoided death: 2035': value_2035_death, 'Cumulative avoided death: 2050': value_2050_death})

# Create a new DataFrame with the collected data
df_benefit = pd.DataFrame(temp_data_benefit)
df_death = pd.DataFrame(temp_data_death)


# delete
del temp_data_benefit, temp_data_death, countries, country_dfs, value_2035_benefit, value_2050_benefit, value_2035_death, value_2050_death






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





# In[4]: PLOTS
#####################################


# --------------
# TOTAL DEATHS

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
    ax.plot(df_country['Year'], df_country['diff_cumulative'], label='Cumulative avoided deaths', color=colors["death"])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_econbenefit_glb, 'Global', 'upper left', ylabel='Thousands of deaths')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_econbenefit_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_econbenefit_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_econbenefit_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_econbenefit_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_econbenefit_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_econbenefit_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Cumulative Avoided Deaths from Improved Air Pollution:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.87, 'Avoided deaths are difference in total mortalities between the scenarios due to \n PM2.5 concentration improvement as fossil fuels are phased out', ha='center', fontsize=12)
fig.text(0.5, 0.81, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes

# Move the charts lower
plt.subplots_adjust(top=0.73, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()




# --------------
# Annual DEATHS

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
    ax.plot(df_country['Year'], df_country['diff_annual'], label='Cumulative avoided deaths', color=colors["death"])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_econbenefit_glb, 'Global', 'upper left', ylabel='Thousands of deaths')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_econbenefit_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_econbenefit_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_econbenefit_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_econbenefit_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_econbenefit_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_econbenefit_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Annaul Avoided Deaths from Improved Air Pollution:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.87, 'Avoided deaths are difference in total mortalities between the scenarios due to \n PM2.5 concentration improvement as fossil fuels are phased out', ha='center', fontsize=12)
fig.text(0.5, 0.81, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes

# Move the charts lower
plt.subplots_adjust(top=0.73, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()







# --------------
# BENEFITS

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
    ax.plot(df_country['Year'], df_country['econ_benefit_discounted (mln)'], label='Cumulative avoided deaths', color=colors["benefit"])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_econbenefit_glb, 'Global', 'upper left', ylabel='Billions of 2019 US$')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_econbenefit_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_econbenefit_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_econbenefit_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_econbenefit_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_econbenefit_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_econbenefit_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Cumulative Economic Benefits from Avoided Deaths due to Improved Air Pollution:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.87, 'Avoided deaths are difference in total mortalities between the scenarios due to PM2.5 concentration improvement \n as fossil fuels are phased out. Economic befenits is the Value of a Statistical Life', ha='center', fontsize=12)
fig.text(0.5, 0.81, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes

# Move the charts lower
plt.subplots_adjust(top=0.73, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()










# In[]

# export data

# --------------
# response function - annual result
df_econbenefit_deu.to_excel('2 - output/script 4.1 - economic benefit/1.1 - econ benefit - germany.xlsx', index = False)
df_econbenefit_idn.to_excel('2 - output/script 4.1 - economic benefit/1.2 - econ benefit - indonesia.xlsx', index = False)
df_econbenefit_ind.to_excel('2 - output/script 4.1 - economic benefit/1.3 - econ benefit - india.xlsx', index = False)
df_econbenefit_tur.to_excel('2 - output/script 4.1 - economic benefit/1.4 - econ benefit - turkeye.xlsx', index = False)
df_econbenefit_usa.to_excel('2 - output/script 4.1 - economic benefit/1.5 - econ benefit - usa.xlsx', index = False)
df_econbenefit_vnm.to_excel('2 - output/script 4.1 - economic benefit/1.6 - econ benefit - vietnam.xlsx', index = False)
df_econbenefit_glb.to_excel('2 - output/script 4.1 - economic benefit/1.7 - econ benefit - global.xlsx', index = False)

# --------------
# overall table
df_benefit.to_excel('2 - output/script 4.1 - economic benefit/2.1 - econ benefit - table.xlsx', index = False)
df_death.to_excel('2 - output/script 4.1 - economic benefit/2.2 - avoided death - table.xlsx', index = False)





