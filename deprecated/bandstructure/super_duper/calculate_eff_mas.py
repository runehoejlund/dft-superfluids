#import important stuff
from gpaw import GPAW, PW, FermiDirac
from ase.io import read
from ase.spectrum.band_structure import BandStructurePlot
from ase.spectrum.band_structure import BandStructure
from ase.build import mx2
import numpy as np
import matplotlib.pyplot as plt
import ase.units
Hartree = ase.units.Hartree#Hartree energy
Bohr = ase.units.Bohr#Bohr radius
#make flot plot
from matplotlib import rcParams
rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern Roman"],
    "font.size": 16})
rcParams['axes.titlepad'] = 20 


emptybands=13

formula_List=['MoS2','MoSe2','WS2','WSe2']
sym_path_List=['KM','KG']
nP_List=[30,59]
eff_mass_Matrix=np.zeros((4,4))
for iLoop in range(len(formula_List)):
    for jLoop in range(len(sym_path_List)):
        #choose
        formula = formula_List[iLoop]
        ecut=500
        xc='PBE'
        no_kpts=30
        vac = 20
        out_dir = './out/'
        name = out_dir + formula + '_PBE_gs.gpw'
        sym_path=sym_path_List[jLoop]
        nP=nP_List[jLoop]

        #structure
        structure_params = {'MoS2': {'kind': '2H', 'a': 3.184, 'thickness': 3.127},
                       'MoSe2': {'kind': '2H', 'a': 3.320, 'thickness': 3.338},
                       'WS2': {'kind': '2H', 'a': 3.186, 'thickness': 3.359},
                       'WSe2': {'kind': '2H', 'a': 3.319, 'thickness': 3.146},
                       'BN': {'kind': '2H', 'a': 2.510, 'thickness': 1}}
        s = structure_params[formula]
        structure = mx2(formula=formula, kind=s['kind'], a=s['a'], thickness=s['thickness'],
                    size=(1, 1, 1), vacuum=vac)
        rec_cell=np.array(structure.cell.reciprocal()[:])*(2*np.pi)
        #
        bs1=BandStructure.read(out_dir+'bsLoop_formula_'+formula+'_direction_'+sym_path+'_npoints_{}_emptybands_{}'.format(nP,emptybands)+ '_'+xc+'_ecut_{}_kp_{}'.format(ecut,no_kpts)+'.json')
        #
        Nkpt=np.shape(bs1.energies)[1]
        kPath=bs1.path.kpts
        kPath0=np.matmul(rec_cell.transpose(),kPath[0])
        kDiff=kPath-kPath[0]
        DeltaK_mag=np.zeros((Nkpt))
        for i in range(Nkpt):
            kPathC=np.matmul(rec_cell.transpose(),kPath[i])
            DeltaK_mag[i]=np.sqrt((kPathC[0]-kPath0[0])**2+(kPathC[1]-kPath0[1])**2+(kPathC[2]-kPath0[2])**2)
        #
        energybands=bs1.energies[0]
        valenceBand=energybands[:,12]
        conductionBand=energybands[:,13]
        ##EFFECTIVE MASSES
        atomUnit_to_eV=Hartree
        Aang_to_atomUnit=1/Bohr
        DeltaK_quan=DeltaK_mag[1]
        Dev2_val=2*(valenceBand[1]-valenceBand[0])/(DeltaK_quan/Aang_to_atomUnit)**2
        Dev2_con=2*(conductionBand[1]-conductionBand[0])/(DeltaK_quan/Aang_to_atomUnit)**2
        #valenceBand=energybands[:,12]
        #conductionBand=energybands[:,13]
        m_eff_e=atomUnit_to_eV/Dev2_con
        m_eff_h=-atomUnit_to_eV/Dev2_val
        eff_mass_Matrix[iLoop,2*jLoop]=m_eff_e
        eff_mass_Matrix[iLoop,2*jLoop+1]=m_eff_h
        
        #apparently k is already in atomic units!!!
        def val_band(x,A1,m_eff_h):
            return A1-atomUnit_to_eV*(x)**2/(2*m_eff_h)
        def con_band(x,A1,m_eff_e):
            return A1+atomUnit_to_eV*(x)**2/(2*m_eff_e)
        
        #choose a cut off
        k_cut=100
        bool_k=DeltaK_mag<k_cut
        DeltaK_cut=DeltaK_mag[bool_k]
        valenceBand_cut=valenceBand[bool_k]
        conductionBand_cut=conductionBand[bool_k]
        #
        kVec=np.concatenate((-np.flip(DeltaK_cut),DeltaK_cut[1:]))
        valVec=np.concatenate((np.flip(valenceBand_cut),valenceBand_cut[1:]))
        conVec=np.concatenate((np.flip(conductionBand_cut),conductionBand_cut[1:]))
        par_val=val_band(kVec,valenceBand[0],m_eff_h)
        par_con=con_band(kVec,conductionBand[0],m_eff_h)
        #plots
        plt.plot(kVec,valVec,'r-*')
        plt.plot(kVec,par_val,'b-*')
        plt.legend(['Data','Parabolic'])
        plt.xlabel(r'$\Delta k\,\mathrm{[1/Å]}$')
        plt.ylabel(r'$E\,\mathrm{[eV]}$')
        plt.title(formula+'Path: '+sym_path+' Eff h-mass: {}'.format(np.round(m_eff_h,2)))
        plt.savefig('./plots/Loop_valFit_{}_sym_{}_npoints_{}_emptybands{}_ecut_{}_kp_{}.svg'.format(formula,sym_path,nP,emptybands,ecut,no_kpts))
        plt.close()

        plt.plot(kVec,conVec,'r-*')
        plt.plot(kVec,par_con,'b-*')
        plt.legend(['Data','Parabolic'])
        plt.xlabel(r'$\Delta k\,\mathrm{[1/Å]}$')
        plt.ylabel(r'$E\,\mathrm{[eV]}$')
        plt.title(formula+'Path: '+sym_path+' Eff e-mass: {}'.format(np.round(m_eff_e,2)))
        plt.savefig('./plots/Loop_conFit_{}_sym_{}_npoints_{}_emptybands_{}_ecut_{}_kp_{}.svg'.format(formula,sym_path,nP,emptybands,ecut,no_kpts))
        plt.close()
np.savez('effective masses'+'_npoints_{}_emptybands_{}'.format(nP,emptybands)+ '_'+xc+'_ecut_{}_kp_{}'.format(ecut,no_kpts)+'.npz', effMass=eff_mass_Matrix)
