### import list of file names
from os import walk

Materials = []
for (dirpath, dirnames, filenames) in walk('./data'):
    N=len('-chi.npz')
    Materials.extend(filenames)
    break
for i,Mat_el in enumerate(Materials):
    Materials[i]=Mat_el[:-N]
Material_classes = []
for i,Mat_el in enumerate(Materials):
    Materials[i]=Mat_el[2:]
    Phase=Mat_el[0]
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
print(Nmat)
for i in range(Nmat):
    selectionString='formula='+Materials[i]+',class='+Material_classes[i]
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
        bandgap_vec.append(row.gap)
        dir_bandgap_vec.append(row.gap_dir)
        print(len(emass1_vec))
        print(len(Material_c2db))
    except KeyError:
        print('Not in database')
    except AttributeError:
        print('No bandgap')
np.savez('./Materials_c2db.npz',bandgap=bandgap_vec,dir_bandgap=dir_bandgap_vec,material_c2db_list=Material_c2db,emass1_vec=emass1_vec,emass2_vec=emass2_vec,hmass1_vec=hmass1_vec,hmass2_vec=hmass2_vec)