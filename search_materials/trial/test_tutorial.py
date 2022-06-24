# creates: band-alignment.png
from math import floor
import numpy as np
import matplotlib.pyplot as plt
from ase.db import connect

# Connect to database
db = connect('c2db.db')
#db = connect('/home/niflheim2/cmr/C2DB-ASR/collected-databases/c2db.db')
print(db)
rows = db.select('gap>0,class=TMDC-H', sort='gap')
print(rows)
labels = []
vbms = []
cbms = []
count=0
for row in rows:
    print(row)
    count+=1
    M, X = row.symbols[:2]
    label = M + X + '$_2$'
    labels.append(label)
    vbms.append(row.vbm)
    cbms.append(row.cbm)

x = np.arange(len(vbms)) + 0.5
emin = floor(min(vbms)) - 1.0

# Width and height in pixels
ppi = 100
figw = 800
figh = 400

fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)
ax = fig.add_subplot(1, 1, 1)
ax.bar(x, np.array(vbms) - emin, bottom=emin)
ax.bar(x, -np.array(cbms), bottom=cbms)
ax.set_xlim(0, len(labels))
ax.set_ylim(emin, 0)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90, fontsize=10)

plt.title("2H-TMD's: Positions of VBM and CBM (PBE+SOC)", fontsize=12)
plt.ylabel('Energy relative to vacuum [eV]', fontsize=10)
plt.tight_layout()
plt.savefig('band-alignment.png')