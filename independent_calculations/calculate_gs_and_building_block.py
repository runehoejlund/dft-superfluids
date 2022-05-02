from calculate_building_block import *
from calculate_ground_state import *
from os.path import exists
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


out_dir = './out/'

materials = ['BN']
# materials = ['BN', 'MoS2', 'MoSe2', 'MoTe2', 'WS2', 'WSe2', 'WTe2']
for formula in materials:
    file_name = out_dir + 'gs_'+ formula + '_fulldiag.gpw'
    if exists(file_name):
        parprint('Found fully diagonalised solution for ' + formula)
        calculate_building_block(formula)
    else:
        parprint('No precalculated ground state calculation found for ' + formula)
        # calculate_ground_state(formula)
        # calculate_building_block(formula)