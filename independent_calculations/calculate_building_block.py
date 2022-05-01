def calculate_building_block(formula):
    from pathlib import Path
    from gpaw.mpi import world
    from gpaw.response.df import DielectricFunction
    from gpaw.response.qeh import BuildingBlock
    from ase.parallel import parprint

    out_dir = './out/'
    parprint('Calculating Building block for ' + formula)

    # chi
    df = DielectricFunction(calc=out_dir + 'gs_'+ formula + '_fulldiag.gpw',
                        eta=0.001,
                        domega0=0.05,
                        omega2=10.0,
                        nblocks=8,
                        ecut=150,
                        truncation='2D')

    buildingblock = BuildingBlock(formula, df, qmax=3.0)

    buildingblock.calculate_building_block()

    # if world.rank == 0:
    #     Path(formula + '_gs_fulldiag.gpw').unlink()

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    materials = ['BN', 'MoS2', 'MoSe2', 'MoTe2', 'WS2', 'WSe2', 'WTe2']
    for formula in materials:
        calculate_building_block(formula)