#initialize list of uid's
uid_List=[]
#load uid's that we would like a thickness for
with open('uid_for_which_we_need_a_thickness.txt', 'r') as content:
    for line in content:
        x=line[:-1]
        uid_List.append(x)
print(uid_List)
#test
from ast import For
import ase.db
db = ase.db.connect('/home/niflheim2/cmr/C2DB-ASR/collected-databases/c2db.db')
Formulas=[]
crystals=[]
for i in range(len(uid_List)):
    selectionString='uid='+uid_List[i]
    row=db.get(selection=selectionString)
    #print(row.ehull)
    Formulas.append(row.formula)
    crystals.append(row.crystal_type)
print(len(Formulas))
print(Formulas)
print(crystals)