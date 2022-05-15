# Independent calculations of Building blocks
## Eigenvalues
**30 kpts and PBE**
```
mq submit "calculate_eigenvalues.py BN 800 PBE 30" -R 24:xeon24_512:8h -n "cheap_eig_BN"
```
```
for material in 'WS2' 'WSe2'
do
 mq submit "calculate_eigenvalues.py $material 500 PBE 30" -R 24:xeon24_512:8h -n "cheap_eig_$material"
done
```
**PBE, 10 kpts**
```
mq submit "calculate_eigenvalues.py BN 800 PBE 10" -R 24:xeon24_512:8h -n "eig_no_kpts_10_BN"
```
```
for material in 'WS2' 'WSe2'
do
 mq submit "calculate_eigenvalues.py $material 500 PBE 10" -R 24:xeon24_512:8h -n "eig_no_kpts_10_$material"
done
```

**LDA, 30 kpts**
```
mq submit "calculate_eigenvalues.py BN 800 LDA 30" -R 24:xeon24_512:8h -n "cheap_eig_no_kpts_30_xc_LDA_BN"
```
```
for material in 'WS2' 'WSe2'
do
 mq submit "calculate_eigenvalues.py $material 500 LDA 30" -R 24:xeon24_512:8h -n "cheap_eig_no_kpts_30_xc_LDA_$material"
done
```

## Building Blocks
**eig: 30 kpts and PBE**
```
mq submit "calculate_building_block.py BN 150 PBE 30" -R 40:xeon40:8h -n "cheap_bb_40_BN" -d "cheap_eig_BN"
```
```
for material in 'WS2' 'WSe2'
do
 mq submit "calculate_building_block.py $material 100 PBE 30" -R 40:xeon40:8h -n "cheap_bb_40_$material" -d "cheap_eig_$material"
done
```

**eig: 10 kpts and PBE**
```
for material in 'BN' 'WS2' 'WSe2'
do
 mq submit "calculate_building_block.py $material 50 PBE 10" -R 40:xeon40:8h -n "cheap_bb_40_eig_no_kpts_10_$material" -d "eig_no_kpts_10_$material"
done
```

**eig: 30 kpts with LDA**
```
for material in 'BN' 'WS2' 'WSe2'
do
 mq submit "calculate_building_block.py $material 80 LDA 30" -R 40:xeon40:8h -n "cheap_bb_40_eig_no_kpts_30_eig_xc_LDA_$material" -d "cheap_eig_no_kpts_30_xc_LDA_$material"
done
```