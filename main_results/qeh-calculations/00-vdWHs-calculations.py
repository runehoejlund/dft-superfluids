import numpy as np
from qeh import make_heterostructure
import ase.units
from default_parameters import get_thickness as get_default_thickness

'''
# Note on units:
- au means Hartree atomic units.
- When we save variables, we convert them from au to eV and Å
'''

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

def get_exciton_screened_potential_r_analytic(r_au, d_au):
    '''
    @returns: r_au [a.u.], U_eh_r_au [a.u.]
    @parameters:
        * r_au: real space array in atomic units (r [Å] / Bohr).
        * d_au: interlayer distance in atomic units (d [Å] / Bohr).
    '''
    eps2 = 2
    U_eh_r_au = -(1/eps2)*1/np.sqrt(r_au**2 + d_au**2)
    
    return r_au, U_eh_r_au

def get_exciton_screened_potential_q_analytic(q_au, d_au):
    '''
    @returns: U_ee, U_eh (in reciprocal space atomic units)
    @parameters:
        * q_au: reciprocal space array (momenta) in atomic units (q [1/Å] * Bohr).
        * d_ay: interlayer distance in atomic units (d [Å] / Bohr).
    '''
    eps2 = 2
    U_ee = (2*np.pi/eps2) * 1/np.abs(q_au)
    U_eh =  - U_ee * np.exp(-d_au*(q_au))
    return U_ee, U_eh

# %%
def get_E_b_analytic(eff_mass, r_au, d_au, L_min=-50, L_max=10, Delta=0.1):
    '''
    Calculates analytic exciton binding energy (i.e. using const. dielectric epsilon = 2)
    @returns: E_b [eV]
    '''
    from scipy.linalg import eig
    Nint = len(r_au)
    
    _, U_eh_r = get_exciton_screened_potential_r_analytic(r_au=r_au, d_au=d_au)

    H = np.zeros((Nint, Nint), dtype=complex)
    for i in range(0, Nint):
        r_abs = r_au[i]
        H[i, i] = - 1. / r_abs**2 / 2. / eff_mass \
            * (-2. / Delta**2 + 1. / 4.) + U_eh_r[i]
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

    E_b_au = - ee[0].real
    E_b = E_b_au * Hartree
    return E_b

def get_ab_initio_results(layers, thicknesses, eff_mass, r_au, nFilling, nPadding):
    '''
    @returns: E_b, q, omega, U_ee, U_eh, U_eh_r, epsM (in units of eV and Å)
    '''
    hs = make_heterostructure(layers=layers,
        thicknesses=thicknesses,
        frequencies=[0.00001, 0.00001, 1],
        momenta=[0.00002, 2, 400])

    # Electron and hole occupations (or is it spin distributions?)
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)

    # Dielectric Function
    q, omega, epsM = hs.get_macroscopic_dielectric_function()

    # Screened potential
    U_ee = hs.get_screened_potential(layer=nPadding)

    # Exciton Screened Potential
    _, U_eh, _ = hs.get_exciton_screened_potential(e_distr=e_distr, h_distr=h_distr)
    _, U_eh_r_au = hs.get_exciton_screened_potential_r(r_au, e_distr=e_distr, h_distr=h_distr)

    # Exciton Binding Energies
    ee, ev = hs.get_exciton_binding_energies(eff_mass=eff_mass, e_distr=e_distr, h_distr=h_distr)
    E_b = -ee[0].real
    # Return in units of eV and Å.
    # Note: The units of U_ee and U_eh (in q-space) are unknown (we don't know the FT)
    U_eh_r = U_eh_r_au * Hartree

    return E_b, q, omega, U_ee, U_eh, U_eh_r, epsM

