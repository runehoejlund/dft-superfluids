from pathlib import Path
from gpaw.mpi import world
from gpaw.response.df import DielectricFunction
from gpaw.response.qeh import BuildingBlock
from ase.parallel import parprint
    
def calculate_building_block(formula, cleanup=False, ecut = 100, nblocks=24, eig_xc='PBE'):
    out_dir = './out/'
    file_prefix = out_dir + formula + '_xc=' + eig_xc
    file_name = file_prefix + '_fulldiag.gpw'
    parprint('Calculating Building block for ' + formula)

    # chi
    df = DielectricFunction(calc=file_name,
                        frequencies={
                            'type': 'nonlinear',
                            'domega0': 0.01,
                            'omega2': 35.0},
                        ecut=ecut,
                        eta=0.001,
                        nbands=400,
                        truncation='2D',
                        nblocks=nblocks)

    buildingblock = BuildingBlock(formula, df, qmax=3.0)

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
    if formula == 'BN':
        ecut = 150
    calculate_building_block(formula, ecut=ecut)
