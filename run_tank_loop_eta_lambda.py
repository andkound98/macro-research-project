#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:48:13 2023

@author: andreaskoundouros
"""

###############################################################################
###############################################################################
# This script loops over the parameter values of eta and lambda in RANK and 
# TANK (lambda only in TANK)
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
percent = 100 # Turn to 100 (1) if impact effect should (not) be in percent
varlist_consumption = 'c' # Specify variable to be checked (here: aggregate 
                          # consumption)

###############################################################################
###############################################################################

# Specify shock here (one at a time)
specific_shock = ('e_z', 0.02) # Technology shock
#specific_shock = ('e_beta', 0.02) # Discount factor shock # 0.198
#specific_shock = ('e_m', 0.02) # Monetary poilicy shock

###############################################################################
###############################################################################

# Load models

# Load baseline RANK model
rank_model_loop = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_rank.yaml" # Set path here

# Duplicate the RANK model
rank_dictionary_0 = ep.parse(rank_model_loop)
rank_copy_eta = copy.deepcopy(rank_dictionary_0)

###############################################################################

# Load baseline TANK model
tank_model_loop = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_tank.yaml" # Set path here

# Duplicate the TANK model
tank_dictionary_0 = ep.parse(tank_model_loop)
tank_copy_eta_lambda = copy.deepcopy(tank_dictionary_0)

###############################################################################
###############################################################################

# Preparations for the loop

# Sequence of lambda values
lambda_sequence = np.arange(0.1, 0.46, 0.05)

# Sequence of eta values
eta_sequence = np.arange(0.33, 1, 0.15)
eta_sequence = np.append(eta_sequence, 1)

# Convert sequnces to lists of strings for row and column names
lambda_sequence_strings = lambda_sequence.tolist()
lambda_sequence_strings = list(map(str, lambda_sequence_strings))

eta_sequence_strings = eta_sequence.tolist()
eta_sequence_strings = list(map(str, eta_sequence_strings))

# Initialise empty container for impact values
impact_eta_lambda = pd.DataFrame(np.nan, index = lambda_sequence, columns = eta_sequence)

###############################################################################
###############################################################################

# For loop over eta and lambda values

for ee in eta_sequence:
    # RANK for eta = ee
    rank_copy_eta['steady_state']['fixed_values']['eta'] = ee
    model_rank_eta = ep.load(rank_copy_eta)
    _ = model_rank_eta.solve_stst()
    x_rank_eta, flag_rank_eta = model_rank_eta.find_path(shock = specific_shock)
    
    indx_rank_eta = [model_rank_eta['variables'].index(v) for v in varlist_consumption]
    rank_eta_index_c = indx_rank_eta[0]
    stst_rank_eta_c = x_rank_eta[-1, rank_eta_index_c]
    impact_rank_eta_c = (x_rank_eta[1, rank_eta_index_c] - stst_rank_eta_c)/stst_rank_eta_c
    
    for ll in lambda_sequence:
        try:
            # For a given eta, do TANK for lambda = ll
            tank_copy_eta_lambda['steady_state']['fixed_values']['eta'] = ee
            tank_copy_eta_lambda['steady_state']['fixed_values']['lam'] = ll
            model_tank_eta_lambda = ep.load(tank_copy_eta_lambda)
            _ = model_tank_eta_lambda.solve_stst()
            x_tank_eta_lambda, flag_tank_eta_lambda = model_tank_eta_lambda.find_path(shock = specific_shock)
            
            indx_tank_eta_lambda = [model_tank_eta_lambda['variables'].index(v) for v in varlist_consumption]
            tank_eta_lambda_index_c = indx_tank_eta_lambda[0]
            stst_tank_eta_lambda_c = x_tank_eta_lambda[-1, tank_eta_lambda_index_c]
            impact_tank_eta_lambda_c = (x_tank_eta_lambda[1, tank_eta_lambda_index_c] - stst_tank_eta_lambda_c)/stst_tank_eta_lambda_c
            
            # Store results
            impact_eta_lambda.loc[ll, ee] = percent * (impact_tank_eta_lambda_c - impact_rank_eta_c)
        except:
            continue

###############################################################################
###############################################################################

# Plot the results

newnames = {'0.33':'0.33', '0.48': '0.48', '0.6299999999999999': '0.63', 
            '0.7799999999999999': '0.78', '0.9299999999999999': '0.93', 
            '1.0': '1.0'}
fig = px.line(impact_eta_lambda, markers = True, 
              color_discrete_sequence=['#636EFA', '#FFA15A', '#EF553B', 
                                       '#00CC96', '#19D3F3', '#FECB52'],
              labels={'0.33': "hello"}) 
fig.update_yaxes(range=[-4, 0.])
fig.update_traces(line=dict(width=3), 
                  marker=dict(size=10))
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
fig.update_layout(title='', # Empty title
                   xaxis_title="\u03BB", # x-axis labeling
                   yaxis_title='Relative Consumption Impact', # y-axis labeling
                   plot_bgcolor = 'whitesmoke', 
                   font=dict(size=20), 
                   margin=dict(l=15, r=15, t=15, b=15), legend=dict(
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None)
fig.show()
fig.write_image("/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/Plots/sensitivity/sensitivity_technology.svg")
#fig.write_image("/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/Plots/sensitivity/sensitivity_discount.svg")
