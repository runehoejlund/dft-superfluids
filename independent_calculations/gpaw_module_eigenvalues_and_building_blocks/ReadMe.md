# Building Blocks with module load gpaw instead og venv
```
for material in 'MoS2' 'MoSe2' 'WS2' 'WSe2' 'MoTe2' 'WTe2'
do
 mq submit "gpaw_v_calculate_building_block.py $material" -R 120:xeon40:48h -n "bb_120_gpaw_loaded_$material"
done
```