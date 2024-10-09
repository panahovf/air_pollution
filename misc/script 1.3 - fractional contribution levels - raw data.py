# In[1]:
# Date: Sep 2, 2024
# Project: Identify grid level fractional contribution
# Author: Farhad Panahov

# description: The data is given as following:
    # Lat and Lon data are given in separate .csv file
    # Fractional contribution factors are given separately for individual type of fossil fuels but without respective lat&lon locations

# Steps: Get grid level 'fractional contribution source' from each type of fossil fuels:
    # Here is the source: https://zenodo.org/records/4739100
    # Sources included: ENEcoal, ENEother, INDcoal, INDother
    # Definitions: ENEcoal - Energy Production (coal combustion only) - Includes electricity and heat production, fuel production and transformation, oil and gas fugitive/flaring, and fossil fuel fires:
        # ENEother - Energy Production (all non-coal combustion) - Includes electricity and heat production, fuel production and transformation, oil and gas fugitive/flaring, and fossil fuel fires
        # INDcoal - Industry (coal combustion only) - Includes Industrial combustion (iron and steel, non-ferrous metals, chemicals, pulp and paper, food and tobacco, non-metallic minerals, construction, transportation equipment, machinery, mining and quarrying, wood products, textile and leather, and other industry combustion) and non-combustion industrial processes and product use (cement production, lime production, other minerals, chemical industry, metal production, food, beverage, wood, pulp, and paper, and other non-combustion industrial emissions)
        # INDother - Industry (all non-coal combustion) - Includes Industrial combustion (iron and steel, non-ferrous metals, chemicals, pulp and paper, food and tobacco, non-metallic minerals, construction, transportation equipment, machinery, mining and quarrying, wood products, textile and leather, and other industry combustion) and non-combustion industrial processes and product use (cement production, lime production, other minerals, chemical industry, metal production, food, beverage, wood, pulp, and paper, and other non-combustion industrial emissions)
    # Usage:
        # ENEcoal for power related emissions from coal combustion, and ENEother for power from oil and gas
        # INDcoal for extration related emissions from coal, and INDother for oil and gas extraction emissions
    # Note: this data has been sampled for the time being for Poland as a case study
    # How: 
        # select indexes from LAT LON data that correspond to max/min lat and lon of Poland
        # save the indexes, and then load these indexes from individual fractional contribution files
        # and combine into a single dataframe




   





# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import json










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory


# --------------
# LOAD FRACTIONAL CONTRIBUTION DATA

# STEP 3 --- combine all files

# load indexes from previous step
files = [
    "GBD-MAPS_Gridded_Fractional_Contributions_LatLon",
    "GBD-MAPS_Gridded_Fractional_Contributions_INDcoal",
    "GBD-MAPS_Gridded_Fractional_Contributions_INDother"
]

# load the files
dfs = [pd.read_csv("2 - output/script 1.2 - fractional contribution levels - raw data/" + fname + "_reduced.csv", index_col=None) for fname in files]


# combine into a singe datarame
df = pd.concat(dfs, axis=1)


# export
df.to_csv("2 - output/script 1.2 - fractional contribution levels - raw data/combined_ind.csv")












