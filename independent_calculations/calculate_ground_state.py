def calculate_ground_state(formula):
    ''' Calculates ground state gpw file for specified material.

    @parameters:
    formula: str
        Chemical formula corresponding to name of json-file (without json-extension) in structures directory.
    '''
    from ase.io import read
    from gpaw import GPAW, PW, FermiDirac
    import numpy as np
    
    # Load in structure and set vacuum to 20 Å.
    structure = read('./structures/' + formula + '.json')
    lengths = structure.get_cell().lengths()
    lengths[np.argmax(lengths)] = 20
    structure.set_cell(lengths)
    structure.center()
    # structure.pbc = (1, 1, 1)

    ecut = 600

    calc = GPAW(mode=PW(ecut),
                xc='LDA',
                kpts={'size': (30, 30, 1), 'gamma': True},
                occupations=FermiDirac(0.01),
                parallel={'domain': 1},
                txt=formula + '_gs_out.txt')

    structure.calc = calc
    structure.get_potential_energy()

    calc.diagonalize_full_hamiltonian(nbands=500, expert=True)
    calc.write(formula + '_gs_fulldiag.gpw', 'all')