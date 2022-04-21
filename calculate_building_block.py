def calculate_building_block(formula):
    from pathlib import Path
    from gpaw.mpi import world
    from gpaw.response.df import DielectricFunction
    from gpaw.response.qeh import BuildingBlock

    # chi
    df = DielectricFunction(calc=formula + '_gs_fulldiag.gpw',
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