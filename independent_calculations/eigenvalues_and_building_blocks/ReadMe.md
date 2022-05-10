# Independent calculations of Building blocks
Test:
```
for material in 'BN' 'MoS2' 'MoSe2' 'WS2' 'WSe2' 'MoTe2' 'WTe2'
do
 mq submit "calculate_eigenvalues.py $material" -R 40:xeon40_768:4h -n "eig_$material"
 mq submit "calculate_building_block.py $material" -R 40:xeon40_768:8h -n "bb_$material" -d "eig_$material"
done
```