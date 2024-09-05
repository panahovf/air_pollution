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
df_concentration_cp = pd.read_excel('2 - output/script 1.1/1.1 - annual concentration levels - current policy.xlsx')
df_concentration_nz = pd.read_excel('2 - output/script 1.1/1.2 - annual concentration levels - netzero 1.5C 67% adjsuted.xlsx')


# --------------
# LOAD EXPOSURE RESPONSE FUNCTIONS
df_response_ihd = pd.read_csv('1 - input/pm desease - cvd_ihd.csv')
df_response_stroke = pd.read_csv('1 - input/pm desease - cvd_stroke.csv')
df_response_lri = pd.read_csv('1 - input/pm desease - lri.csv')
df_response_lung = pd.read_csv('1 - input/pm desease - neo_lung.csv')
df_response_copd = pd.read_csv('1 - input/pm desease - resp_copd.csv')
df_response_t2d = pd.read_csv('1 - input/pm desease - t2_dm.csv')


# --------------
# MORTALITY RATES
# https://vizhub.healthdata.org/gbd-results/
# stroke; tracjeal,bronchus, and lung cancer; diabetes melittus type 2; ischemic heart disease; lower respiratory infections; chronic obstructive pulmonary disease
# death per 100K
df_mortality = pd.read_csv('1 - input/IHME-GBD_2021_DATA-443819b9-1.csv')


# --------------
# POPULATION PROJECTION
# world bank: https://databank.worldbank.org/source/population-estimates-and-projections#
df_pop_project = pd.read_csv('1 - input/population projection - WB.csv')










# In[4]: SET ANNUAL FUNCTION RESUTLS
#####################################

# --------------
# round concentration values to match response function
df_concentration_cp['Concentration_level'] = df_concentration_cp['Concentration_level'].apply(
    lambda x: round(x, 1) if x < 10 else round(x, 0)
)

df_concentration_nz['Concentration_level'] = df_concentration_nz['Concentration_level'].apply(
    lambda x: round(x, 1) if x < 10 else round(x, 0)
)


