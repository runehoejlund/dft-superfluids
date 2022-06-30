#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --mail-user=s183774@student.dtu.dk  # The default value is the submitting user.
#SBATCH --partition=%(partition)s
#SBATCH -N 1      # Minimum of 1 node
#SBATCH -n %(cores)s     # 24 MPI processes per node, 48 tasks in total, appropriate for xeon24 nodes
#SBATCH --time=0-%(hours)s:00:00
#SBATCH --output=%(out)s #name
#SBATCH --error=%(err)s  #name

module purge
module add intel

~/bin/BiEx/biex/BiEx %(inp)s