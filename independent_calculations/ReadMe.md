# Tungsten W-DC

## Ground state calculations
```
mq submit calc_gs_WS2.py -R 24:3h -n gs_WS2_500
mq submit calc_gs_WSe2.py -R 24:3h -n gs_WSe2_500
mq submit calc_gs_WTe2.py -R 24:3h -n gs_WTe2_500
```

## Building Blocks
```
mq submit calc_bb_WS2.py -R 48:4h -n bb_WS2_500 -d gs_WS2_500
mq submit calc_bb_WSe2.py -R 48:4h -n bb_WSe2_500 -d gs_WSe2_500
mq submit calc_bb_WTe2.py -R 48:4h -n bb_WTe2_500 -d gs_WTe2_500
```

# Molybdenum M-DC
## Ground state calculations
```
mq submit calc_gs_MoS2.py -R 24:3h -n gs_MoS2_500
mq submit calc_gs_MoSe2.py -R 24:3h -n gs_MoSe2_500
mq submit calc_gs_MoTe2.py -R 24:3h -n gs_MoTe2_500
```

## Building Blocks
```
mq submit calc_bb_MoS2.py -R 48:4h -n bb_MoS2_500 -d gs_MoS2_500
mq submit calc_bb_MoSe2.py -R 48:4h -n bb_MoSe2_500 -d gs_MoSe2_500
mq submit calc_bb_MoTe2.py -R 48:4h -n bb_MoTe2_500 -d gs_MoTe2_500
```