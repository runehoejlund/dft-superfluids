#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=s173965@student.dtu.dk  # The default value is the submitting user.
#SBATCH --partition=xeon16
#SBATCH -N 1      
#SBATCH -n 16    
#SBATCH --time=1-4:00:00
#SBATCH --output=mpi_job_gpaw_full.log
#SBATCH --error=mpi_job_gpaw_full_errors.log

# source ~/venv/bin/activate
module load GPAW

mpiexec gpaw python calc_gs_WS2.py
