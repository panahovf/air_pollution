# In[1]:
# Date: Sep 27, 2024
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
df_concentration_cp = pd.read_excel('2 - output/script 2.1.3 - air pollition concentration levels - by scenario - devunfccc/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_nz = pd.read_excel('2 - output/script 2.1.3 - air pollition concentration levels - by scenario - devunfccc/1.2 - annual concentration levels - netzero 1.5C 50% adjsuted.xlsx')


# --------------
# LOAD EXPOSURE RESPONSE FUNCTIONS
df_response_ihd = pd.read_csv('1 - input/4 - response functions/pm desease - cvd_ihd.csv')
df_response_stroke = pd.read_csv('1 - input/4 - response functions/pm desease - cvd_stroke.csv')
df_response_lri = pd.read_csv('1 - input/4 - response functions/pm desease - lri.csv')
df_response_lung = pd.read_csv('1 - input/4 - response functions/pm desease - neo_lung.csv')
df_response_copd = pd.read_csv('1 - input/4 - response functions/pm desease - resp_copd.csv')
df_response_t2d = pd.read_csv('1 - input/4 - response functions/pm desease - t2_dm.csv')


# --------------
# MORTALITY RATES
# https://vizhub.healthdata.org/gbd-results/
# stroke; tracjeal,bronchus, and lung cancer; diabetes melittus type 2; ischemic heart disease; lower respiratory infections; chronic obstructive pulmonary disease
# death per 100K
df_mortality = pd.read_excel('1 - input/mortality rates - by country.xlsx')


# --------------
# POPULATION PROJECTION
# world bank: https://databank.worldbank.org/source/population-estimates-and-projections#
df_pop_project = pd.read_excel('1 - input/3 - population/wb - population project - by country.xlsx')



# In[4]: CALCULATE EMDE MORTALITY RATES
########################################

# --------------
# Get list of EMDE countries

# load datasets
temp_directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\1 - input\Country Datasets'
df_country_developing = pd.read_excel(temp_directory + r'\UNFCCC classification.xlsx')
df_country_developing = df_country_developing[df_country_developing["classification"] == "Developing"]

# get and combine lists
v_countrycodes_developing = list(df_country_developing['iso_3'].unique())

# delete
del temp_directory, df_country_developing



# --------------
# Merge and get weighted average mortality rates

# filter population for EMDE
temp_population = df_pop_project.rename(columns={'Country Name': 'Location', '2024 [YR2024]': 'Population_2024'})
temp_population = temp_population[temp_population['Country Code'].isin(v_countrycodes_developing)] # filter population for EMDE


# merge with mortality
df_mortality = pd.merge(df_mortality, temp_population[['Location', 'Population_2024']], on='Location', how='inner')
df_mortality['Population_2024'] = pd.to_numeric(df_mortality['Population_2024'], errors='coerce')


# --------------
# Calculate the weighted average mortality rate for each disease
# Weighted average formula: (sum of rate * population) / sum of population
df_mortality = df_mortality.groupby('Cause').apply(
    lambda x: (x['Value'] * x['Population_2024']).sum() / x['Population_2024'].sum()
).reset_index(name='lower')



# delete
del  temp_population










# In[4]: SET ANNUAL FUNCTION RESUTLS
#####################################

# --------------
### CP
# round concentration values to match response function:
    # values below 10 rounded to 1 decmial place, and 10 & above to zero decimal places
df_concentration_cp[['power_coal', 'power_oilgas',
                           'total_fossil']] = df_concentration_cp[['power_coal', 'power_oilgas',
                                                      'total_fossil']].applymap(
    lambda x: round(x, 1) if x < 10 else round(x, 0)
)
                                                          
      
                                                          
### NZ
# round concentration values to match response function:
    # values below 10 rounded to 1 decmial place, and 10 & above to zero decimal places
df_concentration_nz[['power_coal', 'power_oilgas',
                           'total_fossil']] = df_concentration_nz[['power_coal', 'power_oilgas',
                                                      'total_fossil']].applymap(
    lambda x: round(x, 1) if x < 10 else round(x, 0)
)


                                                          
# --------------
# create response functions to each desease
### CP
df_annual_response_cp_total = df_concentration_cp.copy()


# df_annual_response_cp_total
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_ihd[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_copd[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_lri[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')

df_annual_response_cp_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)   ### this step just renames columns, otherwise you get an error
df_annual_response_cp_total.rename(columns={'lower_x': 'ihd', 'lower_y': 'copd', 'lower': 'lri'}, inplace=True)


df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_lung[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_stroke[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_t2d[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')

df_annual_response_cp_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_cp_total.rename(columns={'lower_x': 'lung', 'lower_y': 'stroke', 'lower': 't2d'}, inplace=True)





### NZ
df_annual_response_nz_total = df_concentration_nz.copy()


# df_annual_response_cp_total
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_ihd[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_copd[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_lri[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')

df_annual_response_nz_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)   ### this step just renames columns, otherwise you get an error
df_annual_response_nz_total.rename(columns={'lower_x': 'ihd', 'lower_y': 'copd', 'lower': 'lri'}, inplace=True)


df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_lung[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_stroke[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_t2d[['exposure', 'lower']], left_on='total_fossil', right_on='exposure', how='left')

df_annual_response_nz_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_nz_total.rename(columns={'lower_x': 'lung', 'lower_y': 'stroke', 'lower': 't2d'}, inplace=True)



# delete
del df_concentration_cp, df_concentration_nz










# In[4]: ESTIMATE SHARE OF DEATH BY DISEASE
#####################################

# --------------
# get growth rates in attibution to disease based on response function
# (R(C) - 1)/R(C)
list_of_columns = df_annual_response_cp_total.columns.drop(['Year', 'power_coal',
                                                            'power_oilgas','total_fossil']).tolist()


# --------------
### CP
df_annual_share_cp_total = df_annual_response_cp_total.copy()
df_annual_share_cp_total[list_of_columns] = (df_annual_share_cp_total[list_of_columns] - 1)/df_annual_share_cp_total[list_of_columns]

df_annual_share_change_cp_total = df_annual_share_cp_total.copy()
df_annual_share_change_cp_total[list_of_columns] = df_annual_share_change_cp_total[list_of_columns].pct_change(axis=0) * 100


### NZ
df_annual_share_nz_total = df_annual_response_nz_total.copy()
df_annual_share_nz_total[list_of_columns] = (df_annual_share_nz_total[list_of_columns] - 1)/df_annual_share_nz_total[list_of_columns]

df_annual_share_change_nz_total = df_annual_share_nz_total.copy()
df_annual_share_change_nz_total[list_of_columns] = df_annual_share_change_nz_total[list_of_columns].pct_change(axis=0) * 100


# BOTH
# get mortality rates by year
df_annual_mortalityrate_cp_total = df_annual_share_change_cp_total.copy()
df_annual_mortalityrate_nz_total = df_annual_share_change_nz_total.copy()


# set initial value as starting point for each disease
temp = df_mortality.loc[df_mortality['Cause'] == 'Ischemic heart disease', 'lower'].values[0]
df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Year'] == 2024, 'ihd'] = temp
df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Year'] == 2024, 'ihd'] = temp

temp = df_mortality.loc[df_mortality['Cause'] == 'Lower respiratory infections', 'lower'].values[0]
df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Year'] == 2024, 'lri'] = temp
df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Year'] == 2024, 'lri'] = temp

temp = df_mortality.loc[df_mortality['Cause'] == 'Chronic obstructive pulmonary disease', 'lower'].values[0]
df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Year'] == 2024, 'copd'] = temp
df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Year'] == 2024, 'copd'] = temp

temp = df_mortality.loc[df_mortality['Cause'] == 'Tracheal, bronchus, and lung cancer', 'lower'].values[0]
df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Year'] == 2024, 'lung'] = temp
df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Year'] == 2024, 'lung'] = temp

temp = df_mortality.loc[df_mortality['Cause'] == 'Stroke', 'lower'].values[0]
df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Year'] == 2024, 'stroke'] = temp
df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Year'] == 2024, 'stroke'] = temp

temp = df_mortality.loc[df_mortality['Cause'] == 'Diabetes mellitus type 2', 'lower'].values[0]
df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Year'] == 2024, 't2d'] = temp
df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Year'] == 2024, 't2d'] = temp


### CP
# get annual mortality rates based on growth rate in disease attribution
for column in df_annual_mortalityrate_cp_total.columns[7:]:
    # Start from 2025 since 2024 is the base year
    for i in range(1, len(df_annual_mortalityrate_cp_total)):
        df_annual_mortalityrate_cp_total.loc[i, column] = df_annual_mortalityrate_cp_total.loc[i - 1, column] * (1 + df_annual_mortalityrate_cp_total.loc[i, column] / 100)


### NZ
# get annual mortality rates based on growth rate in disease attribution
for column in df_annual_mortalityrate_nz_total.columns[7:]:
    # Start from 2025 since 2024 is the base year
    for i in range(1, len(df_annual_mortalityrate_nz_total)):
        df_annual_mortalityrate_nz_total.loc[i, column] = df_annual_mortalityrate_nz_total.loc[i - 1, column] * (1 + df_annual_mortalityrate_nz_total.loc[i, column] / 100)


# delete
del column, i, temp
del df_response_copd, df_response_ihd, df_response_lri, df_response_lung, df_response_stroke, df_response_t2d
del df_mortality










# In[4]: NOW GET ABSOLUTE NUMBER OF DEATH BY DISEASE
#####################################

# --------------
# Filter population
df_pop_project = df_pop_project[df_pop_project['Country Code'].isin(v_countrycodes_developing)]


# --------------
# Calculate the sum of population for all years for each country
columns_to_sum = [col for col in df_pop_project.columns if '[YR20' in col]
df_pop_project = df_pop_project[columns_to_sum].sum().reset_index()
df_pop_project.columns = ['Year', 'Population']


# --------------
# Transpose and clean population data
df_pop_project['Year'] = df_pop_project['Year'].str.slice(0, 4).astype(int)
df_pop_project['100K population'] = df_pop_project['Population'] / 100000


# --------------
# now get absolute death rates by year by disease
# create dataframes
df_annual_mortality_cp_total = df_annual_mortalityrate_cp_total.copy()
df_annual_mortality_nz_total = df_annual_mortalityrate_nz_total.copy()


# multiple death per 100K to population values (1ooK count)
df_annual_mortality_cp_total = pd.merge(df_annual_mortality_cp_total, df_pop_project[['Year', '100K population']], on='Year', how='left')   # merge to make it easier to multiply rates to population
df_annual_mortality_cp_total[list_of_columns] = df_annual_mortality_cp_total[list_of_columns].multiply(df_annual_mortality_cp_total['100K population'], axis=0)   # multiply rates per 100K to 100K population count

df_annual_mortality_nz_total = pd.merge(df_annual_mortality_nz_total, df_pop_project[['Year', '100K population']], on='Year', how='left')   # merge to make it easier to multiply rates to population
df_annual_mortality_nz_total[list_of_columns] = df_annual_mortality_nz_total[list_of_columns].multiply(df_annual_mortality_nz_total['100K population'], axis=0)   # multiply rates per 100K to 100K population count


# --------------
# mortality without population growth
df_annual_mortality_cp_total_nopopgrowth = df_annual_mortalityrate_cp_total.copy()
df_annual_mortality_nz_total_nopopgrowth = df_annual_mortalityrate_nz_total.copy()

# current population estimate
val_population_2024 = df_pop_project.loc[df_pop_project['Year'] == 2024, '100K population'].values[0]

# multiple death per 100K to population values (1ooK count)
df_annual_mortality_cp_total_nopopgrowth[list_of_columns] = df_annual_mortality_cp_total_nopopgrowth[list_of_columns].multiply(val_population_2024, axis=0)   # multiply rates per 100K to 100K population count
df_annual_mortality_nz_total_nopopgrowth[list_of_columns] = df_annual_mortality_nz_total_nopopgrowth[list_of_columns].multiply(val_population_2024, axis=0)   # multiply rates per 100K to 100K population count







# In[]

# export data

# --------------
# response function - annual result
df_annual_response_cp_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/1.1.1 - annual response function - current policy.xlsx', index = False)
df_annual_response_nz_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/1.2.1 - annual response function - NZ 1.5C 50%.xlsx', index = False)


# share attibution - annual result
df_annual_share_cp_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/2.1.1 - annual share attribution - current policy.xlsx', index = False)
df_annual_share_nz_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/2.2.1 - annual share attribution - NZ 1.5C 50%.xlsx', index = False)


# share attibution - annual change
df_annual_share_change_cp_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/3.1.1 - annual share attribution change - current policy.xlsx', index = False)
df_annual_share_change_nz_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/3.2.1 - annual share attribution change - NZ 1.5C 50%.xlsx', index = False)


# mortality rate - annual result
df_annual_mortalityrate_cp_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/4.1.1 - annual mortality rate - current policy.xlsx', index = False)
df_annual_mortalityrate_nz_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/4.2.1 - annual mortality rate - NZ 1.5C 50%.xlsx', index = False)


# mortality - annual result
df_annual_mortality_cp_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/5.1.1 - annual mortality - current policy.xlsx', index = False)
df_annual_mortality_nz_total.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/5.2.1 - annual mortality - NZ 1.5C 50%.xlsx', index = False)


# mortality - annual result - no population growth
df_annual_mortality_cp_total_nopopgrowth.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/6.1.1 - annual mortality - no pop growth - current policy.xlsx', index = False)
df_annual_mortality_nz_total_nopopgrowth.to_excel('2 - output/script 3.2.15 - mortality - by scenario and disease - 2020-50 annual - devunfccc/6.2.1 - annual mortality - no pop growth - NZ 1.5C 50%.xlsx', index = False)









