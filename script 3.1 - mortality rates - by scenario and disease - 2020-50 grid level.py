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
# LOAD CONCENTRATION DATA
df_concentration_cp_total = pd.read_excel('2 - output/script 2.1 - air pollution concentration levels - by scenario/2.5 - annual concentration levels - current policy - total fossil.xlsx')
df_concentration_nz_total = pd.read_excel('2 - output/script 2.1 - air pollution concentration levels - by scenario/3.5 - annual concentration levels - netzero 1.5C 50% adjsuted - total fossil.xlsx')


# --------------
# LOAD EXPOSURE RESPONSE FUNCTIONS
df_response_stroke = pd.read_csv('1 - input/4 - response functions/pm desease - cvd_stroke.csv')


# --------------
# MORTALITY RATES
# https://vizhub.healthdata.org/gbd-results/
# stroke; tracjeal,bronchus, and lung cancer; diabetes melittus type 2; ischemic heart disease; lower respiratory infections; chronic obstructive pulmonary disease
# death per 100K
df_mortality = pd.read_csv('1 - input/IHME-GBD_2021_DATA-443819b9-1.csv')










# In[4]: SET ANNUAL FUNCTION RESUTLS
#####################################

# --------------
# year columns
year_columns_cp = [f'CP_{year}' for year in range(2024, 2051)]
year_columns_nz = [f'NZ_{year}' for year in range(2024, 2051)]


# --------------
# round concentration values to match response function:
    # values below 10 rounded to 1 decmial place, and 10 & above to zero decimal places
df_concentration_cp_total[year_columns_cp] = df_concentration_cp_total[year_columns_cp].applymap(
    lambda x: round(x, 1) if x < 10 else round(x, 0)
)

# round concentration values to match response function:
    # values below 10 rounded to 1 decmial place, and 10 & above to zero decimal places
df_concentration_nz_total[year_columns_nz] = df_concentration_nz_total[year_columns_nz].applymap(
    lambda x: round(x, 1) if x < 10 else round(x, 0)
)




# --------------
# create response functions to each desease
### CP
# 1 - stroke
df_annual_response_cp_total_stroke = df_concentration_cp_total.copy()
for col in year_columns_cp:
    # For each column in the first DataFrame, map the 'exposure' values in the second DataFrame to 'mean'
    df_annual_response_cp_total_stroke[col] = df_annual_response_cp_total_stroke[col].map(
        df_response_stroke.set_index('exposure')['mean']   # Set 'exposure' as the index in df_response_copd for easier mapping
    )



### NZ
# 1 - stroke
df_annual_response_nz_total_stroke = df_concentration_nz_total.copy()
for col in year_columns_nz:
    # For each column in the first DataFrame, map the 'exposure' values in the second DataFrame to 'mean'
    df_annual_response_nz_total_stroke[col] = df_annual_response_nz_total_stroke[col].map(
        df_response_stroke.set_index('exposure')['mean']   # Set 'exposure' as the index in df_response_copd for easier mapping
    )


del col
del df_response_stroke
del df_concentration_cp_total, df_concentration_nz_total








# In[4]: ESTIMATE SHARE OF DEATH BY DISEASE
#####################################

# --------------
# get growth rates in attibution to disease based on response function
# (R(C) - 1)/R(C)
### CP

# 1 - stroke
df_annual_share_cp_total_stroke = df_annual_response_cp_total_stroke.copy()
df_annual_share_cp_total_stroke[year_columns_cp] = (df_annual_share_cp_total_stroke[year_columns_cp] - 1)/df_annual_share_cp_total_stroke[year_columns_cp]

df_annual_share_change_cp_total_stroke = df_annual_share_cp_total_stroke.copy()
df_annual_share_change_cp_total_stroke[year_columns_cp] = df_annual_share_change_cp_total_stroke[year_columns_cp].pct_change(axis=1) * 100



