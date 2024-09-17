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
import seaborn as sns










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


df_annual_mortality_nz_total_deu = pd.read_excel('2 - output/script 3.2.1 - mortality - by scenario and disease - 2020-50 annual - germany/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_idn = pd.read_excel('2 - output/script 3.2.2 - mortality - by scenario and disease - 2020-50 annual - indonesia/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_ind = pd.read_excel('2 - output/script 3.2.3 - mortality - by scenario and disease - 2020-50 annual - india/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_tur = pd.read_excel('2 - output/script 3.2.4 - mortality - by scenario and disease - 2020-50 annual - turkeye/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_usa = pd.read_excel('2 - output/script 3.2.5 - mortality - by scenario and disease - 2020-50 annual - usa/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')
df_annual_mortality_nz_total_vnm = pd.read_excel('2 - output/script 3.2.6 - mortality - by scenario and disease - 2020-50 annual - vietnam/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx')


# --------------
# INFLATION DATA
df_inflation = pd.read_excel('1 - input/5 - econ data/inflation - annual change.xlsx', skiprows = 3)










# In[4]: SET ANNUAL VSL
#####################################

# --------------
# 2005 VSL
vsl = 3.83

# years
years_inflation = [str(year) for year in range(2005, 2024)]

# inflation --- OECD
df_inflation = df_inflation[df_inflation['Country Name'] == 'OECD members']
df_inflation['compounded_value'] = vsl * (df_inflation[years_inflation].div(100).add(1).prod(axis=1))

# get the final value
vsl_2024 = df_inflation['compounded_value'].values[0]

# delete
del vsl, df_inflation, years_inflation









# In[4]: GET TOTAL BENEFIT
#####################################

# country names & ilness for loop
country_codes = ['deu', 'idn', 'ind', 'tur', 'usa', 'vnm']
columns_to_sum = ['ihd', 'copd', 'lri', 'lung', 'stroke']

# variable 
discount_rate = 1.028 # 2.8%


# loop through each country 
for code in country_codes:
    
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
    df_temp['econ_benefit'] = df_temp['diff_cumulative'] * vsl_2024 / 1000
    df_temp['econ_benefit_discounted'] = df_temp['econ_benefit'] / (discount_rate ** df_temp.index)

    # assign this toa respective country
    globals()[f'df_econbenefit_{code}'] = df_temp










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

# chart theme
sns.set_theme(style="ticks")


# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt





# --------------
# 1.1 GERMANY
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_econbenefit_deu['Year'], df_econbenefit_deu['diff_cumulative'], label='Cumulative avoided deaths (LHS)', color = "Green")
ax1.set_ylabel('Thousands of deaths', fontsize=15)
ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_econbenefit_deu['Year'], df_econbenefit_deu['econ_benefit_discounted'], label='Economic benefit (RHS)', color = "Blue")
ax2.set_ylabel('Billion US$ (discounted)', fontsize=15)


# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided death from improved air pollution and economic benefits in Germany: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 1.2 INDONESIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_econbenefit_idn['Year'], df_econbenefit_idn['diff_cumulative'], label='Cumulative avoided deaths (LHS)', color = "Green")
ax1.set_ylabel('Thousands of deaths', fontsize=15)
ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_econbenefit_idn['Year'], df_econbenefit_idn['econ_benefit_discounted'], label='Economic benefit (RHS)', color = "Blue")
ax2.set_ylabel('Billion US$ (discounted)', fontsize=15)


# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided death from improved air pollution and economic benefits in Indonesia: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 1.3 INDIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_econbenefit_ind['Year'], df_econbenefit_ind['diff_cumulative'], label='Cumulative avoided deaths (LHS)', color = "Green")
ax1.set_ylabel('Thousands of deaths', fontsize=15)
ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_econbenefit_ind['Year'], df_econbenefit_ind['econ_benefit_discounted'], label='Economic benefit (RHS)', color = "Blue")
ax2.set_ylabel('Billion US$ (discounted)', fontsize=15)


# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided death from improved air pollution and economic benefits in India: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 1.4 TURKEYE
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_econbenefit_tur['Year'], df_econbenefit_tur['diff_cumulative'], label='Cumulative avoided deaths (LHS)', color = "Green")
ax1.set_ylabel('Thousands of deaths', fontsize=15)
ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_econbenefit_tur['Year'], df_econbenefit_tur['econ_benefit_discounted'], label='Economic benefit (RHS)', color = "Blue")
ax2.set_ylabel('Billion US$ (discounted)', fontsize=15)


# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided death from improved air pollution and economic benefits in Turkeye: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()






# --------------
# 1.5 USA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_econbenefit_usa['Year'], df_econbenefit_usa['diff_cumulative'], label='Cumulative avoided deaths (LHS)', color = "Green")
ax1.set_ylabel('Thousands of deaths', fontsize=15)
ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_econbenefit_usa['Year'], df_econbenefit_usa['econ_benefit_discounted'], label='Economic benefit (RHS)', color = "Blue")
ax2.set_ylabel('Billion US$ (discounted)', fontsize=15)


# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided death from improved air pollution and economic benefits in USA: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()






# --------------
# 1.6 VIETNAM
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_econbenefit_vnm['Year'], df_econbenefit_vnm['diff_cumulative'], label='Cumulative avoided deaths (LHS)', color = "Green")
ax1.set_ylabel('Thousands of deaths', fontsize=15)
ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_econbenefit_vnm['Year'], df_econbenefit_vnm['econ_benefit_discounted'], label='Economic benefit (RHS)', color = "Blue")
ax2.set_ylabel('Billion US$ (discounted)', fontsize=15)


# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided death from improved air pollution and economic benefits in Vietnam: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

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







