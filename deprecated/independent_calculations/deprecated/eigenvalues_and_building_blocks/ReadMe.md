# Independent calculations of Building blocks
**Eigenvalues**:
```
for material in 'BN' 'MoS2' 'MoSe2' 'WS2' 'WSe2' 'MoTe2' 'WTe2'
do
 mq submit "calculate_eigenvalues.py $material" -R 24:xeon24_512:8h -n "eig_$material"
done
```

**Building Blocks**
```
for material in 'MoS2' 'MoSe2' 'WS2' 'WSe2' 'MoTe2' 'WTe2'
do
 mq submit "calculate_building_block.py $material" -R 120:xeon40:48h -n "bb_120_$material"
done
```

**Both in one**
```
for material in 'MoS2' 'MoSe2' 'WS2' 'WSe2' 'MoTe2' 'WTe2'
do
 mq submit "calculate_eigenvalues.py $material" -R 24:xeon24_512:8h -n "eig_$material"
 mq submit "calculate_building_block.py $material" -R 40:xeon40_768:8h -n "bb_$material" -d "eig_$material"
done
```