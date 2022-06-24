import numpy as np
from qeh import Heterostructure
from default_parameters import get_thickness, get_intermass
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

# %%
def get_exciton_binding_energies_coulomb(hs, eff_mass, L_min=-50, L_max=10,
                                     Delta=0.1, e_distr=None, h_distr=None,
                                     Wq_name=None, tweak=None):
                                     
        from scipy.linalg import eig
        r_space = np.arange(L_min, L_max, Delta)
        Nint = len(r_space)
        
        # EDIT THIS
        r, W_r = hs.get_exciton_screened_potential_r(r_array=np.exp(r_space),
                                                       e_distr=e_distr,
                                                       h_distr=h_distr,
                                                       Wq_name=None,
                                                       tweak=tweak)

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
def get_E_b_for_hs(hs, eff_mass, nFilling, nPadding):
    '''
    @returns: E_b
    '''
    Hartree = ase.units.Hartree
    Bohr = ase.units.Bohr

    # Exciton Screened Potential
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)

    # Exciton Binding Energies
    ee, ev = hs.get_exciton_binding_energies(eff_mass=eff_mass,
                                            e_distr=e_distr,
                                            h_distr=h_distr)
    
    # TODO: This is where we sohuld use our own function also
    # ee_2d_coulomb, ev_2d_coullomb = get_exciton_binding_energies_coulomb(...)
    
    E_b = -ee[0].real
    # Return in units of eV and Å.
    # Note: The units of V_ee and V_eh (in q-space) are unknown (we don't know the FT)
    return E_b

def calculate_and_save_binding_energies(materials_e,materials_h,e_avg_vec_iso,h_avg_vec_iso,default_thick, nPadding, nFilling):
    N_e = len(materials_e)
    N_h = len(materials_h)
    E_b_heat_mat = np.zeros((N_e,N_h))
    E_b_heat_ylabels = ['n-' + m for m in materials_e]
    E_b_heat_xlabels = ['p-' + m for m in materials_h]
    E_b = [[]]*N_e*N_h
    bilayer = [[]]*N_e*N_h

    count = 0
    for (i_e, e_layer) in enumerate(materials_e):
        for (i_h, h_layer) in enumerate(materials_h):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])
            print('{} out of {}'.format(count+1,N_e*N_h))

            eff_mass=1/(1/e_avg_vec_iso[i_e]+1/h_avg_vec_iso[i_h])

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            print(layers)
            try:
                d = [(get_thickness(l) + get_thickness(layers[i+1]))/2 for (i,l) in enumerate(layers[:-1])]
            except IndexError:
                print('Thickness not found')
                d=[0 for (i,l) in enumerate(layers[:-1])]
                for i,l in enumerate(layers[:-1]):
                    try:
                        d1=get_thickness(l)
                    except IndexError:
                        d1=default_thick
                    try:
                        d2=get_thickness(layers[i+1])
                    except IndexError:
                        d2=default_thick
                    d[i]=(d1+d2)/2

            hs = Heterostructure(structure=layers, d=d, include_dipole=True, wmax=0, qmax=1, d0=0)              

            E_b[count] = get_E_b_for_hs(hs, eff_mass, nFilling, nPadding)

            E_b_heat_mat[i_e, i_h] = E_b[count]
            count += 1
            #update labels
            try:
                d1=get_thickness(e_layer)
            except IndexError:
                E_b_heat_ylabels[i_e] = 'n-' + e_layer+'*'
            try:
                d1=get_thickness(h_layer)
            except IndexError:
                E_b_heat_xlabels[i_h] = 'p-' + h_layer+'*'
    
    np.savez('wannier_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) +'_default_thick'+str(default_thick)+ '.npz',
        bilayer=bilayer, E_b=E_b, E_b_heat_mat=E_b_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels)

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
    iNDEX1=5
    iNDEX2e=10
    iNDEX2h=10
    #iNDEX2e=len(e_avg_vec_iso)
    #iNDEX2h=len(h_avg_vec_iso)
    default_thick=5
    calculate_and_save_binding_energies(materials_e=materials_e[iNDEX1:iNDEX2e],materials_h=materials_h[iNDEX1:iNDEX2h],e_avg_vec_iso=e_avg_vec_iso[iNDEX1:iNDEX2e],h_avg_vec_iso=h_avg_vec_iso[iNDEX1:iNDEX2h], default_thick=default_thick,nPadding=0, nFilling=1)
