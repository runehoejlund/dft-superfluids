from ase.io import read
from gpaw import GPAW, PW, FermiDirac
import numpy as np

formula = 'BN'

# Load in structure and set vacuum to 20 Å.
structure = read('../structures/' + formula + '.json')

def set_vacuum(structure, vac=20):
    lengths = structure.get_cell().lengths()
    lengths[-1] = vac
    structure.set_cell(lengths)
    structure.center()

def get_potential_energy(name, ecut = 600, no_kpts=30, vac=20, xc='LDA', T_e=0.01):
    set_vacuum(structure, vac)
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

# for ecut in range(100,1100,100):
#     get_potential_energy(name='ecut=' + str(ecut) + '_' + formula + '_gs_out', ecut=ecut)

# for vac in range(2,22,2):
#     get_potential_energy(name='vac=' + str(vac) + '_' + formula + '_gs_out', vac=vac)

for xc in ['LDA', 'PBE', 'RPBE']:
    get_potential_energy(name='xc=' + str(xc) + '_' + formula + '_gs_out', xc=xc)

for T_e in range(0.005, 0.205, 0.005):
    get_potential_energy(name='T_e=' + str(T_e) + '_' + formula + '_gs_out', T_e=T_e)

for no_kpts in range(1,10,1):
    get_potential_energy(name='no_kpts=' + str(no_kpts) + '_' + formula + '_gs_out', no_kpts=no_kpts)
