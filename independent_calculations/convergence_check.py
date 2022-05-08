from ase.io import read
from ase.parallel import parprint
from gpaw import GPAW, PW, FermiDirac
import numpy as np
from itertools import chain

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def get_potential_energy(structure, name, ecut = 600, no_kpts=30, vac=20, xc='LDA', T_e=0.01):
    parprint('Calculating ground state with ecut: ' + str(ecut) + ', no_kpts: ' + str(no_kpts) + ', vac: ' + str(vac) + ', xc: ' + xc + ', T_e: ' + str(T_e))
    parprint('filename: ' + name)
    structure.center(vacuum=vac, axis=2)
    structure.pbc = (1, 1, 1)

    calc = GPAW(mode=PW(ecut),
                xc=xc,
                kpts={'size': (no_kpts, no_kpts, 1), 'gamma': True},
                occupations=FermiDirac(T_e),
                parallel={'domain': 1},
                txt='./out/' + name + '.txt')
    structure.calc = calc
    structure.get_potential_energy()
    calc.write('./out/' + name + '.gpw')

#%% BN
# formula = 'BN'
# structure = read('../structures/' + formula + '.json')
# xc = 'LDA'

# for ecut in range(100,1100,100):
#     get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'ecut=' + str(ecut) + '_' + formula + '_gs_out', ecut=ecut)

# for no_kpts in chain(range(1,5), range(5,85,5)):
#     get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'no_kpts=' + str(no_kpts) + '_' + formula + '_gs_out', no_kpts=no_kpts)

#%% MoS2
# formula = 'MoS2'
# structure = read('../structures/' + formula + '.json')
# xc = 'LDA'

# for ecut in range(100,1100,100):
#     get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'ecut=' + str(ecut) + '_' + formula + '_gs_out', ecut=ecut)

#%% WSe2
formula = 'WSe2'
structure = read('../structures/' + formula + '.json')

# for xc in ['LDA', 'PBE', 'HSE06']:
#     for ecut in range(100,1100,100):
#         get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'ecut=' +str(ecut) + '_' + formula + '_gs_out', xc=xc, ecut=ecut)

#     for vac in range(1,11,1):
#         get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'vac=' + str(vac) + '_' + formula + '_gs_out', vac=vac)

#     # for T_e in range(0.005, 0.205, 0.005):
#     #     get_potential_energy(structure, name='T_e=' + str(T_e) + '_' + formula + '_gs_out', T_e=T_e)

#     for no_kpts in chain(range(1,5), range(5,85,5)):
#         get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'no_kpts=' + str(no_kpts) + '_' + formula + '_gs_out', no_kpts=no_kpts)

for xc in ['HSE06']:
    for ecut in [100, 200, 400, 600]:
        get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'ecut=' +str(ecut) + '_' + formula + '_gs_out', xc=xc, ecut=ecut)

    # for vac in range(1,11,1):
    #     get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'vac=' + str(vac) + '_' + formula + '_gs_out', vac=vac)

    # for T_e in range(0.005, 0.205, 0.005):
    #     get_potential_energy(structure, name='T_e=' + str(T_e) + '_' + formula + '_gs_out', T_e=T_e)

    # for no_kpts in chain(range(1,5), range(5,85,5)):
    #     get_potential_energy(structure, name='xc=' + str(xc) + '_' + 'no_kpts=' + str(no_kpts) + '_' + formula + '_gs_out', no_kpts=no_kpts)