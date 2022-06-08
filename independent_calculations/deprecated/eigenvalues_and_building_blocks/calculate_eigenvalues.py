from ase.io import read
from ase.parallel import parprint
from gpaw import GPAW, PW, FermiDirac
import numpy as np

def calculate_eigenvalues(formula, ecut = 500, no_kpts=30, vac=20, xc='PBE', T_e=0.01, nbands = 504):
    parprint('Calculating ground state for ' + formula)
    parprint('Parameters: ecut: ' + str(ecut) + ', no_kpts: ' + str(no_kpts) + ', vac: ' + str(vac) + ', xc: ' + xc + ', T_e: ' + str(T_e))

    # Load in structure and set vacuum to 20 Å.
    structure = read('../structures/' + formula + '.json')
    structure.center(vacuum=vac, axis=2)
    structure.pbc = (1, 1, 1)

    out_dir = './out/'
    file_prefix = out_dir + formula + '_xc=' + xc

    calc = GPAW(mode=PW(ecut),
                xc=xc,
                kpts={'size': (no_kpts, no_kpts, 1), 'gamma': True},
                occupations=FermiDirac(T_e),
                parallel={'domain': 1},
                txt=file_prefix + '_out.txt')

    structure.calc = calc
    structure.get_potential_energy()
    calc.write(file_prefix + '_gs.gpw', 'all')

    calc.diagonalize_full_hamiltonian(nbands=nbands, expert=True)
    calc.write(file_prefix + '_fulldiag.gpw', 'all')

if __name__ == '__main__':
    import sys
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    formula = sys.argv[1]
    ecut = 500
    if formula == 'BN':
        ecut = 800
    calculate_eigenvalues(formula, ecut=ecut)
