# In[1]:
# Date: Sep 21, 2024
# Project: Creating global emissions phase-out pathways based on Current Policies and NetZero 1.5C 50% adjusted:
    # Data for Rudy to run global scenario analysis on cloud due to large data files
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




# folder & file path
population_path = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution\1 - input\3 - population\1 - germany\output_excel'
population_files = os.listdir(population_path)
df_population = pd.DataFrame()



# load and combine all population files
for file in population_files:
    
    file_path = os.path.join(population_path, file)
    temp_df = pd.read_excel(file_path)
   
    # Add the processed DataFrame to the cumulative DataFrame
    df_population = pd.concat([df_population, temp_df], ignore_index=True)
    
    # print progress
    print("Finished file " + file)


# change column names
df_population.rename(columns={'X': 'Lon', 'Y': 'Lat', 'Value': 'population'}, inplace=True)


# delete
del df_population, population_path, temp_df, file, file_path





# In[]

# export data

# --------------
# emissions changes by type
df_population.to_csv('999 - Data for Rudy - Global/population.csv', index=False)


