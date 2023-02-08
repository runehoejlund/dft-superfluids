#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=%(partition)s
#SBATCH -N 1      # Number of nodes
#SBATCH -n %(cores)s     # Total number of tasks
#SBATCH --time=0-%(hours)s:00:00
#SBATCH --output=%(out)s #name
#SBATCH --error=%(err)s  #name

%(setup)s

module purge
module add intel

~/bin/BiEx/biex/BiEx %(inp)s