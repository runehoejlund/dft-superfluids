formula = 'WS2'

from gpaw import GPAW, PW, FermiDirac
from ase.io import read

out_dir = './out/'
name = out_dir + 'gs_'+ formula + '_fulldiag.gpw'

calc = GPAW(name)
calc.fixed_density(
    eigensolver='dav',
    nbands=24,
    symmetry='off',
    kpts={'size': (30, 30, 1), 'gamma': True},
    convergence={'bands': 6})

bs = calc.band_structure()
bs.plot(filename='bandstructure.png', show=True, emax=10.0)
bs.plot(filename='bandstructure.pdf', show=True, emax=10.0)