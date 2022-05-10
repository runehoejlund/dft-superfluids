def calculate_building_block(formula, cleanup=False, ecut = 50, nblocks=24):
    from pathlib import Path
    from gpaw.mpi import world
    from gpaw.response.df import DielectricFunction
    from gpaw.response.qeh import BuildingBlock
    from ase.parallel import parprint

    out_dir = './out/'
    file_name = out_dir + 'gs_'+ formula + '_fulldiag.gpw'
    parprint('Calculating Building block for ' + formula)

    # chi
    df = DielectricFunction(calc=file_name,
                        frequencies={
                            'type': 'nonlinear',
                            'domega0': 0.05,
                            'omega2': 10.0},
                        ecut=ecut,
                        eta=0.001,
                        truncation='2D',
                        nblocks=nblocks)

    buildingblock = BuildingBlock(formula, df, qmax=3.0)

    buildingblock.calculate_building_block()

    if cleanup:
        # Uncomment to delete gpaw calculation when done.
        if world.rank == 0:
            Path(file_name).unlink()

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    materials = ['BN', 'MoS2', 'MoSe2', 'MoTe2', 'WS2', 'WSe2', 'WTe2']
    for formula in materials:
        calculate_building_block(formula)