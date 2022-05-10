from ase.io import read
from ase.build import mx2
from ase.parallel import parprint
from gpaw import GPAW, PW, FermiDirac

def calculate_groundstate(formula, ecut = 500, no_kpts=30, vac=20, xc='PBE', T_e=0.01, nbands = 504):
    parprint('Calculating ground state for ' + formula)
    parprint('Parameters: ecut: ' + str(ecut) + ', no_kpts: ' + str(no_kpts) + ', vac: ' + str(vac) + ', xc: ' + xc + ', T_e: ' + str(T_e))

    # Load in structure and set vacuum to 20 Å.
    #structure = read('./structures/' + formula + '.json')
    #structure.center(vacuum=vac, axis=2)
    #structure.pbc = (1, 1, 1)
    # make structure as in the tutorial
    structure_params = {'MoS2': {'kind': '2H', 'a': 3.184, 'thickness': 3.127},
                       'MoSe2': {'kind': '2H', 'a': 3.320, 'thickness': 3.338},
                       'WS2': {'kind': '2H', 'a': 3.186, 'thickness': 3.359},
                       'WSe2': {'kind': '2H', 'a': 3.319, 'thickness': 3.146},
                       'BN': {'kind': '2H', 'a': 2.510, 'thickness': 1}}
    s = structure_params[formula]
    structure = mx2(formula=formula, kind=s['kind'], a=s['a'], thickness=s['thickness'],
                size=(1, 1, 1), vacuum=vac)
    
    out_dir = './out/'
    file_prefix = out_dir + formula + '_'+xc

    calc = GPAW(mode=PW(ecut),
                xc=xc,
                kpts={'size': (no_kpts, no_kpts, 1), 'gamma': True},
                occupations=FermiDirac(T_e),
                parallel={'domain': 1},
                txt=file_prefix + '_out.txt')

    structure.calc = calc
    structure.get_potential_energy()
    calc.write(file_prefix + '_gs.gpw')

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    #materials = ['BN', 'MoSe2', 'WTe2']
    #materials = ['MoS2']
    materials = ['MoS2','MoSe2','WS2','WSe2']
    #materials = ['WSe2']
    #materials = ['WS2']
    #materials = ['MoSe2']
    for formula in materials:
        calculate_groundstate(formula)