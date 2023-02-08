# 3. Solve Gap Equation

This directory contains the files for running the final step of our workflow as described in the article, namely solving the gap equation.
Before doing calculations in here you should have run the scripts in the directories `01-material-selection` and `02-qeh-calculations`. We have 3 simple automated preperation scripts:
1. `01_generate_dat_files.py`: takes the effective intrisc screened interaction within the QEH model for each vdWH and saves these to a `.dat` file, which the BiEx framework can read.
2. `02_generate_imp_sh_files.py`: generates a bash script for each vdWH. Running such a script starts a gap equation calculation
3. `03_copy_run_all_script.sh`: simply copies the `run_all.sh` script to the `out` directory, where gap equation calculations are performed

After running these 3 scripts you can navigate to the `out` directory and run the `run_all.sh` script to sbatch all gap equation calculations. This assumes that you are on an HPC environment with sbatch, if not, then you need to run the gap equation calculation scripts (`_MF.sh`-files) in another manner.