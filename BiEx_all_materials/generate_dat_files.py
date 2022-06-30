import numpy as np
from qeh import Heterostructure
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

# %%

def calculate_and_save_dat(materials_e,materials_h,e_avg_vec_iso,h_avg_vec_iso,Mat_plot_iso,d_List,nPadding, nFilling):
    N_e = len(materials_e)
    N_h = len(materials_h)
    bilayer = [[]]*N_e*N_h
    count=0
    for (i_e, e_layer) in enumerate(materials_e):
        for (i_h, h_layer) in enumerate(materials_h):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])
            print('{} out of {}'.format(count+1,N_e*N_h))

            eff_mass=1/(1/e_avg_vec_iso[i_e]+1/h_avg_vec_iso[i_h])

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            print(layers)
            d=[]
            for  (i,l) in enumerate(layers[:-1]):
                if l=='BN':
                    d1=3.33
                else:
                    d1=d_List[l==Mat_plot_iso][0]
                if layers[i+1]=='BN':
                    d2=3.33
                else:
                    d2=d_List[layers[i+1]==Mat_plot_iso][0]
                d.append((d1+d2)/2)
            print(d)

            hs = Heterostructure(structure=layers, d=d, include_dipole=True, wmax=0, qmax=1, d0=0)              

            #Other stuff, taken from heterostructureresults/calculate_heterostructure
            e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
            h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)
            # Dielectric Function
            q, omega, epsM = hs.get_macroscopic_dielectric_function()
            #e-e interaction, Screened potential
            U_ee = hs.get_screened_potential(layer=0).flatten()
            #h-h interaction, Screened potential
            U_hh = hs.get_screened_potential(layer=2).flatten()
            # e-h interaction, Screened potential
            _, U_eh, _ = hs.get_exciton_screened_potential(e_distr=e_distr, h_distr=h_distr)
            #U_ee and hh has a small complex part, which we just ignore
            U_ee=np.real(U_ee)
            U_hh=np.real(U_hh)

            rows=len(q)
            print(np.shape(U_eh))
            print(np.shape(U_ee))
            with open(+'n-' + e_layer + '_' + 'p-' + h_layer+'.dat', 'w') as your_dat_file:
                your_dat_file.write(str(rows))
                for i in range(rows):
                    your_dat_file.write('\n'+str(q[i])+' '+str(U_eh[i])+' '+str(U_ee[i])+' '+str(U_hh[i]))
            count+=1


                 
    
    
if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    #out=np.load()
    #materials=out['materials']
    import numpy as np
    #load materials
    out=np.load('./Materials_iso_stable.npz')
    materials=out['materials']
    h_iso=out['h_iso'].flatten()
    e_iso=out['e_iso'].flatten()
    Material_plot=out['Material_plot']
    materials_e=Material_plot[e_iso]
    materials_h=Material_plot[h_iso]
    e_avg_vec=out['e_avg_vec']
    h_avg_vec=out['h_avg_vec']
    e_avg_vec_iso=e_avg_vec[e_iso]
    h_avg_vec_iso=e_avg_vec[h_iso]
    Mat_plot_iso=out['Mat_plot_iso']
    d_List=out['d_List']
    iNDEX1=0
    iNDEX2e=1
    iNDEX2h=1
    iNDEX2e=len(e_avg_vec_iso)
    iNDEX2h=len(h_avg_vec_iso)
    calculate_and_save_dat(materials_e=materials_e[iNDEX1:iNDEX2e],materials_h=materials_h[iNDEX1:iNDEX2h],e_avg_vec_iso=e_avg_vec_iso[iNDEX1:iNDEX2e],h_avg_vec_iso=h_avg_vec_iso[iNDEX1:iNDEX2h], Mat_plot_iso=Mat_plot_iso,d_List=d_List,nPadding=0, nFilling=1)