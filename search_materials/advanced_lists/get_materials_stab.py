### import list of file names
from os import walk

Materials = []
for (dirpath, dirnames, filenames) in walk('../data'):
    N=len('-chi.npz')
    Materials.extend(filenames)
    break
for i,Mat_el in enumerate(Materials):
    Materials[i]=Mat_el[:-N]
Material_classes = []
Crystal_type = []
Phase_list=[]
for i,Mat_el in enumerate(Materials):
    Materials[i]=Mat_el[2:]
    Phase=Mat_el[0]
    Phase_list.append(Phase)
    if Phase=='H':
        Crystal_type.append('AB2-187-bi')
    elif Phase=='T':
        Crystal_type.append('AB2-164-bd')
    #print(Phase)
    Material_classes.extend(['TMDC-'+Phase])
Nmat=len(Materials)

print(Nmat)
print(Materials)
print(Material_classes)


### Find effective masses
#import some packages
from math import floor
import numpy as np
import matplotlib.pyplot as plt
import ase.db
import asr

# Connect to database
db = ase.db.connect('/home/niflheim2/cmr/C2DB-ASR/collected-databases/c2db.db')
#rows=db.select('class=TMDC-H')
#f = open('Emil_effmass.dat', 'w')
Material_c2db=[]
emass1_vec=[]
emass2_vec=[]
hmass1_vec=[]
hmass2_vec=[]
bandgap_vec=[]
dir_bandgap_vec=[]
Material_plot=[]
uid_vec=[]
thermo_stab=[]
ehull_vec=[]
print(Nmat)
for i in range(Nmat):
    selectionString='formula='+Materials[i]+',crystal_type='+Crystal_type[i]
    selectionString+=',thermodynamic_stability_level=3,first_class_material=True,dynamic_stability_phonons=high,dynamic_stability_stiffness=high'
    print(selectionString)
    print(i)
    #this try/except-construction
    try:
        row=db.get(selection=selectionString)
        print(i)
        emass1_vec.append(row.emass_cb_dir1)
        emass2_vec.append(row.emass_cb_dir2)
        hmass1_vec.append(row.emass_vb_dir1)
        hmass2_vec.append(row.emass_vb_dir2)
        Material_c2db.append(selectionString)
        Material_plot.append(Phase_list[i]+'-'+Materials[i])
        bandgap_vec.append(row.gap)
        dir_bandgap_vec.append(row.gap_dir)
        uid_vec.append(row.uid)
        thermo_stab.append(row.thermodynamic_stability_level)
        ehull_vec.append(row.ehull)
        print(len(thermo_stab))
        print(len(emass1_vec))
        print(len(Material_c2db))
        print(len(dir_bandgap_vec))
    except KeyError:
        print('Not in database')
        if Crystal_type[i]=='AB2-187-bi':
            Crystal_type[i]='AB2-187-ai'
            selectionString='formula='+Materials[i]+',crystal_type='+Crystal_type[i]
            selectionString+=',thermodynamic_stability_level=3,first_class_material=True,dynamic_stability_phonons=high,dynamic_stability_stiffness=high'
            
            print(selectionString)
            try:
                row=db.get(selection=selectionString)
                print(i)
                emass1_vec.append(row.emass_cb_dir1)
                emass2_vec.append(row.emass_cb_dir2)
                hmass1_vec.append(row.emass_vb_dir1)
                hmass2_vec.append(row.emass_vb_dir2)
                Material_c2db.append(selectionString)
                Material_plot.append(Phase_list[i]+'-'+Materials[i])
                bandgap_vec.append(row.gap)
                dir_bandgap_vec.append(row.gap_dir)
                uid_vec.append(row.uid)
                thermo_stab.append(row.thermodynamic_stability_level)
                ehull_vec.append(row.ehull)
                print(len(thermo_stab))
                print(len(emass1_vec))
                print(len(Material_c2db))
                print(len(dir_bandgap_vec))
            except KeyError:
                print('Not in database')
            except AttributeError:
                print('No bandgap')
        else:
            print('Not in database')
    except AttributeError:
        print('No bandgap')
print(np.shape(dir_bandgap_vec))
np.savez('./Materials_stable.npz',Material_plot=Material_plot,bandgap=bandgap_vec,dir_bandgap=dir_bandgap_vec,material_c2db_list=Material_c2db,emass1_vec=emass1_vec,emass2_vec=emass2_vec,hmass1_vec=hmass1_vec,hmass2_vec=hmass2_vec,uid_vec=uid_vec,thermo_stab=thermo_stab,ehull_vec=ehull_vec)
#terminal for no child: kill -9 -1