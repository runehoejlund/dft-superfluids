# creates: lowdim.png
import numpy as np
from ase.db import connect
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

fontsize = 15
matplotlib.rcParams['xtick.labelsize'] = fontsize
matplotlib.rcParams['ytick.labelsize'] = fontsize


def run_example():
    c = connect('/home/niflheim/s183774/dft-superfluids/search_materials/lowdim.db')
    rows = [r for r in c.select()]
    dims = [0, 1, 2, 3]
    colors = ['#8dc2db', '#fbc36e', '#aaca7f', '#ff6961']

    data = []
    for row in rows:
        #print(row)
        if 'a_2' in row and 'b_2' in row:
            k1 = row.a_2
            k2 = row.b_2
            dim = int(row.dimtype[:-1])
            if dim in dims:
                data.append((k1, k2 - k1, dim))
    data = np.array(data)
    #print(data)
    plt.figure(figsize=(10, 5))
    for dim in dims[::-1]:
        indices = np.where(data[:, 2] == dim)[0]
        xs = data[indices, 0]
        ws = data[indices, 1]
        plt.scatter(xs, ws, c=colors[dim], s=1)

    patches = [Patch(color=colors[dim], label="%dD" % dim) for dim in dims]
    plt.legend(handles=patches, loc='upper right', fontsize=fontsize)

    plt.xlim(0.5, 2.5)
    plt.ylim(0, 1.75)
    plt.xlabel(r'$k_1$', fontsize=fontsize)
    plt.ylabel(r'$k_2 - k_1$', fontsize=fontsize)

    plt.tight_layout()
    plt.savefig('./lowdim.pdf')
    plt.close()
run_example()