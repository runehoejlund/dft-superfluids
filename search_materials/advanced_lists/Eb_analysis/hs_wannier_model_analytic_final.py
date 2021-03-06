import numpy as np
from qeh import Heterostructure
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

def get_exciton_screened_potential_r_analytic(r_array,d):
    #d0=10/Bohr #use this for the same thickness. Remember then to change the name of the output file
    d0=sum(d)/Bohr #use this for the varying thickness
    print(d0*Bohr)
    eps2=2
    W_r=-(1/eps2)*1/np.sqrt(r_array**2+d0**2)
    
    return r_array, W_r

def get_exciton_binding_energies_coulomb(eff_mass, L_min=-50, L_max=10,
                                     Delta=0.1, e_distr=None, h_distr=None,
                                     Wq_name=None, tweak=None,d=10):
                                     
        from scipy.linalg import eig
        r_space = np.arange(L_min, L_max, Delta)
        Nint = len(r_space)
        
        # EDIT THIS
        r, W_r = get_exciton_screened_potential_r_analytic(r_array=np.exp(r_space),d=d)

        H = np.zeros((Nint, Nint), dtype=complex)
        for i in range(0, Nint):
            r_abs = np.exp(r_space[i])
            H[i, i] = - 1. / r_abs**2 / 2. / eff_mass \
                * (-2. / Delta**2 + 1. / 4.) + W_r[i]
            if i + 1 < Nint:
                H[i, i + 1] = -1. / r_abs**2 / 2. / eff_mass \
                    * (1. / Delta**2 - 1. / 2. / Delta)
            if i - 1 >= 0:
                H[i, i - 1] = -1. / r_abs**2 / 2. / eff_mass \
                    * (1. / Delta**2 + 1. / 2. / Delta)

        ee, ev = eig(H)
        index_sort = np.argsort(ee.real)
        ee = ee[index_sort]
        ev = ev[:, index_sort]
        return ee * Hartree, ev

# %% OUR OWN FUNCTIONS
def get_E_b_for_hs(eff_mass, nFilling, nPadding,d):
    '''
    @returns: E_b
    '''
    Hartree = ase.units.Hartree
    Bohr = ase.units.Bohr

    # Exciton Screened Potential
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)

    # Exciton Binding Energies
    ee, ev = get_exciton_binding_energies_coulomb(eff_mass=eff_mass,
                                            e_distr=e_distr,
                                            h_distr=h_distr,d=d)
    
    # TODO: This is where we sohuld use our own function also
    # ee_2d_coulomb, ev_2d_coullomb = get_exciton_binding_energies_coulomb(...)
    
    E_b = -ee[0].real
    # Return in units of eV and ??.
    # Note: The units of V_ee and V_eh (in q-space) are unknown (we don't know the FT)
    return E_b

def calculate_and_save_binding_energies(materials_e,materials_h,e_avg_vec_iso,h_avg_vec_iso,Mat_plot_iso,d_List,bandgap_vec,nPadding, nFilling):
    N_e = len(materials_e)
    N_h = len(materials_h)
    E_b_heat_mat = np.zeros((N_e,N_h))
    E_b_heat_ylabels = ['n-' + m for m in materials_e]
    E_b_heat_xlabels = ['p-' + m for m in materials_h]
    E_b = [[]]*N_e*N_h
    effmass_Matrix=np.zeros((N_e,N_h))
    d0_Matrix=np.zeros((N_e,N_h))
    avgBandgap_Matrix=np.zeros((N_e,N_h))
    bilayer = [[]]*N_e*N_h

    count = 0
    for (i_e, e_layer) in enumerate(materials_e):
        for (i_h, h_layer) in enumerate(materials_h):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])
            #print(N_e,N_h)
            print('{} out of {}'.format(count+1,N_e*N_h))

            eff_mass=1/(1/e_avg_vec_iso[i_e]+1/h_avg_vec_iso[i_h])
            effmass_Matrix[i_e,i_h]=eff_mass

            avgBandgap_Matrix[i_e, i_h] = (bandgap_vec[e_layer==Mat_plot_iso]+bandgap_vec[h_layer==Mat_plot_iso])/2
            print(avgBandgap_Matrix[i_e, i_h])
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

            E_b[count] = get_E_b_for_hs(eff_mass, nFilling, nPadding,d)

            E_b_heat_mat[i_e, i_h] = E_b[count]
            d0_Matrix[i_e, i_h] =sum(d)
            count += 1
            
    
    np.savez('wannier_analytic_varying_thickness_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding)+'.npz',
        bilayer=bilayer, E_b=E_b, E_b_heat_mat=E_b_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels,effmass_Matrix=effmass_Matrix,d0_Matrix=d0_Matrix,avgBandgap_Matrix=avgBandgap_Matrix)

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    #out=np.load()
    #materials=out['materials']
    import numpy as np
    #load materials
    out=np.load('../Materials_iso_stable.npz')
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
    bandgap_vec=out['bandgap_iso']
    iNDEX1=0
    iNDEX2e=len(e_avg_vec_iso)
    iNDEX2h=len(h_avg_vec_iso)
    calculate_and_save_binding_energies(materials_e=materials_e[iNDEX1:iNDEX2e],materials_h=materials_h[iNDEX1:iNDEX2h],e_avg_vec_iso=e_avg_vec_iso[iNDEX1:iNDEX2e],h_avg_vec_iso=h_avg_vec_iso[iNDEX1:iNDEX2h], Mat_plot_iso=Mat_plot_iso,d_List=d_List,bandgap_vec=bandgap_vec,nPadding=0, nFilling=1)
