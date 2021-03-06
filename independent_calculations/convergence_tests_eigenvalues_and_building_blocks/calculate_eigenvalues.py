from ase.io import read
from ase.parallel import parprint
from gpaw import GPAW, PW, FermiDirac
import numpy as np

def calculate_eigenvalues(formula, ecut = 500, no_kpts=30, vac=20, xc='LDA', T_e=0.01, nbands = 520):
    ''' Calculates ground state gpw file for specified material.

    @parameters:
    formula: str
        Chemical formula corresponding to name of json-file (without json-extension) in structures directory.
    ecut: int
        Plane Wave Basis Energy cutoff
    no_kpts: int
        Number of k-pts in x- and y-direction
    vac: float 
        Vacuum in Ångstrom in out of plane direction
    xc: str
        Exchange Correlation Functional
    T_e: float
        Electron temperature in eV used for fermi-smearing
    '''
    parprint('Calculating ground state for ' + formula)
    parprint('Parameters: ecut: ' + str(ecut) + ', no_kpts: ' + str(no_kpts) + ', vac: ' + str(vac) + ', xc: ' + xc + ', T_e: ' + str(T_e))

    # Load in structure and set vacuum to 20 Å.
    structure = read('../structures/' + formula + '.json')
    structure.center(vacuum=vac, axis=2)
    structure.pbc = (1, 1, 1)

    out_dir = './out/'
    file_prefix = out_dir + formula

    calc = GPAW(mode=PW(ecut),
                xc=xc,
                kpts={'size': (no_kpts, no_kpts, 1), 'gamma': True},
                occupations=FermiDirac(T_e),
                parallel={'domain': 1},
                txt=file_prefix + '_out.txt')

    structure.calc = calc
    structure.get_potential_energy()
    calc.write(file_prefix + '_gs.pgw', 'all')

    calc.diagonalize_full_hamiltonian(nbands=nbands, expert=True)
    calc.write(file_prefix + '_fulldiag.gpw', 'all')

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    materials = ['BN', 'MoS2', 'MoSe2', 'MoTe2', 'WS2', 'WSe2', 'WTe2']
    for formula in materials:
        calculate_eigenvalues(formula)
