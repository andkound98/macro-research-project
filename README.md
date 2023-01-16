# The Dynamic Consequences of Technology and Discount Factor Shocks in Medium-Scale RANK vs TANK Models

By the end of January, I will collect in this repository everything relevant to the project I submit in January 2023 for the Research Module  "Macroeconomics and Public Economics" in the Economics Master's programme at the University of Bonn.

## `run_models.py`
This file implements the analyses of subsections 4.1 and 4.2. The file first loads the files in which the models are stored, then solves for the steady state of the respective model by the means of root-finding. Then, one of the shocks is initiated, which is done by setting the disturbance equal to 0.02 (other values are also possible) in $t = 0$. Thereafter, the resulting non-linear equilibrium dynamics, i.e. impulse responses, following each of the shocks are solved for, thereby guaranteeing that all variables return to their respective steady state within a prescribed period of time. The results for some important variables, on the aggregate as well as on the individual level, are then plotted.

## `run_tank_loop.py`
This file conducts the analysis in subsection 4.3.
