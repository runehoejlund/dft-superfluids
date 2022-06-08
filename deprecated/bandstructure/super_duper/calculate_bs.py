#import important stuff
from gpaw import GPAW, PW, FermiDirac
from ase.io import read
from ase.spectrum.band_structure import BandStructurePlot
from ase.build import mx2
import numpy as np
import matplotlib.pyplot as plt

#structure parameters
structure_params = {'MoS2': {'kind': '2H', 'a': 3.184, 'thickness': 3.127},
                       'MoSe2': {'kind': '2H', 'a': 3.320, 'thickness': 3.338},
                       'WS2': {'kind': '2H', 'a': 3.186, 'thickness': 3.359},
                       'WSe2': {'kind': '2H', 'a': 3.319, 'thickness': 3.146},
                       'BN': {'kind': '2H', 'a': 2.510, 'thickness': 1}}

formula_List=['MoS2','MoSe2','WS2','WSe2']
sym_path_List=['KM','KG']
nP_List=[30,59]

vac = 20
out_dir = './out/'
xc='PBE'
ecut=500
no_kpts=30

for i in range(len(formula_List)):
    for j in range(len(sym_path_List)):
        #choose
        formula = formula_List[i]

        name = out_dir + formula + '_'+xc+'_ecut_{}_kp_{}'.format(ecut,no_kpts)+ '_gs_rec_latt.gpw'
        sym_path=sym_path_List[j]
        nP=nP_List[j]

        #build structure
        s = structure_params[formula]
        structure = mx2(formula=formula, kind=s['kind'], a=s['a'], thickness=s['thickness'],
                    size=(1, 1, 1), vacuum=vac)
        
        
        #choose path in kspace and load converged density
        kpts = structure.cell.bandpath(path=sym_path, npoints=nP,
                                   pbc=structure.pbc, eps=0.1)#what was eps??
        calc = GPAW(name)
        #calculate bandstructure
        emptybands=26
        convbands = emptybands // 2
        parms = {
            'basis': 'dzp',
            'nbands': -emptybands,
            'txt': 'bs.txt',
            'fixdensity': True,
            'kpts': kpts,
            'convergence': {
                'bands': -convbands},
            'symmetry': 'off'}
        calc = GPAW(name, **parms)
        calc.get_potential_energy()
        #save bandstructure
        bs = calc.band_structure()
        bs.write(out_dir+'bsLoop_formula_'+formula+'_direction_'+sym_path+'_npoints_{}_emptybands_{}'.format(nP,emptybands)+ '_'+xc+'_ecut_{}_kp_{}'.format(ecut,no_kpts)+'.json')