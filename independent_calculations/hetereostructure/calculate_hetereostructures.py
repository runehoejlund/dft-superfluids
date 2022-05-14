import numpy as np
from qeh import Heterostructure
from default_parameters import get_thickness, get_intermass
import ase.units

def get_heterostructure_results(hs, e_layer, h_layer, nFilling, nPadding):
    '''
    @returns: E_b, q, r, omega, U_ee, U_eh, U_eh_r, epsM
    '''
    Hartree = ase.units.Hartree
    Bohr = ase.units.Bohr

    # Dielectric Function
    q, omega, epsM = hs.get_macroscopic_dielectric_function()

    # Screened potential
    U_ee = hs.get_screened_potential(layer=nPadding)

    # Exciton Screened Potential
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)
    _, U_eh, _ = hs.get_exciton_screened_potential(e_distr=e_distr, h_distr=h_distr)

    r = np.exp(np.arange(-50, 10, 0.1))
    _, U_eh_r = hs.get_exciton_screened_potential_r(r, e_distr=e_distr, h_distr=h_distr)

    # Exciton Binding Energies
    ee, ev = hs.get_exciton_binding_energies(eff_mass=get_intermass('H-' + e_layer, 'H-' + h_layer),
                                            e_distr=e_distr,
                                            h_distr=h_distr)
    E_b = -ee[0].real
    # Return in units of eV and Å.
    # Note: The units of U_ee and U_eh (in q-space) are unknown (we don't know the FT)
    return E_b, q, r * Bohr, omega, U_ee, U_eh, U_eh_r * Hartree, epsM

def calculate_and_save_hs_results(materials, nPadding, nFilling):
    N = len(materials)
    E_b_heat_mat = np.zeros((N,N))
    E_b_heat_ylabels = ['n-' + m for m in materials]
    E_b_heat_xlabels = ['p-' + m for m in materials]
    E_b = [[]]*N**2
    U_ee = [[]]*N**2
    U_eh = [[]]*N**2
    U_eh_r = [[]]*N**2
    bilayer = [[]]*N**2
    epsM = [[]]*N**2

    count = 0
    for (i_e, e_layer) in enumerate(materials):
        for (i_h, h_layer) in enumerate(materials):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            d = [(get_thickness(l) + get_thickness(layers[i+1]))/2 for (i,l) in enumerate(layers[:-1])]

            hs = Heterostructure(structure=layers, d=d, include_dipole=True, wmax=0, qmax=1, d0=0)              

            E_b[count], q, r, omega, U_ee[count], U_eh[count], U_eh_r[count], epsM[count] = get_heterostructure_results(hs, e_layer, h_layer, nFilling, nPadding)
            E_b_heat_mat[i_e, i_h] = E_b[count]

            count += 1
    
    np.savez('independent_vdWHs_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) + '.npz',
        materials=materials, bilayer=bilayer, E_b=E_b, E_b_heat_mat=E_b_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels,
        q=q, r=r, omega=omega, U_ee=U_ee, U_eh=U_eh, U_eh_r=U_eh_r, epsM=epsM)

def calculate_hetereostructures(materials, paddings = [0,1,2,3], fillings = [1, 2, 3, 4, 6, 8, 10]):
    nPadding = 0
    for nFilling in fillings:
        calculate_and_save_hs_results(materials, nPadding, nFilling)
    
    nFilling = 3
    for nPadding in paddings:
        calculate_and_save_hs_results(materials, nPadding, nFilling)

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    calculate_hetereostructures(materials=['WS2', 'WSe2','MoTe2'])
