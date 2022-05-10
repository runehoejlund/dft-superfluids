# Independent calculations of Building blocks
Test:
```
for material in 'BN' 'MoS2' 'MoSe2' 'WS2' 'WSe2' 'MoTe2' 'WTe2'
do
 mq submit "calculate_eigenvalues.py $material" -R 24:xeon24_512:8h -n "eig_$material"
 mq submit "calculate_building_block.py $material" -R 24:xeon24_512:8h -n "bb_$material" -d "eig_$material"
done
```