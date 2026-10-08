
Compute year by year binary field from snow depth:

##MAR
https://github.com/msantolariaotin/MAR-RECAP/blob/main/scripts/compute_binary_daily_snc.MAR_byyear.py

###
for year in $(seq 1980 1 2024);do
python compute_binary_daily_snc.MAR_byyear.py ${year}
done
###

Snow on land and ice, as when transforming to 1,0 the accumulation problem will not occur
#ds_SND=mar.compute_snow_height(ZN2_k1,ZN3_k2,dsICE)
#ds_SNC=ds_SND > 0.1 #meters
#Output saved in /MARout/GRq/spin2/work/binary_snow 
# as 'SHSN3_SHSN2_bin_day_MARv3.14_ER5_spin2_GRq_1983.nc

Snow on land
ds_SND=ZN3_k2
ds_SNC=ds_SND > 0.1 #meters
#Output saved in /MARout/GRq/spin2/work/snow_bin/
# as 'SHSN3_bin_day_MARv3.14_ER5_spin2_GRq_1983.nc


##For all the other datasets:
https://github.com/msantolariaotin/MAR-RECAP/blob/main/scripts/method_binary_snow_all.ipynb

#esa cci
#hma sr
#HARv2
method_binary_snow_all.ipynb

