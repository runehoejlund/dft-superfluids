# This file simply runs all bash scripts (ending with _MF.sh)
# It is supposed to be automatically copied to the directory with .dat files.
# By running it at the correct directory we start the BiEX gap equation calculations.

for file in ./*_MF.sh; do
    sbatch $file
done