### NZ
# 1 - stroke
df_annual_share_nz_total_stroke = df_annual_response_nz_total_stroke.copy()
df_annual_share_cp_total_stroke[year_columns_nz] = (df_annual_share_nz_total_stroke[year_columns_nz] - 1)/df_annual_share_nz_total_stroke[year_columns_nz]

df_annual_share_change_nz_total_stroke = df_annual_share_nz_total_stroke.copy()
df_annual_share_change_nz_total_stroke[year_columns_nz] = df_annual_share_change_nz_total_stroke[year_columns_nz].pct_change(axis=1) * 100





# --------------
# get mortality rates by year
df_annual_mortalityrate_cp_total_stroke = df_annual_share_change_cp_total_stroke.copy()
df_annual_mortalityrate_nz_total_stroke = df_annual_share_change_nz_total_stroke.copy()


disease_data_cp = {'Stroke': df_annual_mortalityrate_cp_total_stroke}
disease_data_nz = {'Stroke': df_annual_mortalityrate_nz_total_stroke}



### CP
# Loop through each disease
for disease, df_disease_cp in disease_data_cp.items():
    # Set the initial mortality value based on the 'cause_name' in df_mortality
    initial_value = df_mortality.loc[df_mortality['cause_name'] == disease, 'val'].values[0]
    
    # Set the base year (CP_2024) for each disease
    df_disease_cp['CP_2024'] = initial_value
    
    # Get annual mortality rates based on growth rate in disease attribution
    for column in year_columns_cp[1:]:  # Start from 2025 since 2024 is the base year
        df_disease_cp[column] = (
            df_disease_cp[year_columns_cp[year_columns_cp.index(column) - 1]] *  # Previous year's values
            (1 + df_disease_cp[column] / 100)  # Growth rate in the current column
        )


### NZ

# Loop through each disease
for disease, df_disease_nz in disease_data_nz.items():
    # Set the initial mortality value based on the 'cause_name' in df_mortality
    initial_value = df_mortality.loc[df_mortality['cause_name'] == disease, 'val'].values[0]
    
    # Set the base year (CP_2024) for each disease
    df_disease_nz['NZ_2024'] = initial_value
    
    # Get annual mortality rates based on growth rate in disease attribution
    for column in year_columns_nz[1:]:  # Start from 2025 since 2024 is the base year
        df_disease_nz[column] = (
            df_disease_nz[year_columns_nz[year_columns_nz.index(column) - 1]] *  # Previous year's values
            (1 + df_disease_nz[column] / 100)  # Growth rate in the current column
        )


del disease, df_disease_cp, df_disease_nz, disease_data_cp, disease_data_nz, initial_value, column
del df_mortality










# In[]

# export data

# --------------
# response function - annual result
df_annual_response_cp_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/1.1.1 - annual response function - current policy - stroke.xlsx', index = False)
df_annual_response_nz_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/1.2.1 - annual response function - NZ 1.5C 50% - stroke.xlsx', index = False)


# share attibution - annual result
df_annual_share_cp_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/2.1.1 - annual share attribution - current policy - stroke.xlsx', index = False)
df_annual_share_nz_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/2.2.1 - annual share attribution - NZ 1.5C 50% - stroke.xlsx', index = False)


# share attibution - annual change
df_annual_share_change_cp_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/3.1.1 - annual share attribution change - current policy - stroke.xlsx', index = False)
df_annual_share_change_nz_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/3.2.1 - annual share attribution change - NZ 1.5C 50% - stroke.xlsx', index = False)


# mortality rate - annual result
df_annual_mortalityrate_cp_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/4.1.1 - annual mortality rate - current policy - stroke.xlsx', index = False)
df_annual_mortalityrate_nz_total_stroke.to_excel('2 - output/script 3.1 - mortality rates - by scenario and disease - 2020-50 grid level/4.2.1 - annual mortality rate - NZ 1.5C 50% - stroke.xlsx', index = False)










