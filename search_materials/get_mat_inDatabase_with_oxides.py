#np.savez('./Materials_iso.npz',materials=materials,iso=iso,e_avg_vec=e_avg_vec,h_avg_vec=h_avg_vec)
import numpy as np
import matplotlib.pyplot as plt
import ase.db
#load materials
out=np.load('./Materials_iso_crystal.npz')
materials=out['materials']
h_iso=out['h_iso'].flatten()
e_iso=out['e_iso'].flatten()
N=len(h_iso)
iso=np.repeat(False,N)
for i in range(N):
    if h_iso[i]==1:
        iso[i]=True
    elif e_iso[i]==1:
        iso[i]=True
    else:
        iso[i]=False
bandgap=out['bandgap']
dir_bandgap=out['dir_bandgap']
e_avg_vec=out['e_avg_vec']
h_avg_vec=out['h_avg_vec']
print(iso)
print(bandgap[iso])
print(dir_bandgap[iso])



dir_gap=abs(bandgap-dir_bandgap)<0.01
materials_iso=materials[iso]
e_avg_vec_iso=e_avg_vec[iso]
h_avg_vec_iso=h_avg_vec[iso]
e_iso_iso=e_iso[iso]
print(np.shape(dir_gap))
dir_gap_iso=dir_gap[iso]
print(dir_gap)
print(materials_iso)
print(materials_iso[dir_gap_iso])

inDatabase=np.repeat(False,sum(iso))
print(inDatabase)
COD_id_vec=np.zeros((sum(iso)))
db_c2db = ase.db.connect('/home/niflheim2/cmr/C2DB-ASR/collected-databases/c2db.db')
db_lowdim = ase.db.connect('/home/niflheim/s183774/dft-superfluids/search_materials/lowdim.db')
N_iso=len(materials_iso)
for i in range(N_iso):
    try:
        print(i)
        selectionString=materials_iso[i]
        row_c2db=db_c2db.get(selection=selectionString)
        COD_id=row_c2db.cod_id
        selectionString='dbid={}'.format(COD_id)
        print(selectionString)
        #row=db.get(selection='formula=SnMo6S8')
        row=db_lowdim.get(selection=selectionString)
        print(row.formula)
        print(row.dbid)
        COD_id_vec[i]=row.dbid
        inDatabase[i]=True
        print(COD_id)
        print(inDatabase)
    except AttributeError:
        print('formula={} has no cod_id'.format(materials_iso[i]))
    except KeyError:
        print('formula={} is not in lowdim database'.format(materials_iso[i]))

thicknesses=0
print(materials_iso[inDatabase])
print(COD_id_vec[inDatabase])
np.savez('./Materials_iso_wData_crystal.npz',COD_id=COD_id_vec[inDatabase],materials=materials_iso[inDatabase],dir_gap=dir_gap_iso[inDatabase],e_avg_vec=e_avg_vec_iso[inDatabase],h_avg_vec=h_avg_vec_iso[inDatabase],e_iso=e_iso_iso[inDatabase])
