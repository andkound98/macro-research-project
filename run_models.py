#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Koundouros [koundouros.andreas@gmail.com]
"""

###############################################################################
###############################################################################
# This script compares non-linear medium-scale RANK and TANK models after 
# different shocks (a technology shock and a discount factor shock)
###############################################################################
###############################################################################

# Import packages
import os
import time as tm
import econpizza as ep 
import numpy as np
import pandas as pd
#from grgrlib import pplot # Import this for plotting all (!) variables
import plotly.express as px
import plotly.io as pio

###############################################################################
###############################################################################

# Preliminaries

pio.renderers.default = "svg" # For plotting in the Spyder window
save_plot_yes = False # If true, it saves the plots after creating them
start = tm.time() # Start timer

horizon = 50 # Desired time horizon for the IRFs

###############################################################################
###############################################################################

# Set working directory accordingly
absolute_path = os.getcwd()

# Set path for RANK model, load the model and solve for its steady state
relative_path_rank = os.path.join("models", "rank.yaml")
full_path_rank = os.path.join(absolute_path, relative_path_rank)

rank = full_path_rank
rank_mod = ep.load(rank)
_ = rank_mod.solve_stst()

# Set path for TANK model, load the model and solve for its steady state
relative_path_tank = os.path.join("models", "tank.yaml")
full_path_tank = os.path.join(absolute_path, relative_path_tank)

tank = full_path_tank
tank_mod = ep.load(tank)
_ = tank_mod.solve_stst()

###############################################################################
###############################################################################

# Specify the shock here (one at a time)
specific_shock = ('e_z', 0.02) # Technology shock
#specific_shock = ('e_beta', 0.02) # Discount factor shock

###############################################################################
###############################################################################

# Find RANK IRFs to the specified shock
rank_x, rank_flag = rank_mod.find_path(shock = specific_shock)

# Find TANK IRFs to the specified shock
tank_x, tank_flag = tank_mod.find_path(shock = specific_shock)

###############################################################################
###############################################################################

# If desired, make plots for all (!) variables specified in the models

#pplot(rank_x[:horizon], labels = rank_mod['variables']) # Plot IRFs of RANK
#pplot(tank_x[:horizon], labels = tank_mod['variables']) # Plot IRFs of TANK

# Below, plots of key variables are created

###############################################################################
###############################################################################

# Preparations for plots of key variables 

# Extract key variables and find their indices
varlist_rank = 'c', 'n', 'pi', 'R', 'RR', 'y', 'w', 'i', 'prof'
varlist_tank = 'c', 'cuu', 'chh', 'n', 'nuu', 'nhh', 'pi', 'R', 'RR', 'y', 'w', 'i', 'prof'

indx_rank = [rank_mod['variables'].index(v) for v in varlist_rank]
indx_tank = [tank_mod['variables'].index(v) for v in varlist_tank]

# Consumption
rank_c = indx_rank[0] # Aggregate consumption RANK
tank_c = indx_tank[0] # Aggregate consumption TANK
tank_cuu =indx_tank[1] # Unconstrained agents' consumption TANK
tank_chh = indx_tank[2] # Hand-to-mouth agents' consumption TANK

# Labour hours
rank_n = indx_rank[1] # Aggregate labour hours RANK
tank_n = indx_tank[3] # Aggregate labour hours TANK
tank_nuu =indx_tank[4] # Unconstrained agents' labour hours TANK
tank_nhh = indx_tank[5] # Hand-to-mouth agents' labour hours TANK

# Inflation
rank_pi = indx_rank[2]
tank_pi = indx_tank[6]

# Wages
rank_w = indx_rank[6]
tank_w = indx_tank[10]

# Interest Rates
rank_r = indx_rank[3]
tank_r = indx_tank[7]
rank_rr = indx_rank[4]
tank_rr = indx_tank[8]

# Output 
rank_y = indx_rank[5]
tank_y = indx_tank[9]

# Investment 
rank_inv = indx_rank[7]
tank_inv = indx_tank[11]

# Firm Profits
rank_prof = indx_rank[8]
tank_prof = indx_tank[12]

###############################################################################

# Extract steady state values corresponding to the key variables (note that
# by construction, the last value of the IRFs is the steady state; 
# alternatively, one could also use the very first value, but these are 
# identical)

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
stst_rank_rr = rank_x[-1,rank_rr]
stst_tank_rr = tank_x[-1,tank_rr]

# Output 
stst_rank_y = rank_x[-1,rank_y]
stst_tank_y = tank_x[-1,tank_y]

# Investment 
stst_rank_inv = rank_x[-1,rank_inv]
stst_tank_inv = tank_x[-1,tank_inv]

# Firm Profits
stst_rank_prof = rank_x[-1,rank_prof]
stst_tank_prof = tank_x[-1,tank_prof]

###############################################################################
###############################################################################

# Preliminaries

time = list(range(0, horizon, 1)) # Time variable
percent = 100 # Turn to 100 (1) if impulse response should (not) be in percent

# Setting paths in case plots should be created 
relative_path_plots_technology = os.path.join("plots", "technology")
full_path_plots_technology = os.path.join(absolute_path, 
                                          relative_path_plots_technology) 

relative_path_plots_discount = os.path.join("plots", "discount")
full_path_plots_discount = os.path.join(absolute_path, 
                                        relative_path_plots_discount) 

###############################################################################
###############################################################################

# Aggregate Responses (for RANK vs TANK)

# Aggregate Consumption 
agg_consumption = np.column_stack([time, # Concatenate IRFs 
                                   percent*((rank_x[:horizon,rank_c] - stst_rank_c)/stst_rank_c), 
                                   percent*((tank_x[:horizon,tank_c] - stst_tank_c)/stst_tank_c)])
agg_consumption = pd.DataFrame(agg_consumption, # Turn data into data frame
                               columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(agg_consumption, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Consumption', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_agg_c = os.path.join(full_path_plots_technology, 
                                                    "technology_agg_c.svg")
    fig.write_image(full_path_plots_technology_agg_c)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_agg_c = os.path.join(full_path_plots_discount, 
                                                  "discount_agg_c.svg")
    fig.write_image(full_path_plots_discount_agg_c)

###############################################################################

# Aggregate Labour Hours
agg_labour = np.column_stack([time, # Concatenate IRFs  
                              percent*((rank_x[:horizon,rank_n] - stst_rank_n)/stst_rank_n), 
                              percent*((tank_x[:horizon,tank_n] - stst_tank_n)/stst_tank_n)])
agg_labour = pd.DataFrame(agg_labour, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(agg_labour, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Labour Hours', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_agg_n = os.path.join(full_path_plots_technology, 
                                                    "technology_agg_n.svg")
    fig.write_image(full_path_plots_technology_agg_n)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_agg_n = os.path.join(full_path_plots_discount, 
                                                  "discount_agg_n.svg")
    fig.write_image(full_path_plots_discount_agg_n)
    
###############################################################################

# Wages
wages = np.column_stack([time, 
                         percent*((rank_x[:horizon,rank_w] - stst_rank_w)/stst_rank_w), 
                         percent*((tank_x[:horizon,tank_w] - stst_tank_w)/stst_tank_w)])
wages = pd.DataFrame(wages, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(wages, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Real Wage', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_wage = os.path.join(full_path_plots_technology, 
                                                   "technology_wage.svg")
    fig.write_image(full_path_plots_technology_wage)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_wage = os.path.join(full_path_plots_discount, 
                                                 "discount_wage.svg")
    fig.write_image(full_path_plots_discount_wage)
    
###############################################################################

# Interest Rate
interest = np.column_stack([time, 
                            percent*((rank_x[:horizon,rank_r] - stst_rank_r)/stst_rank_r), 
                            percent*((tank_x[:horizon,tank_r] - stst_tank_r)/stst_tank_r)]) 
interest = pd.DataFrame(interest, columns = ['Quarters', 'RANK', 'TANK']) 

# Plotting
fig = px.line(interest, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Nominal Interest Rate', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_interest = os.path.join(full_path_plots_technology, 
                                                       "technology_interest.svg")
    fig.write_image(full_path_plots_technology_interest)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_interest = os.path.join(full_path_plots_discount, 
                                                     "discount_interest.svg")
    fig.write_image(full_path_plots_discount_interest)
    
###############################################################################    

# Real Rate
real_interest = np.column_stack([time, 
                      percent*((rank_x[:horizon,rank_rr] - stst_rank_rr)/stst_rank_rr), 
                      percent*((tank_x[:horizon,tank_rr] - stst_tank_rr)/stst_tank_rr)])
real_interest = pd.DataFrame(real_interest, 
                             columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(real_interest, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Real Interest Rate', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_rr = os.path.join(full_path_plots_technology, 
                                                   "technology_rr.svg")
    fig.write_image(full_path_plots_technology_rr)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_rr = os.path.join(full_path_plots_discount, 
                                                 "discount_rr.svg")
    fig.write_image(full_path_plots_discount_rr)

###############################################################################

# Ouptut
output = np.column_stack([time, 
                          percent*((rank_x[:horizon,rank_y] - stst_rank_y)/stst_rank_y), 
                          percent*((tank_x[:horizon,tank_y] - stst_tank_y)/stst_tank_y)]) 
output = pd.DataFrame(output, columns = ['Quarters', 'RANK', 'TANK']) 

# Plotting
fig = px.line(output, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Output', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_output = os.path.join(full_path_plots_technology, 
                                                     "technology_output.svg")
    fig.write_image(full_path_plots_technology_output)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_output = os.path.join(full_path_plots_discount, 
                                                   "discount_output.svg")
    fig.write_image(full_path_plots_discount_output)

###############################################################################

# Inflation 
inflation = np.column_stack([time, 
                             percent*((rank_x[:horizon,rank_pi] - stst_rank_pi)/stst_rank_pi), 
                             percent*((tank_x[:horizon,tank_pi] - stst_tank_pi)/stst_tank_pi)])
inflation = pd.DataFrame(inflation, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(inflation, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Inflation', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_infl = os.path.join(full_path_plots_technology, 
                                                   "technology_infl.svg")
    fig.write_image(full_path_plots_technology_infl)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_infl = os.path.join(full_path_plots_discount, 
                                                 "discount_infl.svg")
    fig.write_image(full_path_plots_discount_infl)

###############################################################################

# Investment
investment = np.column_stack([time, 
                             percent*((rank_x[:horizon,rank_inv] - stst_rank_inv)/stst_rank_inv), 
                             percent*((tank_x[:horizon,tank_inv] - stst_tank_inv)/stst_tank_inv)])
investment = pd.DataFrame(investment, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(investment, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Investment', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_inv = os.path.join(full_path_plots_technology, 
                                                   "technology_inv.svg")
    fig.write_image(full_path_plots_technology_inv)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_inv = os.path.join(full_path_plots_discount, 
                                                 "discount_inv.svg")
    fig.write_image(full_path_plots_discount_inv)

###############################################################################

# Firm Profits
profits = np.column_stack([time, 
                             percent*((rank_x[:horizon,rank_prof] - stst_rank_prof)/stst_rank_prof), 
                             percent*((tank_x[:horizon,tank_prof] - stst_tank_prof)/stst_tank_prof)])
profits = pd.DataFrame(profits, columns = ['Quarters', 'RANK', 'TANK'])

# Plotting
fig = px.line(profits, x = "Quarters", y = ['RANK', 'TANK'],
              color_discrete_map={'RANK': '#636EFA', 
                                  'TANK': '#FFA15A'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Firm Profits', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_prof = os.path.join(full_path_plots_technology, 
                                                   "technology_prof.svg")
    fig.write_image(full_path_plots_technology_prof)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_prof = os.path.join(full_path_plots_discount, 
                                                 "discount_prof.svg")
    fig.write_image(full_path_plots_discount_prof)

###############################################################################
###############################################################################

# Individual-Level Responses (for TANK)

# Consumption 
ind_consumption = np.column_stack([time, 
                               percent*((tank_x[:horizon,tank_chh] - stst_tank_chh)/stst_tank_chh), 
                               percent*((tank_x[:horizon,tank_cuu] - stst_tank_cuu)/stst_tank_cuu)]) 
ind_consumption = pd.DataFrame(ind_consumption, 
                               columns = ['Quarters', 'TANK Hand-to-Mouth', 'TANK Unconstrained']) 

# Plotting
fig = px.line(ind_consumption, x = "Quarters", 
              y = ['TANK Hand-to-Mouth', 'TANK Unconstrained'],
              color_discrete_map={'TANK Hand-to-Mouth': '#FF6692', 
                                  'TANK Unconstrained': '#00CC96'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Consumption', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_ind_c = os.path.join(full_path_plots_technology, 
                                                    "technology_ind_c.svg")
    fig.write_image(full_path_plots_technology_ind_c)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_ind_c = os.path.join(full_path_plots_discount, 
                                                  "discount_ind_c.svg")
    fig.write_image(full_path_plots_discount_ind_c)
    
###############################################################################

# Labour Hours
ind_labour = np.column_stack([time, 
                          percent*((tank_x[:horizon,tank_nhh] - stst_tank_nhh)/stst_tank_nhh), 
                          percent*((tank_x[:horizon,tank_nuu] - stst_tank_nuu)/stst_tank_nuu)]) 
ind_labour = pd.DataFrame(ind_labour, 
                          columns = ['Quarters', 'TANK Hand-to-Mouth', 'TANK Unconstrained'])

# Plotting
fig = px.line(ind_labour, x = "Quarters", 
              y = ['TANK Hand-to-Mouth', 'TANK Unconstrained'],
              color_discrete_map={'TANK Hand-to-Mouth': '#FF6692',
                                  'TANK Unconstrained': '#00CC96'})
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Labour Hours', # y-axis labeling
                   font=dict(size=20),
                   legend=dict(orientation="h", # For horizontal legend
                               yanchor="bottom", y=1.02, xanchor="right", x=1), 
                   legend_title=None, plot_bgcolor = 'whitesmoke', 
                   margin=dict(l=15, r=15, t=5, b=5))
fig.update_traces(line=dict(width=6))
fig.show() # Display plot

# Save plot as SVG
if specific_shock[0] == 'e_z' and save_plot_yes == True:
    full_path_plots_technology_ind_n = os.path.join(full_path_plots_technology, 
                                                    "technology_ind_n.svg")
    fig.write_image(full_path_plots_technology_ind_n)

if specific_shock[0] == 'e_beta' and save_plot_yes == True:
    full_path_plots_discount_ind_n = os.path.join(full_path_plots_discount, 
                                                  "discount_ind_n.svg")
    fig.write_image(full_path_plots_discount_ind_n)

###############################################################################
###############################################################################

# Print run time
print('It took', (tm.time()-start)/60, 'minutes to execute this script.')