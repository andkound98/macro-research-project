# The Dynamic Consequences of Technology and Discount Factor Shocks in Medium-Scale RANK vs TANK Models

By the end of January, I will collect in this repository the relevant material for the project I submit in January 2023 for the Research Module  "Macroeconomics and Public Economics" in the Economics Master's programme at the University of Bonn.

In brief, the paper contrasts a two-agent New Keynesian model (TANK) to an otherwise unchanged non-linear medium-scale representative-agent New Keynesian model (RANK) by first discussing the changes needed to obtain the two-agent structure and consequently implementing the two models computationally to solve for the dynamics of TANK and RANK after two distinct shocks.

---

## `run_models.py`
This code file implements the analyses of subsections 4.1 and 4.2 of the paper and produces the plots found therein.

The code first loads the files in which the RANK and TANK models are stored (from the `models` folder), then solves for the steady state of the respective model by the means of root-finding. Thereafter, one of the shocks is initiated, which is done by setting one of the two disturbances equal to $0.02$ (other values are also possible) in $t = 1$. 

As a next step, the resulting (non-linear) equilibrium dynamics, i.e. the impulse responses to each of the shock are solved for, thereby guaranteeing that all variables return to their respective steady state within a prescribed period of time. The results for some important variables, on the aggregate as well as on the individual level, are then plotted. If desired, one can plot all variables' impulse responses as well.

## `run_tank_loop_eta_lambda.py`
This file conducts the analysis of subsection 4.3. In particular, the code runs a double loop, which iterates over a sequence of values for $\eta$, thereby solving in each step the RANK model with that given value of $\eta$. In each iteration, the code also computes the corresponding TANK solution, while looping over a sequence of values for $\lambda$ in TANK. With this approach, each TANK model with different values of $\lambda$ can be compared to a respective RANK model with the same choice for $\eta$.

Finally, the code produces the plots for figure 5 of the paper.

---

All codes were run using the Spyder IDE 5.3.3 with Python 3.9.12 and [`econpizza`](https://pypi.org/project/econpizza/) 0.4.1 on macOS 12.6.1.
