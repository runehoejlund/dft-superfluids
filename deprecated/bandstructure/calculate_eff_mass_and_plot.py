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

emptybands=13

formula_List=['MoS2','MoSe2','WS2','WSe2']
sym_path_List=['KM','KG']
nP_List=[30,59]
eff_mass_Matrix=np.zeros((4,4))
for iLoop in range(len(formula_List)):
    for jLoop in range(2):
        #choose
        formula = formula_List[iLoop]
        vac = 20
        out_dir = './out/'
        name = out_dir + formula + '_PBE_gs.gpw'
        sym_path=sym_path_List[jLoop]
        nP=nP_List[jLoop]

        bs1=BandStructure.read('/home/niflheim/s183774/dft-superfluids/bandstructure/bsLoop_formula_'+formula+'_direction_'+sym_path+'_npoints_{}_emptybands_{}'.format(nP,emptybands)+'.json')
        #
        Nkpt=np.shape(bs1.energies)[1]
        kPath=bs1.path.kpts
        kDiff=kPath-kPath[0]
        DeltaK_mag=np.zeros((Nkpt))
        for i in range(Nkpt):
            DeltaK_mag[i]=np.sqrt((kPath[i,0]-kPath[0,0])**2+(kPath[i,1]-kPath[0,1])**2+(kPath[i,2]-kPath[0,2])**2)
        #
        energybands=bs1.energies[0]
        valenceBand=energybands[:,12]
        conductionBand=energybands[:,13]
        ##EFFECTIVE MASSES
        atomUnit_to_eV=Hartree
        Aang_to_atomUnit=1/Bohr
        DeltaK_quan=DeltaK_mag[1]
        Dev2_val=2*(valenceBand[1]-valenceBand[0])/DeltaK_quan**2
        Dev2_con=2*(conductionBand[1]-conductionBand[0])/DeltaK_quan**2
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
        plt.xlabel('Delta k')
        plt.ylabel('E [eV]')
        plt.title('Effective h-mass: {}'.format(m_eff_h))
        plt.savefig('/home/niflheim/s183774/dft-superfluids/bandstructure/plots/Loop_valFit_{}_sym_{}_npoints_{}_emptybands{}.svg'.format(formula,sym_path,nP,emptybands))
        plt.close()

        plt.plot(kVec,conVec,'r-*')
        plt.plot(kVec,par_con,'b-*')
        plt.legend(['Data','Parabolic'])
        plt.xlabel('Delta k')
        plt.ylabel('E [eV]')
        plt.title('Effective e-mass: {}'.format(m_eff_e))
        plt.savefig('/home/niflheim/s183774/dft-superfluids/bandstructure/plots/Loop_conFit_{}_sym_{}_npoints_{}_emptybands_{}.svg'.format(formula,sym_path,nP,emptybands))
        plt.close()
np.savez('effective masses', effMass=eff_mass_Matrix)
