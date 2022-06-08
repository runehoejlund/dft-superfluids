formula = 'MoS2'

from calculate_eigenvalues import calculate_eigenvalues
from os.path import exists
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

calculate_eigenvalues(formula, ecut=500)