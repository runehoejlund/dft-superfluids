# 2. Ab Initio Calculation with QEH Model
This directory contains the script `01_qeh_calculations.py`, which combines the TMO and TMD layers into bilayers and calculates the intrinsic screening in the bilayer structure using the ab initio QEH framework. For comparison we calculate the screened interaction with 3 different methods:
1. Using an analytic screened coulomb potential with a constant dielectric function of $\epsilon=2$ **and constant interlayer distance $d_0 = 9.1$ Å**.
    *e.g. for the variable: U_ee_analytic_const_d*
2. Using an analytic screened coulomb potential with a constant dielectric function of $\epsilon=2$ **and variable interlayer distance determined from DFT-calculations**.
    *e.g. for the variable: U_ee_analytic*
3. Using the QEH framework. 
    *e.g. for the variable: U_ee*

Before running the script, you should have run all scripts in the directory `01-material-selection`.

## Data Analysis
The resulting data is analysed in the iPython Notebook, `./02_qeh_analysis.ipynb`.
The iPython Notebook also generates the plots seen in the article.

## Preparation for the gap equation
After the qeh-calculations in `01_qeh_calculations.py` have finished, you can run the script `./03_prepare_for_gap_equation_calculations.sh` which simply copies the data from the qeh calculations into the directory `03-gap-equation` (for performing the gap equation calculations).