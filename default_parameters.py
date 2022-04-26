from numpy import mean

_default_ehmasses = {'BPx': {'emass1': [0.17, 1.12], 'hmass1': [0.15, 6.35]},
                    'BPy': {'emass1': [0.17, 1.12], 'hmass1': [0.15, 6.35]},
                    'H-CrO2-NM': {'emass1': 0.875, 'hmass1': 1.442},
                    'H-CrS2-NM': {'emass1': 0.872, 'hmass1': 0.883},
                    'H-CrSe2-NM': {'emass1': 0.936, 'hmass1': 0.955},
                    'H-CrTe2-NM': {'emass1': 0.855, 'hmass1': 0.9},
                    'H-HfS2-NM': {'emass1': 1.255, 'hmass1': 2.653},
                    'H-HfSe2-NM': {'emass1': 1.351, 'hmass1': 3.108},
                    'H-HfTe2-NM': {'emass1': 1.722, 'hmass1': 0.612},
                    'H-MoO2-NM': {'emass1': 0.419, 'hmass1': 0.764},
                    'H-MoS2-NM': {'emass1': 0.427, 'hmass1': 0.53},
                    'MoSSe': {'emass1': 0.48, 'hmass1': 0.60},
                    'H-MoSe2-NM': {'emass1': 0.492, 'hmass1': 0.583},
                    'H-MoTe2-NM': {'emass1': 0.493, 'hmass1': 0.597},
                    'H-PbS2-NM': {'emass1': 0.386, 'hmass1': 0.618},
                    'H-PbSe2-NM': {'emass1': 0.281, 'hmass1': 0.418},
                    'H-PdSe2-NM': {'emass1': 1.241, 'hmass1': 0.333},
                    'H-ScO2-FM': {'emass1': 2.94, 'hmass1': 10.669},
                    'H-ScS2-FM': {'emass1': 4.018, 'hmass1': 5.235},
                    'H-ScSe2-FM': {'emass1': 0.0, 'hmass1': 4.261},
                    'H-SnO2-NM': {'emass1': 0.282, 'hmass1': 7.291},
                    'H-SnS2-NM': {'emass1': 0.656, 'hmass1': 0.482},
                    'H-TiS2-NM': {'emass1': 0.0, 'hmass1': 2.585},
                    'H-TiSe2-NM': {'emass1': 0.0, 'hmass1': 1.654},
                    'H-VSe2-FM': {'emass1': 2.157, 'hmass1': 0.801},
                    'H-VTe2-FM': {'emass1': 3.332, 'hmass1': 1.105},
                    'H-WO2-NM': {'emass1': 0.346, 'hmass1': 0.781},
                    'H-WS2-NM': {'emass1': 0.328, 'hmass1': 0.336},
                    'H-WSe2-NM': {'emass1': 0.389, 'hmass1': 0.355},
                    'H-WTe2-NM': {'emass1': 0.364, 'hmass1': 0.286},
                    'H-ZrS2-NM': {'emass1': 2.881, 'hmass1': 2.2},
                    'H-ZrSe2-NM': {'emass1': 0.0, 'hmass1': 1.973},
                    'H-ZrTe2-NM': {'emass1': 0.0, 'hmass1': 1.136},
                    'T-GeO2-NM': {'emass1': 0.344, 'hmass1': 3.79},
                    'T-GeS2-NM': {'emass1': 0.689, 'hmass1': 1.289},
                    'T-HfO2-NM': {'emass1': 3.18, 'hmass1': 2.767},
                    'T-HfS2-NM': {'emass1': 2.372, 'hmass1': 0.249},
                    'T-HfSe2-NM': {'emass1': 2.286, 'hmass1': 0.159},
                    'T-Mn2Cl4-FM': {'emass1': 1.746, 'hmass1': 6.806},
                    'T-MnO2-FM': {'emass1': 1.055, 'hmass1': 43.724},
                    'T-NiO2-NM': {'emass1': 2.007, 'hmass1': 0.0},
                    'T-NiS2-NM': {'emass1': 0.403, 'hmass1': 0.617},
                    'T-PbO2-NM': {'emass1': 0.45, 'hmass1': 29.088},
                    'T-PbS2-NM': {'emass1': 0.895, 'hmass1': 4.138},
                    'T-PbSe2-NM': {'emass1': 1.07, 'hmass1': 0.36},
                    'T-PdO2-NM': {'emass1': 3.069, 'hmass1': 0.0},
                    'T-PdS2-NM': {'emass1': 0.565, 'hmass1': 2.247},
                    'T-PdSe2-NM': {'emass1': 0.337, 'hmass1': 0.635},
                    'T-PtO2-NM': {'emass1': 3.288, 'hmass1': 28.946},
                    'T-PtS2-NM': {'emass1': 0.682, 'hmass1': 1.546},
                    'T-PtSe2-NM': {'emass1': 0.463, 'hmass1': 2.893},
                    'T-PtTe2-NM': {'emass1': 0.251, 'hmass1': 0.359},
                    'T-SnO2-NM': {'emass1': 0.355, 'hmass1': 4.491},
                    'T-SnS2-NM': {'emass1': 0.779, 'hmass1': 2.034},
                    'T-SnSe2-NM': {'emass1': 0.744, 'hmass1': 0.402},
                    'T-TiO2-NM': {'emass1': 1.214, 'hmass1': 3.834},
                    'T-ZrO2-NM': {'emass1': 1.384, 'hmass1': 3.017},
                    'T-ZrS2-NM': {'emass1': 2.04, 'hmass1': 0.26},
                    'T-ZrSe2-NM': {'emass1': 1.928, 'hmass1': 0.158}}

