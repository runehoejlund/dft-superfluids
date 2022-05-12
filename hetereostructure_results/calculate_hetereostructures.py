import numpy as np
from qeh import Heterostructure
from default_parameters import get_thickness, get_intermass
import ase.units

def get_heterostructure_results(hs, e_layer, h_layer, nFilling, nPadding):
    '''
    @returns: E_b, q, r, omega, V_ee, V_eh, V_eh_r, epsM
    '''
    Hartree = ase.units.Hartree
    Bohr = ase.units.Bohr

    # Dielectric Function
    q, omega, epsM = hs.get_macroscopic_dielectric_function()

    # Screened potential
    V_ee = hs.get_screened_potential(layer=nPadding)

    # Exciton Screened Potential
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)
    _, V_eh, _ = hs.get_exciton_screened_potential(e_distr=e_distr, h_distr=h_distr)

    r = np.arange(-100, 100, 0.1)
    _, V_eh_r = hs.get_exciton_screened_potential_r(r, e_distr=e_distr, h_distr=h_distr)

    # Exciton Binding Energies
    ee, ev = hs.get_exciton_binding_energies(eff_mass=get_intermass('H-' + e_layer, 'H-' + h_layer),
                                            e_distr=e_distr,
                                            h_distr=h_distr)
    E_b = -ee[0].real
    # Return in units of eV and Å.
    # Note: The units of V_ee and V_eh (in q-space) are unknown (we don't know the FT)
    return E_b, q, r * Bohr, omega, V_ee * Hartree, V_eh * Hartree, V_eh_r * Hartree, epsM

def calculate_and_save_hs_results(materials, nPadding, nFilling):
    N = len(materials)
    E_b_heat_mat = np.zeros((N,N))
    E_b_heat_ylabels = ['n-' + m for m in materials]
    E_b_heat_xlabels = ['p-' + m for m in materials]
    E_b = [[]]*N**2
    V_ee = [[]]*N**2
    V_eh = [[]]*N**2
    V_eh_r = [[]]*N**2
    bilayer = [[]]*N**2
    epsM = [[]]*N**2

    count = 0
    for (i_e, e_layer) in enumerate(materials):
        for (i_h, h_layer) in enumerate(materials):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])

            # d_BN = get_thickness('BN')  # hBN-hBN distance#3.22 før
            # d_e_layer = get_thickness(e_layer)
            # d_e_BN = (d_BN+d_e_layer)/2  # MoS2-hBN distance
            # d_h_layer = get_thickness(h_layer)
            # d_h_BN = (d_BN+d_h_layer)/2  # WSe2-hBN distance
            # layers = ['{}BN'.format(nPadding), e_layer, '3BN', h_layer, '{}BN'.format(nPadding)]
            # d= [d_BN]*(nPadding-1) + [d_e_BN]*2 + [d_BN]*(nFilling-1) + [d_h_BN]*2 + [d_BN]*(nPadding-1)

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            d = [(get_thickness(l) + get_thickness(layers[i+1]))/2 for (i,l) in enumerate(layers[:-1])]

            hs = Heterostructure(structure=layers, d=d, include_dipole=True, wmax=0, qmax=1, d0=0)              

            E_b[count], q, r, omega, V_ee[count], V_eh[count], V_eh_r[count], epsM[count] = get_heterostructure_results(hs, e_layer, h_layer, nFilling, nPadding)
            E_b_heat_mat[i_e, i_h] = E_b[count]

            count += 1
    
    np.savez('vdWHs_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) + '.npz',
        bilayer=bilayer, E_b=E_b, E_b_heat_mat=E_b_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels,
        q=q, r=r, omega=omega, V_ee=V_ee, V_eh=V_eh, V_eh_r=V_eh_r, epsM=epsM)

def calculate_hetereostructures(materials, paddings = [0,1,2,3], fillings = [1, 2, 3, 4, 6, 8, 10]):
    nPadding = 0
    for nFilling in fillings:
        calculate_and_save_hs_results(materials, nPadding, nFilling)
    
    nFilling = 3
    for nPadding in paddings:
        calculate_and_save_hs_results(materials, nPadding, nFilling)

# def get_exciton_binding_energies_coulomb(hs, eff_mass, L_min=-50, L_max=10,
#                                      Delta=0.1, e_distr=None, h_distr=None,
#                                      Wq_name=None, tweak=None):
#         from scipy.linalg import eig
#         r_space = np.arange(L_min, L_max, Delta)
#         Nint = len(r_space)

#         r, W_r = hs.get_exciton_screened_potential_r(r_array=np.exp(r_space),
#                                                        e_distr=e_distr,
#                                                        h_distr=h_distr,
#                                                        Wq_name=None,
#                                                        tweak=tweak)

#         H = np.zeros((Nint, Nint), dtype=complex)
#         for i in range(0, Nint):
#             r_abs = np.exp(r_space[i])
#             H[i, i] = - 1. / r_abs**2 / 2. / eff_mass \
#                 * (-2. / Delta**2 + 1. / 4.) + W_r[i]
#             if i + 1 < Nint:
#                 H[i, i + 1] = -1. / r_abs**2 / 2. / eff_mass \
#                     * (1. / Delta**2 - 1. / 2. / Delta)
#             if i - 1 >= 0:
#                 H[i, i - 1] = -1. / r_abs**2 / 2. / eff_mass \
#                     * (1. / Delta**2 + 1. / 2. / Delta)

#         ee, ev = eig(H)
#         index_sort = np.argsort(ee.real)
#         ee = ee[index_sort]
#         ev = ev[:, index_sort]
#         return ee * Hartree, ev

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    calculate_hetereostructures(materials=['WS2','MoS2','WSe2','MoSe2'],paddings = [], fillings = [8, 10])
