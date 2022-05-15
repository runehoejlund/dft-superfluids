from pathlib import Path
from gpaw.mpi import world
from gpaw.response.df import DielectricFunction
from gpaw.response.qeh import BuildingBlock
from ase.parallel import parprint
    
def calculate_building_block(formula, cleanup=False, ecut = 100, nblocks=24, omega2=35.0, nbands=400, eig_xc='PBE', eig_no_kpts=30):
    out_dir = './out/'
    file_prefix = out_dir + formula + '_xc=' + eig_xc + '_no_kpts=' + str(eig_no_kpts)
    file_name = file_prefix + '_fulldiag.gpw'
    parprint('Calculating Building block for ' + formula)

    # chi
    df = DielectricFunction(calc=file_name,
                        frequencies={
                            'type': 'nonlinear',
                            'domega0': 0.01,
                            'omega2': omega2},
                        ecut=ecut,
                        eta=0.001,
                        nbands=nbands,
                        truncation='2D',
                        nblocks=nblocks)
    output_file = formula + '_ecut=' + str(ecut) + '_omega2=' + str(omega2) + '_nbands=' + str(nbands) + '_eig_xc=' + eig_xc + '_eig_no_kpts=' + str(eig_no_kpts)
    buildingblock = BuildingBlock(output_file, df, qmax=3.0)

    buildingblock.calculate_building_block()

    if cleanup:
        # Uncomment to delete gpaw calculation when done.
        if world.rank == 0:
            Path(file_name).unlink()

if __name__ == '__main__':
    import sys
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    formula = sys.argv[1]
    
    ecut = 100
    if len(sys.argv) > 2:
        ecut = sys.argv[2]
    
    eig_xc = 'PBE'
    if len(sys.argv) > 3:
        eig_xc = sys.argv[3]
    
    eig_no_kpts = 30
    if len(sys.argv) > 4:
        eig_no_kpts = sys.argv[4]

    calculate_building_block(formula, ecut=ecut, nblocks=40, nbands=120, eig_xc=eig_xc, eig_no_kpts=eig_no_kpts)
