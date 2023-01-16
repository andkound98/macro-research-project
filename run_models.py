#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:27:44 2022

@author: andreaskoundouros
"""

###############################################################################
###############################################################################
# This script compares RANK and TANK after different shocks
###############################################################################
###############################################################################

# Import packages
import econpizza as ep 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "svg" # For plotting in the Spyder window

###############################################################################
###############################################################################

# Load and solve RANK
rank = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_rank.yaml" # Set path here
rank_mod = ep.load(rank)
_ = rank_mod.solve_stst()

# Load and solve TANK
tank = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_tank.yaml" # Set path here
#tank = "/Users/andreaskoundouros/Documents/Uni Master WS22:23/RM Macro/Project/yaml/med_scale_tank_extension_2.yaml" # Load the extension TANK file
tank_mod = ep.load(tank)
_ = tank_mod.solve_stst()

###############################################################################
###############################################################################

# Specify shock here (one at a time)
specific_shock = ('e_z', 0.02) # Technology shock
#specific_shock = ('e_beta', 0.02) # Discount factor shock
#specific_shock = ('e_m', 0.02) # Monetary poilicy shock

###############################################################################
###############################################################################

# Find IRFs for RANK 
rank_x, rank_flag = rank_mod.find_path(shock = specific_shock)

# Find IRFs for TANK
tank_x, tank_flag = tank_mod.find_path(shock = specific_shock)

###############################################################################
###############################################################################

# Extract relevant variables
varlist_rank = 'c', 'n', 'pi', 'R', 'Rn', 'y', 'w'
varlist_tank = 'c', 'cuu', 'chh', 'n', 'nuu', 'nhh', 'pi', 'R', 'Rn', 'y', 'w'

indx_rank = [rank_mod['variables'].index(v) for v in varlist_rank]
indx_tank = [tank_mod['variables'].index(v) for v in varlist_tank]

# Consumption
rank_c = indx_rank[0]
tank_c = indx_tank[0]
tank_cuu =indx_tank[1]
tank_chh = indx_tank[2]

# Labour hours
rank_n = indx_rank[1]
tank_n = indx_tank[3]
tank_nuu =indx_tank[4]
tank_nhh = indx_tank[5]

# Inflation
rank_pi = indx_rank[2]
tank_pi = indx_tank[6]

# Wages
rank_w = indx_rank[6]
tank_w = indx_tank[10]

# Interest Rates
rank_r = indx_rank[3]
rank_rn = indx_rank[4]
tank_r = indx_tank[7]
tank_rn = indx_tank[8]

# Output 
rank_y = indx_rank[5]
tank_y = indx_tank[9]

###############################################################################

# Extract relevant steady state values
# Consumption
stst_rank_c = rank_x[-1,rank_c]
stst_tank_c = tank_x[-1,tank_c]
stst_tank_cuu = tank_x[-1,tank_cuu]
stst_tank_chh = tank_x[-1,tank_chh]

# Labour hours
stst_rank_n = rank_x[-1,rank_n]
stst_tank_n = tank_x[-1,tank_n]
stst_tank_nuu = tank_x[-1,tank_nuu]
stst_tank_nhh = tank_x[-1,tank_nhh]

# Inflation 
stst_rank_pi = rank_x[-1,rank_pi]
stst_tank_pi = tank_x[-1,tank_pi]

# Wages
stst_rank_w = rank_x[-1, rank_w]
stst_tank_w = tank_x[-1, tank_w]

# Interest Rates
stst_rank_r = rank_x[-1,rank_r]
stst_tank_r = tank_x[-1,tank_r]

# Output 
stst_rank_y = rank_x[-1,rank_y]
stst_tank_y = tank_x[-1,tank_y]

###############################################################################
###############################################################################

# Create data frame for plotting
horizon = 50 # Time horizon
time = list(range(0, horizon, 1)) # Create time variable
percent = 100 # Turn to 100 (1) if impulse response should (not) be in percent

###############################################################################
###############################################################################

# Aggregate Responses 

# Aggregate Consumption 
agg_consumption = np.column_stack([time, percent*((rank_x[:horizon,rank_c] - stst_rank_c)/stst_rank_c), percent*((tank_x[:horizon,tank_c] - stst_tank_c)/stst_tank_c)]) # Concatenate data 
agg_consumption = pd.DataFrame(agg_consumption, columns = ['Quarters', 'RANK', 'TANK']) # Turn data into data frame

# Plotting
fig = px.line(agg_consumption, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Consumption', # y-axis labeling
                   font=dict(size=20),
                   legend=dict( # For horizontal legend
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################

# Aggregate Labour Hours
agg_labour = np.column_stack([time, percent*((rank_x[:horizon,rank_n] - stst_rank_n)/stst_rank_n), percent*((tank_x[:horizon,tank_n] - stst_tank_n)/stst_tank_n)]) # Concatenate data 
agg_labour = pd.DataFrame(agg_labour, columns = ['Quarters', 'RANK', 'TANK']) # Turn data into data frame

# Plotting
fig = px.line(agg_labour, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Labour Hours', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################

# Inflation 
inflation = np.column_stack([time, percent*((rank_x[:horizon,rank_pi] - stst_rank_pi)/stst_rank_pi), percent*((tank_x[:horizon,tank_pi] - stst_tank_pi)/stst_tank_pi)])
inflation = pd.DataFrame(inflation, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(inflation, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Inflation', # y-axis labeling
                   font=dict(size=20),
                   legend=dict( 
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################

# Wages
wages = np.column_stack([time, percent*((rank_x[:horizon,rank_w] - stst_rank_w)/stst_rank_w), percent*((tank_x[:horizon,tank_w] - stst_tank_w)/stst_tank_w)])
wages = pd.DataFrame(wages, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(wages, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Real Wage', # y-axis labeling
                   font=dict(size=20),
                   legend=dict( 
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################

# Interest Rate
interest = np.column_stack([time, percent*((rank_x[:horizon,rank_r] - stst_rank_r)/stst_rank_r), percent*((tank_x[:horizon,tank_r] - stst_tank_r)/stst_tank_r)]) # Concatenate data 
interest = pd.DataFrame(interest, columns = ['Quarters', 'RANK', 'TANK']) # Turn data into data frame

# Plotting
fig = px.line(interest, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Nominal Interest Rate', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################

# Ouptut
output = np.column_stack([time, percent*((rank_x[:horizon,rank_y] - stst_rank_y)/stst_rank_y), percent*((tank_x[:horizon,tank_y] - stst_tank_y)/stst_tank_y)]) # Concatenate data 
output = pd.DataFrame(output, columns = ['Quarters', 'RANK', 'TANK']) # Turn data into data frame

# Plotting
fig = px.line(output, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Output', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################
###############################################################################

# Individual-Level Responses 

# Consumption 
consumption = np.column_stack([time, percent*((tank_x[:horizon,tank_chh] - stst_tank_chh)/stst_tank_chh), percent*((tank_x[:horizon,tank_cuu] - stst_tank_cuu)/stst_tank_cuu)]) # , (rank_x[:horizon,rank_c] - stst_rank_c)/stst_rank_c, (tank_x[:horizon,tank_c] - stst_tank_c)/stst_tank_c
consumption = pd.DataFrame(consumption, columns = ['Quarters', 'TANK Hand-to-Mouth', 'TANK Unconstrained']) # , 'RANK Consumption', 'TANK Consumption'

# Plotting
fig = px.line(consumption, x = "Quarters", y = ['TANK Hand-to-Mouth', 'TANK Unconstrained'],
              color_discrete_map={'RANK Hand-to-Mouth': '#00CC96', 
                                  'TANK Unconstrained': '#FF6692'}) # , 'RANK Consumption', 'TANK Consumption'
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Consumption', # y-axis labeling
                   font=dict(size=20),
                   legend=dict( # For horizontal legend
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot

###############################################################################

# Labour Hours
labour = np.column_stack([time, percent*((tank_x[:horizon,tank_nhh] - stst_tank_nhh)/stst_tank_nhh), percent*((tank_x[:horizon,tank_nuu] - stst_tank_nuu)/stst_tank_nuu)]) # , (rank_x[:horizon,rank_n] - stst_rank_n)/stst_rank_n, (tank_x[:horizon,tank_n] - stst_tank_n)/stst_tank_n
labour = pd.DataFrame(labour, columns = ['Quarters', 'TANK Hand-to-Mouth', 'TANK Unconstrained']) # , 'RANK Labour', 'TANK Labour'

# Plotting
fig = px.line(labour, x = "Quarters", y = ['TANK Hand-to-Mouth', 'TANK Unconstrained'],
              color_discrete_map={'RANK Hand-to-Mouth': '#00CC96', 
                                  'TANK Unconstrained': '#FF6692'}) # , 'RANK Labour', 'TANK Labour'
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Labour Hours', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(
    orientation="h", # For horizontal legend
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), legend_title=None, plot_bgcolor = 'whitesmoke')
fig.update_traces(line=dict(width=3))
fig.show() # Display plot
