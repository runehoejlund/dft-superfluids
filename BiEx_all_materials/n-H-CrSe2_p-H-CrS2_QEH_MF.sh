#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --mail-user=s183774@student.dtu.dk  # The default value is the submitting user.
#SBATCH --partition=xeon40_768
#SBATCH -N 1      # Minimum of 1 node
#SBATCH -n 40     # 24 MPI processes per node, 48 tasks in total, appropriate for xeon24 nodes
#SBATCH --time=0-24:00:00
#SBATCH --output=n-H-CrSe2_p-H-CrS2_QEH_MF/out.txt #name
#SBATCH --error=n-H-CrSe2_p-H-CrS2_QEH_MF/err.txt  #name

module purge
module add intel

~/bin/BiEx/biex/BiEx n-H-CrSe2_p-H-CrS2_QEH_MF.inp
