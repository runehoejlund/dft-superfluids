formula = 'WS2'

# from calculate_ground_state import *
from bandstructure_groundstate import calculate_ground_state
from os.path import exists
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# out_dir = './out/'
# file_name = out_dir + 'gs_'+ formula + '_fulldiag.gpw'

# if exists(file_name):
#     parprint('Found fully diagonalised solution for ' + formula)
# else:
#     parprint('No precalculated ground state calculation found for ' + formula)
#     calculate_ground_state(formula, ecut=500)

calculate_ground_state(formula, ecut=500)