_default_thicknesses = {'H-MoS2-icsd-644245': 6.1511,
                       'H-TaSe2-icsd-651948': 6.375,
                       #  'H-TaSe2-icsd-651950': 6.36,
                       'T-PdTe2-icsd-649016': 5.118,
                       'T-CrSe2-icsd-626718': 5.915,
                       'T-ZrTe2-icsd-653213': 6.66,
                       'T-VS2-icsd-651361': 5.755,
                       'T-TiSe2-icsd-173923': 6.01,
                       'H-NbSe2-icsd-645369': 6.27,
                       'T-CrTlTe2-icsd-152836': 7.9352,
                       'T-SnSe2-icsd-651910': 6.132,
                       'T-HfS2-icsd-638847': 5.837,
                       'T-VSe2-icsd-652158': 6.048,
                       'H-MoTe2-icsd-15431': 6.982,
                       'T-CoTe2-icsd-625401': 5.405,
                       'T-SnS2-icsd-650992': 5.9,
                       'T-TiTe2-icsd-653071': 6.48,
                       'T-ZrS2-icsd-651465': 5.813,
                       'T-TaS2-icsd-651089': 5.9,
                       'T-HfTe2-icsd-638959': 6.65,
                       'T-PtS2-icsd-649534': 5.0389,
                       'T-TiS2-icsd-651178': 5.7,
                       'T-NbTe2-icsd-645529': 6.61,
                       'T-HfSe2-icsd-638899': 6.159,
                       'T-IrTe2-icsd-33934': 5.404,
                       'T-RhTe2-icsd-650448': 5.442,
                       'H-MoSe2-icsd-644334': 6.45,
                       'T-SiTe2-icsd-652385': 6.71,
                       'H-WSe2-icsd-40752': 6.48,
                       'T-PtTe2-icsd-649747': 5.2209,
                       'T-VTe2-icsd-603582': 6.582,
                       'H-TaS2-icsd-651092': 6.05,
                       'H-WS2-icsd-202366': 6.1615,
                       'T-ZrSe2-icsd-652236': 6.128,
                       'T-PtSe2-icsd-649589': 5.0813,
                       'T-NiTe2-icsd-159382': 5.266,
                       'BPx': 5.26,
                       'BPy': 5.26,
                       'MoSSe': 6.32,
                       'MoSSePrime': 6.32,
                       'graphene': 3.35,  # Wiki
                       'BN': 3.33,  # ioffe.ru/SVA/NSM/Semicond/BN/basic.html
                       'GaSe': 9.3}

def _get_ehmass(formula):
    '''
    @Returns: Dict with format: {'emass1': float (or [float, float]), 'hmass1': float (or [float, float])}.
        Default effective electron and hole mass for material with the given chemical formula (e.g. for 'H-MoS2').
    '''
    key = [k for k in _default_ehmasses.keys() if k.startswith(formula)][0]
    return _default_ehmasses[key]

def get_intermass(e_layer_formula, h_layer_formula):
    '''
    @Returns: Effective interlayer exciton mass between e_layer (n-doped) and h_layer (p-doped)
    '''
    me = mean(_get_ehmass(e_layer_formula)['emass1'])
    mh = mean(_get_ehmass(h_layer_formula)['hmass1'])
    return 1/(1/me + 1/mh)

def get_thickness(formula):
    '''
    @Returns: Default thickness for material with the given chemical formula (e.g. for 'H-MoS2').
    '''
    key = [k for k in _default_thicknesses.keys() if k.startswith(formula)][0]
    return _default_thicknesses[key]
