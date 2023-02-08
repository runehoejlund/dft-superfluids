import numpy as np
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

def calculate_and_save_dat(nPadding=0, nFilling=1):
    qeh_data = np.load('qeh_data_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) + '.npz')
    bilayers = [b.replace(', ', '_') for b in qeh_data['bilayers']]
    q = qeh_data['q']
    q_au = q * Bohr
    N_q = len(q_au)

    print([k for k in qeh_data.keys()])

    N_bilayers = len(bilayers)
    for i, bilayer in enumerate(bilayers):
        print(str(i+1) + ' out of ' + str(N_bilayers))
        with open('./out/' + bilayer + '_QEH.dat', 'w') as dat_file:
            dat_file.write(str(N_q))
            U_eh = np.real(qeh_data['U_eh'][i].flatten())
            U_ee = np.real(qeh_data['U_ee'][i].flatten())
            U_hh = np.real(qeh_data['U_hh'][i].flatten())

            for j in range(N_q):
                dat_file.write('\n'+str(q_au[j])+' '+str(U_eh[j])+' '+str(U_ee[j])+' '+str(U_hh[j]))
        
        with open('./out/' + bilayer + '_analytic.dat', 'w') as dat_file:
            dat_file.write(str(N_q))
            U_eh = qeh_data['U_eh_analytic'][i]
            U_ee = qeh_data['U_ee_analytic'][i]
            U_hh = qeh_data['U_hh_analytic'][i]

            for j in range(N_q):
                dat_file.write('\n'+str(q_au[j])+' '+str(U_eh[j])+' '+str(U_ee[j])+' '+str(U_hh[j]))


if __name__ == '__main__':
    from os import path, chdir
    chdir(path.dirname(path.abspath(__file__)))

    calculate_and_save_dat(nPadding=0, nFilling=1)