def calculate_heterostructure_results(materials_e,materials_h,e_avg_vec_iso,h_avg_vec_iso, materials, material_thicknesses,nPadding, nFilling, use_cache = False):
    N_e = len(materials_e)
    N_h = len(materials_h)
    N = N_e*N_h

    def get_thickness(layer):
        try:
            return material_thicknesses[layer==materials][0]
        except:
            return get_default_thickness(layer)
    
    def get_distances():
        ts = [[]]*N # thicknesses
        ds = [[]]*N # interlayer distances

        count = 0
        for (i_e, e_layer) in enumerate(materials_e):
            for (i_h, h_layer) in enumerate(materials_h):
                layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
                ts[count] = np.array([get_thickness(layer) for layer in layers])
                # Calculate distance between layers
                interlayer_distances = 1/2*(ts[count][(nPadding+1):] + ts[count][:-(nPadding+1)])
                ds[count] = sum(interlayer_distances)
                count += 1
        return ts, ds
    
    if use_cache:
        vdWH_cached = np.load('00-cache.npz')
        q = vdWH_cached['q']
        omega=vdWH_cached['omega']
        E_b_heat_mat = vdWH_cached['E_b_heat_mat']
        E_b = vdWH_cached['E_b']
        epsM=vdWH_cached['epsM']
        U_ee = vdWH_cached['U_ee']
        U_eh = vdWH_cached['U_eh']
        U_eh_r = vdWH_cached['U_eh_r']
        q_au = q * Bohr
    else:
        E_b_heat_mat = np.zeros((N_e,N_h))
        E_b = [[]]*N
        epsM = [[]]*N
        U_ee = [[]]*N
        U_eh = [[]]*N
        U_eh_r = [[]]*N
    
    E_b_analytic_heat_mat = np.zeros((N_e,N_h))
    E_b_analytic_const_d_heat_mat = np.zeros((N_e,N_h))
    E_b_heat_ylabels = ['n-' + m for m in materials_e]
    E_b_heat_xlabels = ['p-' + m for m in materials_h]
    bilayers = [[]]*N
    E_b_analytic = [[]]*N
    epsM_analytic = [[]]*N
    U_ee_analytic = [[]]*N
    U_eh_analytic = [[]]*N
    U_eh_r_analytic = [[]]*N
    E_b_analytic_const_d = [[]]*N
    U_ee_analytic_const_d = [[]]*N
    U_eh_analytic_const_d = [[]]*N
    U_eh_r_analytic_const_d = [[]]*N

    # Set const. distance d0 as mean of all layer distances.
    thicknesses, distances = get_distances()
    d0 = np.mean(distances)
    d0_au = d0/Bohr
            
    # # Uncomment to set constant layer distance of d0 = 10 Å
    # # (instead of mean distance of all heterostructures)
    # d0 = 10
    # d0_au = d0/Bohr

    r_au = np.exp(np.arange(-50, 10, 0.1))
    r = r_au * Bohr

    count = 0
    for (i_e, e_layer) in enumerate(materials_e):
        for (i_h, h_layer) in enumerate(materials_h):
            bilayers[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayers[count])
            print('{} out of {}'.format(count+1,N))

            eff_mass=1/(1/e_avg_vec_iso[i_e]+1/h_avg_vec_iso[i_h])

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            print(layers)

            # Calculate and save ab initio results
            if not use_cache:
                E_b[count], q, omega, U_ee[count], U_eh[count], U_eh_r[count], epsM[count] = get_ab_initio_results(layers=layers,
                    thicknesses=thicknesses[count], eff_mass=eff_mass, r_au=r_au, nFilling=nFilling, nPadding=nPadding)
                q_au = q * Bohr
                E_b_heat_mat[i_e, i_h] = E_b[count]

            # Calculate and save analytic results
            epsM_analytic[count] = 2*np.ones(q.shape) # const. eps = 2
            d = distances[count]
            d_au = d/Bohr
            
            # Exciton binding energy
            E_b_analytic[count] = get_E_b_analytic(eff_mass=eff_mass, r_au=r_au, d_au=d_au)
            E_b_analytic_heat_mat[i_e, i_h] = E_b_analytic[count]
            E_b_analytic_const_d[count] = get_E_b_analytic(eff_mass=eff_mass, r_au=r_au, d_au=d0_au)
            E_b_analytic_const_d_heat_mat[i_e, i_h] = E_b_analytic_const_d[count]
            
            # Screened potential
            U_ee_analytic[count], U_eh_analytic[count] = get_exciton_screened_potential_q_analytic(q_au=q_au, d_au=d_au)
            U_ee_analytic_const_d[count], U_eh_analytic_const_d[count] = get_exciton_screened_potential_q_analytic(q_au=q_au, d_au=d0_au)
            #
            _, U_eh_r_analytic_au = get_exciton_screened_potential_r_analytic(r_au=r_au, d_au=d_au)
            U_eh_r_analytic[count] = U_eh_r_analytic_au * Hartree
            _, U_eh_r_analytic_const_d_au = get_exciton_screened_potential_r_analytic(r_au=r_au, d_au=d0_au)
            U_eh_r_analytic_const_d[count] = U_eh_r_analytic_const_d_au * Hartree
            count += 1
    
    # Save in units of eV and Å.
    # Note: The units of U_ee and U_eh (in q-space) are unknown (we don't know the FT)
    np.savez('../vdWH_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) + '.npz',
        bilayers=bilayers, thicknesses=thicknesses, distances=distances, d0=d0,
        r=r, q=q, omega=omega, epsM=epsM, epsM_analytic=epsM_analytic,
        E_b=E_b, E_b_analytic=E_b_analytic, E_b_analytic_const_d=E_b_analytic_const_d,
        E_b_heat_mat=E_b_heat_mat, E_b_analytic_heat_mat=E_b_analytic_heat_mat, E_b_analytic_const_d_heat_mat=E_b_analytic_const_d_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels,
        U_ee=U_ee, U_ee_analytic=U_ee_analytic, U_ee_analytic_const_d=U_ee_analytic_const_d,
        U_eh=U_eh, U_eh_analytic=U_eh_analytic, U_eh_analytic_const_d=U_eh_analytic_const_d,
        U_eh_r=U_eh_r, U_eh_r_analytic=U_eh_r_analytic, U_eh_r_analytic_const_d=U_eh_r_analytic_const_d)

if __name__ == '__main__':
    from os import path, chdir
    chdir(path.dirname(path.abspath(__file__)))
    
    # load materials
    out = np.load('../Materials_iso_stable.npz')
    h_iso = out['h_iso'].flatten()
    e_iso = out['e_iso'].flatten()
    Material_plot = out['Material_plot']
    materials_e = Material_plot[e_iso]
    materials_h = Material_plot[h_iso]
    e_avg_vec = out['e_avg_vec']
    h_avg_vec = out['h_avg_vec']
    e_avg_vec_iso = e_avg_vec[e_iso]
    h_avg_vec_iso = e_avg_vec[h_iso]
    materials = out['Mat_plot_iso']
    material_thicknesses = out['d_List']
    iNDEX1 = 0
    iNDEX2e = len(e_avg_vec_iso)
    iNDEX2h = len(h_avg_vec_iso)
    calculate_heterostructure_results(materials_e=materials_e[iNDEX1:iNDEX2e], 
        materials_h=materials_h[iNDEX1:iNDEX2h],e_avg_vec_iso=e_avg_vec_iso[iNDEX1:iNDEX2e],
        h_avg_vec_iso=h_avg_vec_iso[iNDEX1:iNDEX2h], materials=materials,
        material_thicknesses=material_thicknesses,
        nPadding=0, nFilling=1, use_cache=True)