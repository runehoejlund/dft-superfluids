#np.savez('./Materials_iso.npz',materials=materials,iso=iso,e_avg_vec=e_avg_vec,h_avg_vec=h_avg_vec)
import numpy as np
import matplotlib.pyplot as plt
import ase.db
#load materials
out=np.load('./Materials_iso.npz')
materials=out['materials']
h_iso=out['h_iso'].flatten()
e_iso=out['e_iso'].flatten()
bandgap=out['bandgap']
dir_bandgap=out['dir_bandgap']
e_avg_vec=out['e_avg_vec']
h_avg_vec=out['h_avg_vec']
print(bandgap[h_iso])
print(dir_bandgap[h_iso])




dir_gap=abs(bandgap[h_iso]-dir_bandgap[h_iso])<0.01
materials_iso=materials[h_iso]
e_avg_vec_iso=e_avg_vec[h_iso]
h_avg_vec_iso=h_avg_vec[h_iso]
e_iso_iso=e_iso[h_iso]
dir_gap_iso=dir_gap[h_iso]
print(dir_gap)
print(materials_iso)

inDatabase=np.repeat(False,sum(h_iso))
print(inDatabase)
COD_id_vec=np.zeros((sum(h_iso)))
db_c2db = ase.db.connect('/home/niflheim2/cmr/C2DB-ASR/collected-databases/c2db.db')
db_lowdim = ase.db.connect('/home/niflheim/s183774/dft-superfluids/search_materials/lowdim.db')
for i in range(sum(h_iso)):
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
np.savez('./Materials_iso_wData.npz',COD_id=COD_id_vec[inDatabase],materials=materials_iso[inDatabase],dir_gap=dir_gap_iso[inDatabase],e_avg_vec=e_avg_vec_iso[inDatabase],h_avg_vec=h_avg_vec_iso[inDatabase],e_iso=e_iso_iso[inDatabase])
