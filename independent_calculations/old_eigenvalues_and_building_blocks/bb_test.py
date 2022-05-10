from pathlib import Path
from gpaw.mpi import world
from gpaw.response.df import DielectricFunction
from gpaw.response.qeh import BuildingBlock
from os.path import exists
from ase.parallel import parprint
import numpy as np

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

formula = 'MoSe2'
filename = './out/gs_' + formula + '_fulldiag.gpw'

if exists(filename):
    parprint('Found fully diagonalised solution for ' + formula)
    df = DielectricFunction(calc=filename,
                        frequencies={
                            'type': 'nonlinear',
                            'domega0': 0.05,
                            'omega2': 10.0},
                        eta=0.001, truncation='2D')
    buildingblock = BuildingBlock(formula, df, qmax=3.0)

    buildingblock.calculate_building_block()
else:
    parprint('No precalculated ground state calculation found for ' + formula)