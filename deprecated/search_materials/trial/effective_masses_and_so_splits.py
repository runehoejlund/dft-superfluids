# creates: band-alignment.png
from math import floor
import numpy as np
import matplotlib.pyplot as plt
import ase.db
import asr

#function to get nice formula
def getniceformula(label):
    name=label[0]
    out=name
    num=1
    for i in range(1,len(label)):
        if(label[i]==label[i-1]):
            num+=1
            if(i==(len(label)-1) and num>1):
                out=out+str(num)
        else:
            if num>1:
                out=out+str(num)
            name=label[i]
            out=out+name
            num=1
    return out


classes=['TMDC-H']
# Connect to database
db = ase.db.connect('/home/niflheim2/cmr/C2DB-ASR/collected-databases/c2db.db')
f = open('Emil_effmass.dat', 'w')
barrier = 0.5 #eV Min barrier in staggered alignment
#print criteria in f
print('Search for bilayer materials with large effective masses and bandgaps',file=f)
print('classes',classes,file=f)#printing directly to file
print('CRITERIA:',file=f)
print("'class='+thisclass+',gap>0.5,first_class_material=True,emass_cb_dir1>0.3,emass_vb_dir1<-0.3',sort='emass_vb_dir1'",file=f)
print('Additional criteria: abs(emass_dir1-emass_dir2) <0.03 and abs(emass)<3',file=f)
print('                     vbm > BN.vbn + 0.3, cbm < BN.cbm - 0.3',file=f)
print('                     gap_dir = gap',file=f)
ids=[]#
plotlabel=[]
me=[]#electron mass
mh=[]#hole mass
cbm=[]#conduction band maximum
vbm=[]
evac=[]
evacdiff=[]
a_lat=[]

# for thisclass in classes:
#     rows = db.select('class='+thisclass+',gap>0.5,has_asr_gw=True,first_class_material=True,emass_cb_dir1>0.3,emass_vb_dir1<-0.2',sort='emass_vb_dir1')
#     labels = []
#     print('\n\n CLASS: ',thisclass,file=f)
#     print('label,      gap, emass_cb_dir1, emass_cb_dir2, emass_vb_dir1, emass_vb_dir2, magstate,cbm,vbm',file=f)
#     for row in rows:    
#         label=row.symbols[:]
#         print(label)
#         labels.append(label)
#         ids.append(row.id)
#         niceformula=getniceformula(label)
#         if(thisclass=='TMDC-H' and not hasattr(row,'icsd_id') and 'Cr' not in niceformula): continue
#         plotlabel.append(niceformula)
        
#         me.append((row.emass_cb_dir1 + row.emass_cb_dir2)/2)
#         mh.append((row.emass_vb_dir1 + row.emass_vb_dir2)/2)

#         cbm.append(row.cbm_gw)
#         vbm.append(row.vbm_gw)

#         evacdiff.append(row.evacdiff)

#         evac.append(row.evac)

#         #a_lat.append(row.a)

#         offset=10-len(niceformula)

#         niceformula+=offset*' '

#         print(niceformula,format(row.gap,'.4f'),format(row.emass_cb_dir1,'.4f'),format(row.emass_cb_dir2,'.4f'),format(row.emass_vb_dir1,'.4f'),

#               format(row.emass_vb_dir2,'.4f'),row.magstate,row.cbm,row.vbm,file=f)


# combos=[]
# gap=[]

# for i in range(len(cbm)):

#     for j in range(len(vbm)):

#         thisgap=vbm[j] - evac[j] - (cbm[i]-evac[i]) - (evacdiff[i]+evacdiff[j])/2.

#         #print(thisgap)

#         #lat_mm=abs(a_lat[j]-a_lat[i])/((a_lat[i]+a_lat[j])/2.0)

#         #if(lat_mm > 0.1):

#         #    continue

#         if('CrSe2' in niceformula): print('TEST: CrSe2 in niceformula')

#         if(thisgap > -0.3 and thisgap < 0.4):

#             combos.append([i,j])

#             gap.append(thisgap)

# print('len combos',len(combos))

# for i in range(len(combos)):

#     #print(combos[i][0],combos[i][1])

#     print(plotlabel[combos[i][0]],plotlabel[combos[i][1]],gap[i],file=f)    

#     print(plotlabel[combos[i][0]],plotlabel[combos[i][1]],gap[i])


# print('Only selected Janus:')

# sel_Janus=['AsTeBr','BiTeBr','BiTeCl','CrSeTe','CrSSe','MoSSe']

# for i in range(len(combos)):

# #print(combos[i][0],combos[i][1])    

#     if(plotlabel[combos[i][0]] not in sel_Janus and '2' not in plotlabel[combos[i][0]]): continue

#     if(plotlabel[combos[i][1]] not in sel_Janus and '2' not in plotlabel[combos[i][1]]): continue

#     print(plotlabel[combos[i][0]],plotlabel[combos[i][1]],gap[i],file=f)

#     print(plotlabel[combos[i][0]],plotlabel[combos[i][1]],gap[i])


# xticks=[]


# # Width and height in pixels

# ppi = 100

# figw = 800

# figh = 600

# fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)

# ax = fig.add_subplot(1, 1, 1)

# for i in range(len(me)):

#     ax.plot(i,me[i],'bo')

#     ax.plot(i,abs(mh[i]),'ro')

#     xticks.append(i)

# #ax = fig.add_subplot(1, 1, 1)

# plt.ylabel('effective masses')

# plt.title('electron mass (blue) hole mass (red)')

# #plt.savefig('materials.png')

# ax.set_xticks(xticks)

# ax.set_xticklabels(plotlabel, rotation=90, fontsize=10)

# plt.savefig('materials.png')