# --------------
# create response functions to each desease
### NZ
df_annual_response_nz = df_concentration_nz.copy()
df_annual_response_nz = pd.merge(df_annual_response_nz, df_response_ihd[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_nz = pd.merge(df_annual_response_nz, df_response_copd[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_nz = pd.merge(df_annual_response_nz, df_response_lri[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')

df_annual_response_nz.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_nz.rename(columns={'mean_x': 'ihd', 'mean_y': 'copd', 'mean': 'lri'}, inplace=True)

df_annual_response_nz = pd.merge(df_annual_response_nz, df_response_lung[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_nz = pd.merge(df_annual_response_nz, df_response_stroke[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_nz = pd.merge(df_annual_response_nz, df_response_t2d[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')

df_annual_response_nz.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_nz.rename(columns={'mean_x': 'lung', 'mean_y': 'stroke', 'mean': 't2d'}, inplace=True)


### CP
df_annual_response_cp = df_concentration_cp.copy()
df_annual_response_cp = pd.merge(df_annual_response_cp, df_response_ihd[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_cp = pd.merge(df_annual_response_cp, df_response_copd[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_cp = pd.merge(df_annual_response_cp, df_response_lri[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')

df_annual_response_cp.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_cp.rename(columns={'mean_x': 'ihd', 'mean_y': 'copd', 'mean': 'lri'}, inplace=True)

df_annual_response_cp = pd.merge(df_annual_response_cp, df_response_lung[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_cp = pd.merge(df_annual_response_cp, df_response_stroke[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')
df_annual_response_cp = pd.merge(df_annual_response_cp, df_response_t2d[['exposure', 'mean']], left_on='Concentration_level', right_on='exposure', how='left')

df_annual_response_cp.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_cp.rename(columns={'mean_x': 'lung', 'mean_y': 'stroke', 'mean': 't2d'}, inplace=True)


# delete
del df_response_copd, df_response_ihd, df_response_lri, df_response_lung, df_response_stroke, df_response_t2d










# In[4]: ESTIMATE SHARE OF DEATH BY DISEASE
#####################################

# --------------
# get list of columns
list_of_columns = df_annual_response_nz.columns.drop(['Year', 'Concentration_level']).tolist()


# --------------
# get growth rates in attibution to disease based on response function
# (R(C) - 1)/R(C)
### NZ
df_annual_share_nz = df_annual_response_nz.copy()
df_annual_share_nz[list_of_columns] = (df_annual_share_nz[list_of_columns] - 1)/df_annual_share_nz[list_of_columns]

df_annual_share_nz_change = df_annual_share_nz.copy()
df_annual_share_nz_change[list_of_columns] = df_annual_share_nz_change[list_of_columns].pct_change(axis=0) * 100


# --------------
### CP
df_annual_share_cp = df_annual_response_cp.copy()
df_annual_share_cp[list_of_columns] = (df_annual_share_cp[list_of_columns] - 1)/df_annual_share_cp[list_of_columns]

df_annual_share_cp_change = df_annual_share_cp.copy()
df_annual_share_cp_change[list_of_columns] = df_annual_share_cp_change[list_of_columns].pct_change(axis=0) * 100





# --------------
# get mortality rates by year
### NZ
df_annual_share_nz_change_mortalityrate = df_annual_share_nz_change.copy()

# set initial value as starting point for each disease
temp = df_mortality.loc[df_mortality['cause_name'] == 'Ischemic heart disease', 'val'].values[0]
df_annual_share_nz_change_mortalityrate.loc[df_annual_share_nz_change_mortalityrate['Year'] == 2024, 'ihd'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Lower respiratory infections', 'val'].values[0]
df_annual_share_nz_change_mortalityrate.loc[df_annual_share_nz_change_mortalityrate['Year'] == 2024, 'lri'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Chronic obstructive pulmonary disease', 'val'].values[0]
df_annual_share_nz_change_mortalityrate.loc[df_annual_share_nz_change_mortalityrate['Year'] == 2024, 'copd'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Tracheal, bronchus, and lung cancer', 'val'].values[0]
df_annual_share_nz_change_mortalityrate.loc[df_annual_share_nz_change_mortalityrate['Year'] == 2024, 'lung'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Stroke', 'val'].values[0]
df_annual_share_nz_change_mortalityrate.loc[df_annual_share_nz_change_mortalityrate['Year'] == 2024, 'stroke'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Diabetes mellitus type 2', 'val'].values[0]
df_annual_share_nz_change_mortalityrate.loc[df_annual_share_nz_change_mortalityrate['Year'] == 2024, 't2d'] = temp


# get annual mortality rates based on growth rate in disease attribution
for column in df_annual_share_nz_change_mortalityrate.columns[2:]:
    # Start from 2025 since 2024 is the base year
    for i in range(1, len(df_annual_share_nz_change_mortalityrate)):
        df_annual_share_nz_change_mortalityrate.loc[i, column] = df_annual_share_nz_change_mortalityrate.loc[i - 1, column] * (1 + df_annual_share_nz_change_mortalityrate.loc[i, column] / 100)





### CP
df_annual_share_cp_change_mortalityrate = df_annual_share_cp_change.copy()

# set initial value as starting point for each disease
temp = df_mortality.loc[df_mortality['cause_name'] == 'Ischemic heart disease', 'val'].values[0]
df_annual_share_cp_change_mortalityrate.loc[df_annual_share_cp_change_mortalityrate['Year'] == 2024, 'ihd'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Lower respiratory infections', 'val'].values[0]
df_annual_share_cp_change_mortalityrate.loc[df_annual_share_cp_change_mortalityrate['Year'] == 2024, 'lri'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Chronic obstructive pulmonary disease', 'val'].values[0]
df_annual_share_cp_change_mortalityrate.loc[df_annual_share_cp_change_mortalityrate['Year'] == 2024, 'copd'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Tracheal, bronchus, and lung cancer', 'val'].values[0]
df_annual_share_cp_change_mortalityrate.loc[df_annual_share_cp_change_mortalityrate['Year'] == 2024, 'lung'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Stroke', 'val'].values[0]
df_annual_share_cp_change_mortalityrate.loc[df_annual_share_cp_change_mortalityrate['Year'] == 2024, 'stroke'] = temp

temp = df_mortality.loc[df_mortality['cause_name'] == 'Diabetes mellitus type 2', 'val'].values[0]
df_annual_share_cp_change_mortalityrate.loc[df_annual_share_cp_change_mortalityrate['Year'] == 2024, 't2d'] = temp


# get annual mortality rates based on growth rate in disease attribution
for column in df_annual_share_cp_change_mortalityrate.columns[2:]:
    # Start from 2025 since 2024 is the base year
    for i in range(1, len(df_annual_share_cp_change_mortalityrate)):
        df_annual_share_cp_change_mortalityrate.loc[i, column] = df_annual_share_cp_change_mortalityrate.loc[i - 1, column] * (1 + df_annual_share_cp_change_mortalityrate.loc[i, column] / 100)





# delete
del column, disease, i, temp











# In[4]: NOW GET ABSOLUTE NUMBER OF DEATH BY DISEASE
#####################################

# --------------
# Transpose and clean population data
df_pop_project = df_pop_project.transpose().reset_index()   #transpose
df_pop_project = df_pop_project.drop(df_pop_project.index[0:4])   #remove estra rows
df_pop_project.columns = ['Year', 'Population']   #set names
df_pop_project['Year'] = df_pop_project['Year'].str.slice(0, 4).astype(int) #clean year column
df_pop_project['100K population'] = df_pop_project['Population'] / 100000


# --------------
# now get absolute death rates by year by disease
# create dataframes
df_annual_share_nz_mortality = df_annual_share_nz_change_mortalityrate.copy()
df_annual_share_cp_mortality = df_annual_share_cp_change_mortalityrate.copy()


# multiple death per 100K to population values (1ooK count)
df_annual_share_nz_mortality = pd.merge(df_annual_share_nz_mortality, df_pop_project[['Year', '100K population']], on='Year', how='left')   # merge to make it easier to multiply rates to population
df_annual_share_nz_mortality[list_of_columns] = df_annual_share_nz_mortality[list_of_columns].multiply(df_annual_share_nz_mortality['100K population'], axis=0)   # multiply rates per 100K to 100K population count

df_annual_share_cp_mortality = pd.merge(df_annual_share_cp_mortality, df_pop_project[['Year', '100K population']], on='Year', how='left')   # merge to make it easier to multiply rates to population
df_annual_share_cp_mortality[list_of_columns] = df_annual_share_cp_mortality[list_of_columns].multiply(df_annual_share_cp_mortality['100K population'], axis=0)   # multiply rates per 100K to 100K population count










# In[]

# export data

# --------------
# response function - annual result
df_annual_response_cp.to_excel('2 - output/script 2.1/2.1 - annual response function - current policy.xlsx', index = False)
df_annual_response_nz.to_excel('2 - output/script 2.1/2.2 - annual response function - netzero 1.5C 67% adjsuted.xlsx', index = False)


# response function - annual result - share attibution
df_annual_share_cp.to_excel('2 - output/script 2.1/2.3 - annual response function share attribution - current policy.xlsx', index = False)
df_annual_share_nz.to_excel('2 - output/script 2.1/2.4 - annual response function share attribution - netzero 1.5C 67% adjsuted.xlsx', index = False)


# response function - annual result - share attibution
df_annual_share_cp_change.to_excel('2 - output/script 2.1/2.5 - annual response function share attribution growth rate - current policy.xlsx', index = False)
df_annual_share_nz_change.to_excel('2 - output/script 2.1/2.6 - annual response function share attribution growth rate - netzero 1.5C 67% adjsuted.xlsx', index = False)


# response function - annual result - share attibution
df_annual_share_cp_change_mortalityrate.to_excel('2 - output/script 2.1/2.7 - annual mortality rate - current policy.xlsx', index = False)
df_annual_share_nz_change_mortalityrate.to_excel('2 - output/script 2.1/2.8 - annual mortality rate - netzero 1.5C 67% adjsuted.xlsx', index = False)


# response function - annual result - share attibution
df_annual_share_cp_mortality.to_excel('2 - output/script 2.1/2.9 - annual mortality absolute - current policy.xlsx', index = False)
df_annual_share_nz_mortality.to_excel('2 - output/script 2.1/2.10 - annual mortality absolute - netzero 1.5C 67% adjsuted.xlsx', index = False)











