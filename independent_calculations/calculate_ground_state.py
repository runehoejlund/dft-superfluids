from ase.io import read
from gpaw import GPAW, PW, FermiDirac
import numpy as np

def set_vacuum(structure, vac=20):
    lengths = structure.get_cell().lengths()
    lengths[np.argmax(lengths)] = vac
    structure.set_cell(lengths)
    structure.center()

def calculate_ground_state(formula, ecut = 600, no_kpts=30, vac=20, xc='LDA', T_e=0.01):
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
    # Load in structure and set vacuum to 20 Å.
    structure = read('../structures/' + formula + '.json')
    set_vacuum(structure, vac)
    structure.pbc = (1, 1, 1)

    out_dir = './out/'

    calc = GPAW(mode=PW(ecut),
                xc=xc,
                kpts={'size': (no_kpts, no_kpts, 1), 'gamma': True},
                occupations=FermiDirac(T_e),
                parallel={'domain': 1},
                txt=out_dir + 'gs_' + formula + '_out.txt')

    structure.calc = calc
    structure.get_potential_energy()

    calc.diagonalize_full_hamiltonian(nbands=500, expert=True)
    calc.write(out_dir + 'gs_'+ formula + '_fulldiag.gpw', 'all')

if __name__ == '__main__':
    materials = ['BN', 'MoS2', 'MoSe2', 'MoTe2', 'WS2', 'WSe2', 'WTe2']
    for formula in materials:
        print('calculating ground state for ' + formula)
        calculate_ground_state(formula)