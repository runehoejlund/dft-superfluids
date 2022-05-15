import numpy as np
from qeh import Heterostructure
from default_parameters import get_thickness, get_intermass
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

def get_E_b_for_hs(hs, e_layer, h_layer, nFilling, nPadding, i_e, i_h):
    '''
    @returns: E_b
    '''
    # effective masses from article
    me_vec=np.array([0.33,0.40,0.36,0.43])
    mh_vec=np.array([0.30,0.48,0.30,0.50])

    # # effective masses that we use
    # me_vec=np.array([0.33,0.43,0.39,0.49])
    # mh_vec=np.array([0.34,0.53,0.36,0.58])

    mu_matrix=np.zeros((4,4))
    for ie in range(4):
        for jh in range(4):
            mu_matrix[ie,jh]=1/(1/me_vec[ie]+1/mh_vec[jh])

    # Exciton Screened Potential
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)

    # Exciton Binding Energies
    ee, ev = hs.get_exciton_binding_energies(mu_matrix[i_e,i_h], e_distr=e_distr, h_distr=h_distr)
    
    E_b = -ee[0].real
    print(np.round(E_b,3)*10**3)
    # Return in units of eV and Å.
    # Note: The units of V_ee and V_eh (in q-space) are unknown (we don't know the FT)
    return E_b

def calculate_and_save_binding_energies(materials, nPadding, nFilling):
    N = len(materials)
    E_b_heat_mat = np.zeros((N,N))
    E_b_heat_ylabels = ['n-' + m for m in materials]
    E_b_heat_xlabels = ['p-' + m for m in materials]
    E_b = [[]]*N**2
    bilayer = [[]]*N**2

    count = 0
    for (i_e, e_layer) in enumerate(materials):
        for (i_h, h_layer) in enumerate(materials):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            d = [(get_thickness(l) + get_thickness(layers[i+1]))/2 for (i,l) in enumerate(layers[:-1])]

            hs = Heterostructure(structure=layers, d=d, include_dipole=True, wmax=0, qmax=1, d0=0)
                       
            E_b[count] = get_E_b_for_hs(hs, e_layer, h_layer, nFilling, nPadding,i_e,i_h)
            E_b_heat_mat[i_e, i_h] = E_b[count]

            count += 1
    
    np.savez('wannier_qeh_article_masses_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) + '.npz',
        bilayer=bilayer, E_b=E_b, E_b_heat_mat=E_b_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels)

if __name__ == '__main__':
   import os
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)
   
   calculate_and_save_binding_energies(materials=['WS2','MoS2','WSe2','MoSe2'], nPadding=0, nFilling=3)
