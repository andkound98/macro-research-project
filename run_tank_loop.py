#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:48:13 2023

@author: andreaskoundouros
"""

###############################################################################
###############################################################################
# This script compares TANK models depending on the share of hand-to-mouth 
# agents
###############################################################################
###############################################################################

# Import packages
import econpizza as ep
import numpy as np
import pandas as pd
import copy
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "svg" # For plotting in the Spyder window

###############################################################################
###############################################################################

# Preliminaries 
horizon = 50 # Time horizon
percent = 100 # Turn to 100 (1) if impulse response should (not) be in percent
time = list(range(0, horizon, 1)) # Create time variable

###############################################################################
###############################################################################

# Specify shock here (one at a time)
#specific_shock = ('e_z', 0.02) # Technology shock
specific_shock = ('e_beta', 0.02) # Discount factor shock
#specific_shock = ('e_m', 0.02) # Monetary poilicy shock

###############################################################################
###############################################################################

# Solve and solve RANK
rank = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_rank.yaml" # Set path here
rank_mod = ep.load(rank)
_ = rank_mod.solve_stst()
rank_x, rank_flag = rank_mod.find_path(shock = specific_shock)

# Do preparatory calculations with RANK (serves a benchmark for TANK)
varlist_lambda = 'c' 
indx_rank = [rank_mod['variables'].index(v) for v in varlist_lambda]
rank_c = indx_rank[0]
stst_rank_c = rank_x[-1,rank_c]
rank_benchmark_c = percent*((rank_x[:horizon,rank_c] - stst_rank_c)/stst_rank_c)
impact_rank_benchmark_c = percent*((rank_x[1,rank_c] - stst_rank_c)/stst_rank_c)

###############################################################################

# Load baseline TANK model
tank_model_loop = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_tank.yaml" # Set path here

# Duplicate the TANK model
tank_dictionary_0 = ep.parse(tank_model_loop)
tank_copy_lambda = copy.deepcopy(tank_dictionary_0)

###############################################################################
###############################################################################

# Preparations for the loop

# Sequence of lambda values
lambda_sequence = np.arange(0., 0.6, 0.05)

# Initialise empty containers
consumption_lambda = [] # Container for storing the full impulse responses
impact_lambda = [] # Container for impact effect

###############################################################################
###############################################################################

# For loop over values of lambda  
for ll in lambda_sequence:
    # Change lambda 
    tank_copy_lambda['steady_state']['fixed_values']['lam'] = ll
    
    # Load the model with the new value of lambda 
    model_lambda = ep.load(tank_copy_lambda)
    
    # Solve the model and find impulse responses
    _ = model_lambda.solve_stst()
    x_lambda, flag_lambda = model_lambda.find_path(shock = specific_shock)
    
    # Grab consumption
    indx_tank_lambda = [model_lambda['variables'].index(v) for v in varlist_lambda]
    
    # Store impulse responses
    c_lambda = indx_tank_lambda[0]
    stst_c_lambda = x_lambda[-1,c_lambda]
    consumption_lambda.append((percent*((x_lambda[:horizon,c_lambda] - stst_c_lambda)/stst_c_lambda)) - (rank_benchmark_c))
    
    # Store impact effect
    impact_lambda.append((percent*((x_lambda[1,c_lambda] - stst_c_lambda)/stst_c_lambda)) - (impact_rank_benchmark_c))

###############################################################################
###############################################################################

# Impulse response functions

# Create sequence of lambdas in string format
# lambda_sequence_strings = lambda_sequence.tolist()
# lambda_sequence_strings = list(map(str, lambda_sequence_strings))
# lambda_sequence_strings.append('Quarters')

# Create final dataframe
# consumption_lambda.append(time)
# consumption_lambda_df = pd.DataFrame(consumption_lambda)
# consumption_lambda_df = consumption_lambda_df.transpose()
# consumption_lambda_df.columns = lambda_sequence_strings

###############################################################################

# Impulse response functions, depending on lambda
# fig = px.line(consumption_lambda_df, x = "Quarters", y = lambda_sequence_strings)
# fig.update_layout(title='', # Empty title
#                    xaxis_title='Quarters', # x-axis labeling
#                    yaxis_title='Consumption in Deviation from RANK', # y-axis labeling
#                    legend=dict( # For horizontal legend
#     orientation="h",
#     yanchor="bottom",
#     y=1.02,
#     xanchor="right",
#     x=1
# ), legend_title=None, plot_bgcolor = 'whitesmoke')
# fig.show() # Display plot

###############################################################################
###############################################################################

# Impact effect

# Plotting the impact effect, depending on lambda
fig = px.line(x = lambda_sequence, y = impact_lambda, markers=True)
fig.update_yaxes(range=[-1.5, 0.1]) # Ensure the same y-axis range across figures
fig.update_traces(line=dict(color="orange", width=3), 
                  marker=dict(size=10))
fig.update_layout(title='', # Empty title
                   xaxis_title="\u03BB", # x-axis labeling
                   yaxis_title='Consumption Impact', # y-axis labeling
                   plot_bgcolor = 'whitesmoke', 
                   font=dict(size=20))
fig.show()
