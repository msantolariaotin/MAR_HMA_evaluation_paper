#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(1, '/home/santolam/MyPythonLibrary/MAR-RECAP/libmar/')
import climbasis as climb
from climbasis import *
import domain as dom
import myplot
import numpy.ma as ma
from myplot import *
import obsinfo as obs
from obsinfo import *


# In[2]:


plotsDir='/home/santolam/MyPythonLibrary/MAR-RECAP/scripts_paper_on_evaluation_MAR/figures_paper_on_evaluation/'


# In[3]:


domainM='GRq'; nx=ny=10

ds_RF_raw=xr.open_mfdataset('/bettik/PROJECTS/pr-regional-climate/santolam/MARout_post/GRq/spin2/work/daily/'+
    'RF_daysum_MARv3.14_ER5_spin2_GRq_*.nc')['RF']#.sel(ZTQLEV=2)
ds_RF= ds_RF_raw.rename({'TIME': 'time'})
ds_RF=ds_RF[:,ny:-ny,nx:-nx]

ds_SF_raw=xr.open_mfdataset('/bettik/PROJECTS/pr-regional-climate/santolam/MARout_post/GRq/spin2/work/daily/'+
    'SF_daysum_MARv3.14_ER5_spin2_GRq_*.nc')['SF']#.sel(ZTQLEV=2)
ds_SF= ds_SF_raw.rename({'TIME': 'time'})
ds_SF=ds_SF[:,ny:-ny,nx:-nx]


# In[4]:


ds_TF=ds_RF+ds_SF


# In[ ]:





# In[ ]:





# In[ ]:





# In[5]:


## Model MAR
domain='GRc'
sourceDataGrid='/home/santolam/'
fileName_grM='NST.2000.01.01.00.GRc.nc'
dsM= xr.open_dataset(sourceDataGrid+fileName_grM)
LONS=dsM.LON[ny:-ny,nx:-nx].values;LATS=dsM.LAT[ny:-ny,nx:-nx].values
dsSH=dsM.SH[ny:-ny,nx:-nx];dsICE=dsM.ICE[ny:-ny,nx:-nx]

dsSH=dsSH.rename({'y': 'Y','x':'X'})


# In[6]:


lonmin, lonmax = 86.4, 87.2
latmin, latmax = 27.6, 28.2

mask_khumbu = (
    (LONS >= lonmin) & (LONS <= lonmax) &
    (LATS >= latmin) & (LATS <= latmax)
)


# In[7]:


from scipy import stats
import numpy as np
import xarray as xr

def daily_lapse_rate(ds_TF, dsSH, mask_region):

    Z = dsSH.values[mask_region]   # elevation only once

    lapse_rates = []

    for t in ds_TF.time:
        T = ds_TF.sel(time=t).values[mask_region]

        mask = np.isfinite(T) & np.isfinite(Z)

        slope, _, _, _, _ = stats.linregress(
            Z[mask],
            T[mask]
        )

        lapse_rates.append(slope * 1000)   # °C/km

    return xr.DataArray(
        lapse_rates,
        coords=[ds_TF.time],
        dims=["time"],
        name="lapse_rate"
    )


# In[ ]:


lr_khumbu = daily_lapse_rate(ds_TF, dsSH, mask_khumbu)


# In[ ]:





# In[ ]:


#ds_TF=ds_SF+ds_RF


# In[ ]:


####
##Donnes meteo
sourceData='/bettik/PROJECTS/pr-regional-climate/santolam/glacioclim/donnees_precip/'
#
#Precipitation_Khare_corrected_Nov2016_Nov2023_final.xlsx
#Precipitation_Pyramid_Pheriche_corrected_Apr2016_Nov2023_final.xlsx
#Precipitation_Pyramid_Pheriche_corrected_Dec2012_Apr2016_final.xlsx


# In[ ]:


#https://github.com/Andeol-ramb/MAR_HMA_GLACIOCLIM_Comparisons/blob/main/Sensitivity_Test_MAR/Sensitivity_Test_Pyramide_Precip.ipynb
####
## Opening Pheriche+Khare
####

sourceDataSta=sourceData#'/Users/santolam/Data/glacioclim/donnees_precip/'
path1 =sourceDataSta+"/Precipitation_Pyramid_Pheriche_corrected_Dec2012_Apr2016_final.xlsx"
xl_data1=pd.ExcelFile(path1)

dfs1= {sheet_name: xl_data1.parse(sheet_name) 
       for sheet_name in xl_data1.sheet_names}

DataPyramid_Pheriche12_16=dfs1['Precip_data_Dec12_Apr16']

NameVarsPP12_16=['TimeY','RRYhourly','RRYcumul','TimeH','RRHhourly','RRHcumul']
UnitVarsPP16_23=['data/hour','mm','mm','data/hour','mm','mm',]

dfile1P12_16= pd.DataFrame(data=DataPyramid_Pheriche12_16.loc[10:])
df1P12_16=pd.DataFrame(dfile1P12_16.values, columns=NameVarsPP12_16)

df1P12_16['TimeY'] = df1P12_16['TimeY'].dt.round('h')

path =sourceDataSta+"/Precipitation_Pyramid_Pheriche_corrected_Apr2016_Nov2023_final.xlsx"
xl_data=pd.ExcelFile(path)

dfs = {sheet_name: xl_data.parse(sheet_name) 
       for sheet_name in xl_data.sheet_names}
DataPyramid_Pheriche16_23=dfs['Precip_data_Apr16_Nov23']

NameVarsPP16_23=['TimeY','TairY','uY','RHY','WMOphaseY','RRYhourly','RRYcumul','TimeH','TairH','uH','RHh','WMOphaseH','RRHhourly','RRHcumul']
UnitVarsPP16_23=['data/hour','(°C)','(ms-1)','(%)','mm','mm','data/hour','(°C)','(ms-1)','(%)','mm','mm',]

dfile1P16_23= pd.DataFrame(data=DataPyramid_Pheriche16_23.loc[10:57630]) #3399 marche, Toujours la même taille jusque 3399 puis toujours lenght var=t-1 par la suite 
#CHANGEMENT DANS TIME:3389 	2016-09-15 17:59:59.!999! / 2016-09-15 18:59:59.!998! 
#donc erreur à chaque changement de décimale, corriger cette data avant tout autre chose


dfile2P16_23=pd.DataFrame(data=DataPyramid_Pheriche16_23.loc[57632:]) 
df1P16_23=pd.DataFrame(dfile1P16_23.values, columns=NameVarsPP16_23)
df2P16_23=pd.DataFrame(dfile2P16_23.values, columns=NameVarsPP16_23)
df1P16_23['TimeY'] = df1P16_23['TimeY'].dt.round('h')
df2P16_23['TimeY'] = df2P16_23['TimeY'].dt.round('30min')

#Definition d'une fréquence permettant par la suite le traitement avec des Xarray
def NewTime(df, NameVar, values, freq):
    time = pd.to_datetime(df['TimeY'].values)
    ds = xr.Dataset({NameVar: ("time", np.asarray(values))}, coords={"time": time})
    return ds
# Time step: 1h

RR1_PY=[float(thing) for thing in df1P12_16['RRYhourly'].values]
RRY1_PY = [float(thing) for thing in df1P16_23['RRYhourly'].values]
dsY1_PY = NewTime(df1P16_23, 'RRYhourly', RRY1_PY, '1h')
dsRR1_PY= NewTime(df1P12_16, 'RRYhourly', RR1_PY, '1h')

# Time step : 30 min 
RRY2_PY = [float(thing) for thing in df2P16_23['RRYhourly'].values]
dsY2_PY = NewTime(df2P16_23, 'RRYhourly', RRY2_PY, '30min')
RR_PY = xr.concat([dsRR1_PY,dsY1_PY, dsY2_PY], dim='time')


RR1_PH=[float(thing) for thing in df1P12_16['RRHhourly'].values]
RRY1_PH = [float(thing) for thing in df1P16_23['RRHhourly'].values]
dsY1_PH = NewTime(df1P16_23, 'RRHhourly', RRY1_PH, '1h')
dsRR1_PH= NewTime(df1P12_16, 'RRHhourly', RR1_PH, '1h')

# Time step : 30 min 
RRY2_PH = [float(thing) for thing in df2P16_23['RRHhourly'].values]
dsY2_PH = NewTime(df2P16_23, 'RRHhourly', RRY2_PH, '30min')
RR_PH = xr.concat([dsRR1_PH,dsY1_PH, dsY2_PH], dim='time')

#####
#
#Khare
#
#####
fileName_KH='Precipitation_Khare_corrected_Nov2016_Nov2023_final.xlsx'
xl_file_KH = pd.ExcelFile(sourceDataSta+fileName_KH)
print(xl_file_KH)
#
dfs_KH = {sheet_name: xl_file_KH.parse(sheet_name) 
          for sheet_name in xl_file_KH.sheet_names}

NameVars_KH=['Time','Tair' ,'u' ,'RH', 'Phase_WMO','RR_WMO_Half-hourly_values','RR_WMO_Khare_cumulated']
UnitVars_KH=['time','(°C)','(ms-1)','(%)','phase','mm w.e.','mm w.e.']

##Define new DataFrame and changing name of columns
dfile_KH = pd.DataFrame(data=dfs_KH["Precip_data_Nov16_Nov23"].loc[8:])
df_KH=pd.DataFrame(dfile_KH.values, columns=NameVars_KH)

path =sourceDataSta+fileName_KH
xl_data=pd.ExcelFile(path)
dfs = {sheet_name: xl_data.parse(sheet_name) 
       for sheet_name in xl_data.sheet_names}
DataKhare16_23=dfs['Precip_data_Nov16_Nov23']
NameVarsPP16_23=['Time','Tair','u','RH','WMOphase','RRhourly','RRcumul']
UnitVarsPP16_23=['data/hour','(°C)','(ms-1)','(%)','mm','mm']
dfileP16_23= pd.DataFrame(data=DataKhare16_23.loc[10:])
dfP16_23=pd.DataFrame(dfileP16_23.values, columns=NameVarsPP16_23)

RR_KH=[float(i) for i in dfP16_23.RRhourly.values] 
def NewTime(df, NameVar, values, freq):
    time = pd.to_datetime(df['Time'].values)
    ds = xr.Dataset({NameVar: ("time", np.asarray(values))}, coords={"time": time})
    return ds
RR_KH=NewTime(dfP16_23,'RRhourly',RR_KH,'30min')
#RR=RR.sel(time=slice('2016'))


rr_daily_PY=RR_PY.resample(time='D').sum()
rr_daily_PY=rr_daily_PY.RRYhourly

rr_daily_PH=RR_PH.resample(time='D').sum()
rr_daily_PH=rr_daily_PH.RRHhourly

rr_daily_KH=RR_KH.resample(time='D').sum()
rr_daily_KH=rr_daily_KH.RRhourly

idatePY = str(rr_daily_PY.time[0].values)[:10]
fdatePY = str(rr_daily_PY.time[-1].values)[:10]
idatePH = str(rr_daily_PH.time[0].values)[:10]
fdatePH = str(rr_daily_PH.time[-1].values)[:10]
idateKH = str(rr_daily_KH.time[0].values)[:10]
fdateKH = str(rr_daily_KH.time[-1].values)[:10]


# In[ ]:


###
## PYRAMID Salerno
### 


# In[ ]:


sourceData='/bettik/PROJECTS/pr-regional-climate/santolam/PYRAMID_NETWORK_DATA_v3/'

file_AWS0='AWS0_Z5035_Lvl1.csv'
file_AWS1='AWS1_Z5035_Lvl1.csv'
file_AWS2='AWS2_Z4260_Lvl1.csv'
file_AWS3='AWS3_Z2660_Lvl1.csv'
file_AWS4='AWS4_Z5600_Lvl1.csv'
file_AWS5='AWS5_Z3570_Lvl1.csv'
file_AWSSC='AWSSC_Z7986_Lvl1.csv'
file_CNG='CNG_SNP_Z5700_Lvl1.csv'
file_mon_Pyr='Pyramid_Z5035_lvl2.csv'

# Store filenames in a dictionary for easy looping
files = {
    'AWS0': file_AWS0,
    'AWS1': file_AWS1,
    'AWS2': file_AWS2,
    'AWS3': file_AWS3,
    'AWS4': file_AWS4,
    'AWS5': file_AWS5,
    'AWSSC': file_AWSSC,
    'CNG': file_CNG,
    #'Pyramid': file_mon_Pyr
}
dfs = {}
for name, fname in files.items():
    path = os.path.join(sourceData, fname)
    
    # Read semicolon-delimited CSV
    df = pd.read_csv(path, sep=';')
    
    # Combine into datetime
    df['TIMESTAMP'] = pd.to_datetime(dict(
        year=df['year'],
        month=df['month'],
        day=df['day'],
        hour=df['hour']
    ))
    
    # Set datetime index and drop date columns
    df.set_index('TIMESTAMP', inplace=True)
    df.drop(columns=['year', 'month', 'day', 'hour'], inplace=True)
    
    # Replace physically impossible values (< -100) with NaN
    df[df < -100] = np.nan
    
    # Store
    dfs[name] = df
    
# Optional: unpack for direct access
df_AWS0  = dfs['AWS0']
df_AWS1  = dfs['AWS1']
df_AWS2  = dfs['AWS2']
df_AWS3  = dfs['AWS3']
df_AWS4  = dfs['AWS4']
df_AWS5  = dfs['AWS5']
df_AWSSC = dfs['AWSSC']
df_CNG   = dfs['CNG']
#df_Pyr   = dfs['Pyramid']

# Quick check
print(df_AWS0.head())

# Daily total precipitation (sum of hourly rates)
rr_AWS0_daily = df_AWS0['RR'].resample('D').sum()
rr_AWS1_daily = df_AWS1['RR'].resample('D').sum()
rr_AWS2_daily = df_AWS2['RR'].resample('D').sum()
rr_AWS3_daily = df_AWS3['RR'].resample('D').sum()
rr_AWS4_daily = df_AWS4['RR'].resample('D').sum()
rr_AWS5_daily = df_AWS5['RR'].resample('D').sum()


# In[ ]:


sourceData='/bettik/PROJECTS/pr-regional-climate/santolam/nat_geo_stations_everest/'
#sourceData='/Users/santolam/Desktop/nat_geo_stations_everest/'
##
file_bc='Base_Camp_20230630.csv'
file_c2='Camp2_20230630.csv'
file_phort='Phortse_20230630.csv'
file_bish='Bishop_Rock_20230630.csv'
file_sc='South_Col_20230630.csv'

df_bc = pd.read_csv(os.path.join(sourceData, file_bc), parse_dates=['TIMESTAMP'])
df_c2 = pd.read_csv(os.path.join(sourceData, file_c2), parse_dates=['TIMESTAMP'])
df_phort = pd.read_csv(os.path.join(sourceData, file_phort), parse_dates=['TIMESTAMP'])
df_bish = pd.read_csv(os.path.join(sourceData, file_bish), parse_dates=['TIMESTAMP'])
df_sc = pd.read_csv(os.path.join(sourceData, file_sc), parse_dates=['TIMESTAMP'])

# Optional: set timestamp as index
for df in [df_bc, df_c2, df_phort, df_bish, df_sc]:
    df.set_index('TIMESTAMP', inplace=True)

# Quick check
print(df_bc.head())

rr_bc_daily = df_bc['PRECIP'].resample('D').sum()
rr_phort_daily = df_phort['PRECIP'].resample('D').sum()


# In[ ]:





# In[ ]:





# In[ ]:


###Coordinates


# In[ ]:


import pandas as pd
from pyproj import Transformer

# Define the transformer (UTM Zone 45N → WGS84)
transformer = Transformer.from_crs("epsg:32645", "epsg:4326", always_xy=True)

# --- Coordinates conversions (you already have some precomputed) ---
# MN (Mera North)
eastingMN, northingMN = 489885, 3065938
lon_MN, lat_MN = transformer.transform(eastingMN, northingMN)
elev_MN = 5360

# CH (Changri)
lon_CH, lat_CH, elev_CH = 86.77948450, 27.98336311, 5360

# ML (Merala)
lon_ML, lat_ML, elev_ML = 86.900, 27.735, 5352.008

# KH (Khare)
lon_KH, lat_KH, elev_KH = 86.8776142768303, 27.74424682282522, 4888

# PH (Pheriche)
lon_PH, lat_PH, elev_PH = 86.81972903284355, 27.895048949594884, 4260

# PY (Pyramid)
lon_PY, lat_PY, elev_PY = 86.81296905961787, 27.957821815535848, 5035

# MS (Mera South)
eastingMS, northingMS = 487553.653, 3064704.231
lon_MS, lat_MS = transformer.transform(eastingMS, northingMS)
elev_MS = 5360  # estimated same as MN, if not otherwise specified

# MC (Mera Central)
eastingMC, northingMC = 488409.424, 3066148.049
lon_MC, lat_MC = transformer.transform(eastingMC, northingMC)
elev_MC = 5770

# --- Define metadata list ---
stations_info_glacioclim = [
    {"ID": "MN", "Name": "Mera Naulek", "Lat": lat_MN, "Lon": lon_MN, "Elev_m": elev_MN, "Timestep": "1h"},
    {"ID": "CH", "Name": "Changri", "Lat": lat_CH, "Lon": lon_CH, "Elev_m": elev_CH, "Timestep": "1h"},
    {"ID": "ML", "Name": "Mera La", "Lat": lat_ML, "Lon": lon_ML, "Elev_m": elev_ML, "Timestep": "1h"},
    {"ID": "KH", "Name": "Khare", "Lat": lat_KH, "Lon": lon_KH, "Elev_m": elev_KH, "Timestep": "1h"},
    {"ID": "PH", "Name": "Pheriche", "Lat": lat_PH, "Lon": lon_PH, "Elev_m": elev_PH, "Timestep": "1h"},
    {"ID": "PY", "Name": "Pyramid", "Lat": lat_PY, "Lon": lon_PY, "Elev_m": elev_PY, "Timestep": "1h"},
    {"ID": "MS", "Name": "Mera Summir", "Lat": lat_MS, "Lon": lon_MS, "Elev_m": elev_MS, "Timestep": "1h"},
    {"ID": "MC", "Name": "Mera Camp 5770", "Lat": lat_MC, "Lon": lon_MC, "Elev_m": elev_MC, "Timestep": "1h"},
]

# --- Create DataFrame ---
df_stations_glacioclim = pd.DataFrame(stations_info_glacioclim)

# Display neatly
print(df_stations_glacioclim.to_string(index=False, justify='center', col_space=12))


# In[ ]:


##
# --- AWS and related station metadata ---

# AWSSC (South Col)
lat_AWSSC, lon_AWSSC, elev_AWSSC = 27.98, 86.76, 7986

# CNG_SNP (Changri Nup)
lat_CNG, lon_CNG, elev_CNG = 27.96, 86.93, 5700

# AWS0 (Pyramid)
lat_AWS0, lon_AWS0, elev_AWS0 = 27.96, 86.81, 5035

# AWS1 (Pyramid)
lat_AWS1, lon_AWS1, elev_AWS1 = 27.96, 86.81, 5035

# AWS2 (Pheriche)
lat_AWS2, lon_AWS2, elev_AWS2 = 27.90, 86.82, 4260

# AWS3 (Lukla)
lat_AWS3, lon_AWS3, elev_AWS3 = 27.70, 86.72, 2660

# AWS4 (Kala Patthar)
lat_AWS4, lon_AWS4, elev_AWS4 = 27.99, 86.83, 5600

# AWS5 (Namche)
lat_AWS5, lon_AWS5, elev_AWS5 = 27.80, 86.71, 3570

# Pyramid (monthly level 2)
lat_Pyr, lon_Pyr, elev_Pyr = 27.96, 86.81, 5035

# Define metadata as a list of dicts
stations_info_salerno = [
    {"ID": "AWSSC", "Name": "South Col", "Lat": 27.98, "Lon": 86.76, "Elev_m": 7986, "Timestep": "1h"},
    {"ID": "CNG_SNP", "Name": "Changri Nup", "Lat": 27.96, "Lon": 86.93, "Elev_m": 5700, "Timestep": "1h"},
    {"ID": "AWS0", "Name": "Pyramid", "Lat": 27.96, "Lon": 86.81, "Elev_m": 5035, "Timestep": "1h"},
    {"ID": "AWS1", "Name": "Pyramid", "Lat": 27.96, "Lon": 86.81, "Elev_m": 5035, "Timestep": "1h"},
    {"ID": "AWS2", "Name": "Pheriche", "Lat": 27.90, "Lon": 86.82, "Elev_m": 4260, "Timestep": "1h"},
    {"ID": "AWS3", "Name": "Lukla", "Lat": 27.70, "Lon": 86.72, "Elev_m": 2660, "Timestep": "1h"},
    {"ID": "AWS4", "Name": "Kala Patthar", "Lat": 27.99, "Lon": 86.83, "Elev_m": 5600, "Timestep": "1h"},
    {"ID": "AWS5", "Name": "Namche", "Lat": 27.80, "Lon": 86.71, "Elev_m": 3570, "Timestep": "1h"},
    {"ID": "PYmon", "Name": "Pyramid (monthly)", "Lat": 27.96, "Lon": 86.81, "Elev_m": 5035, "Timestep": "1month"},
]

# Create DataFrame
df_stations_salerno = pd.DataFrame(stations_info_salerno)

# Display
print(df_stations_salerno)


# In[ ]:


#Nat geo
#BASE CAMP AWS (27.9952 N, 86.8406 E, 5315 M ASL)
lat_bc,lon_bs,elev_bc=27.9952, 86.8406, 5315
#CAMP II AWS (27.9810 N, 86.9023 E, 6464 M ASL)
lat_c2,lon_c2,elev_c2=27.9810, 86.9023, 6464 
#PHORTSE AWS (27.8456 N, 86.7472 E, 3810 M ASL)
lat_phort,lon_phort,elev_phort=27.8456, 86.7472, 3810 
#BISHOP ROCK AWS (27.9735 N, 86.9308 E, 8810 M ASL)
lat_bish,lon_bish,elev_bish=27.9735, 86.9308, 8810 
#MT. EVEREST SOUTH COL AWS (27.9719 N, 86.9295 E, 7945 M ASL)
lat_sc,lon_sc,elev_sc=27.9719, 86.9295, 7945


# Define metadata for Everest AWS network
stations_info_everest = [
    {"ID": "bc", "Name": "BaseCampAWS", "Lat": 27.9952, "Lon": 86.8406, "Elev_m": 5315},
    {"ID": "c2", "Name": "Camp II AWS", "Lat": 27.9810, "Lon": 86.9023, "Elev_m": 6464},
    {"ID": "phort", "Name": "Phortse AWS", "Lat": 27.8456, "Lon": 86.7472, "Elev_m": 3810},
    {"ID": "bc", "Name": "Bishop Rock AWS", "Lat": 27.9735, "Lon": 86.9308, "Elev_m": 8810},
    {"ID": "sc", "Name": "Mt. Everest South Col AWS", "Lat": 27.9719, "Lon": 86.9295, "Elev_m": 7945},
]

# Create DataFrame
df_everest_stations = pd.DataFrame(stations_info_everest)

# Display
print(df_everest_stations)


# In[ ]:


# --- Merge all station metadata into one unified dictionary ---
stations_all = {}

# Add Salerno AWS
for sta in stations_info_salerno:
    stations_all[sta["ID"]] = (sta["Lat"], sta["Lon"], "SalernoAWS")

# Add Glacioclim AWS
for sta in stations_info_glacioclim:
    stations_all[sta["ID"]] = (sta["Lat"], sta["Lon"], "Glacioclim")

# Add NatGeo / Everest AWS
for sta in stations_info_everest:
    stations_all[sta["ID"]] = (sta["Lat"], sta["Lon"], "NatGeo")

# Check summary
print(f"Total stations merged: {len(stations_all)}")
print(stations_all.keys())


# In[ ]:


lat,lon=LATS,LONS
# --------------------------
def nearest_ij(lat2d, lon2d, lat, lon):
    """Return nearest (j, i) indices in the model grid."""
    dist = np.hypot(lat2d - lat, lon2d - lon)
    j, i = np.unravel_index(np.nanargmin(dist), dist.shape)
    return j, i

# --------------------------
# Compute indices + collect summary
# --------------------------
nearest_indices = {}
rows = []

for name, (lat_sta, lon_sta, group) in stations_all.items():
    j, i = nearest_ij(lat, lon, lat_sta, lon_sta)
    nearest_indices[name] = (j, i)
    rows.append({
        "ID": name,
        "Group": group,
        "Station_Lat": lat_sta,
        "Station_Lon": lon_sta,
        "Grid_j": j,
        "Grid_i": i,
        "Model_Lat": float(lat[j, i]),
        "Model_Lon": float(lon[j, i]),
        "Model_Elev_m": float(dsSH.values[j, i])
    })

df_station_to_grid = pd.DataFrame(rows).sort_values(["Group", "ID"]).reset_index(drop=True)

print(df_station_to_grid.to_string(index=False))


# In[ ]:


# --------------------------
# Salerno
jAWS0, iAWS0   = nearest_indices["AWS0"]
jAWS1, iAWS1   = nearest_indices["AWS1"]
jAWS2, iAWS2   = nearest_indices["AWS2"]
jAWS3, iAWS3   = nearest_indices["AWS3"]
jAWS4, iAWS4   = nearest_indices["AWS4"]
jAWS5, iAWS5   = nearest_indices["AWS5"]
jAWSSC, iAWSSC = nearest_indices["AWSSC"]
jCNG, iCNG     = nearest_indices["CNG_SNP"]
jPYR2, iPYR2   = nearest_indices["PYmon"]

# Glacioclim
jMN, iMN = nearest_indices["MN"]
jCH, iCH = nearest_indices["CH"]
jML, iML = nearest_indices["ML"]
jKH, iKH = nearest_indices["KH"]
jPH, iPH = nearest_indices["PH"]
jPY, iPY = nearest_indices["PY"]
jMS, iMS = nearest_indices["MS"]
jMC, iMC = nearest_indices["MC"]

# NatGeo (Everest)
jbc, ibc     = nearest_indices["bc"]
jc2, ic2     = nearest_indices["c2"]
jphort, iphort = nearest_indices["phort"]
jbish, ibish   = nearest_indices["bc"]
jsc, isc       = nearest_indices["sc"]

# Optional: save lookup table
df_station_to_grid.to_csv("/bettik/PROJECTS/pr-regional-climate/santolam/station_grid_lookup_MARnxny10.csv", index=False)


# In[ ]:


##Glacio
#rr_daily_PY=RR_PY.resample(time='D').sum()
#rr_daily_PH=RR_PH.resample(time='D').sum()
#rr_daily_KH=RR_KH.resample(time='D').sum()

#idatePY = str(rr_daily_PY.time[0].values)[:10]
#fdatePY = str(rr_daily_PY.time[-1].values)[:10]
#idatePH = str(rr_daily_PH.time[0].values)[:10]
#fdatePH = str(rr_daily_PH.time[-1].values)[:10]
#idateKH = str(rr_daily_KH.time[0].values)[:10]
#fdateKH = str(rr_daily_KH.time[-1].values)[:10]

ts_RF_PH=ds_RF[:,jPH,iPH].sel(time=slice(idatePH,fdatePH))
ts_SF_PH=ds_SF[:,jPH,iPH].sel(time=slice(idatePH,fdatePH))
ts_TF_PH=ts_RF_PH+ts_SF_PH

ts_RF_KH=ds_RF[:,jKH,iKH].sel(time=slice(idateKH,fdateKH))
ts_SF_KH=ds_SF[:,jKH,iKH].sel(time=slice(idateKH,fdateKH))
ts_TF_KH=ts_RF_KH+ts_SF_KH


ts_RF_PY=ds_RF[:,jPY,iPY].sel(time=slice(idatePY,fdatePY))
ts_SF_PY=ds_SF[:,jPY,iPY].sel(time=slice(idatePY,fdatePY))
ts_TF_PY=ts_RF_PY+ts_SF_PY


# In[ ]:





# In[ ]:





# In[ ]:


## Salerno
# Daily total precipitation (sum of hourly rates)
#rr_AWS0_daily = df_AWS0['RR'].resample('D').sum()
#rr_AWS1_daily = df_AWS1['RR'].resample('D').sum()
#rr_AWS2_daily = df_AWS2['RR'].resample('D').sum()
#rr_AWS3_daily = df_AWS3['RR'].resample('D').sum()
#rr_AWS4_daily = df_AWS4['RR'].resample('D').sum()
#rr_AWS5_daily = df_AWS5['RR'].resample('D').sum()
#jAWS0, iAWS0 
# --- Define date ranges for each AWS based on observations ---
idate_AWS0 = str(rr_AWS0_daily.index[0].date())
fdate_AWS0 = str(rr_AWS0_daily.index[-1].date())
idate_AWS1 = str(rr_AWS1_daily.index[0].date())
fdate_AWS1 = str(rr_AWS1_daily.index[-1].date())
idate_AWS2 = str(rr_AWS2_daily.index[0].date())
fdate_AWS2 = str(rr_AWS2_daily.index[-1].date())
idate_AWS3 = str(rr_AWS3_daily.index[0].date())
fdate_AWS3 = str(rr_AWS3_daily.index[-1].date())
idate_AWS4 = str(rr_AWS4_daily.index[0].date())
fdate_AWS4 = str(rr_AWS4_daily.index[-1].date())
idate_AWS5 = str(rr_AWS5_daily.index[0].date())
fdate_AWS5 = str(rr_AWS5_daily.index[-1].date())

# --- Compute RF, SF, TF for each AWS station ---
ts_RF_AWS0 = ds_RF[:, jAWS0, iAWS0].sel(time=slice(idate_AWS0, fdate_AWS0))
ts_SF_AWS0 = ds_SF[:, jAWS0, iAWS0].sel(time=slice(idate_AWS0, fdate_AWS0))
ts_TF_AWS0 = ts_RF_AWS0 + ts_SF_AWS0

ts_RF_AWS1 = ds_RF[:, jAWS1, iAWS1].sel(time=slice(idate_AWS1, fdate_AWS1))
ts_SF_AWS1 = ds_SF[:, jAWS1, iAWS1].sel(time=slice(idate_AWS1, fdate_AWS1))
ts_TF_AWS1 = ts_RF_AWS1 + ts_SF_AWS1

ts_RF_AWS2 = ds_RF[:, jAWS2, iAWS2].sel(time=slice(idate_AWS2, fdate_AWS2))
ts_SF_AWS2 = ds_SF[:, jAWS2, iAWS2].sel(time=slice(idate_AWS2, fdate_AWS2))
ts_TF_AWS2 = ts_RF_AWS2 + ts_SF_AWS2

ts_RF_AWS3 = ds_RF[:, jAWS3, iAWS3].sel(time=slice(idate_AWS3, fdate_AWS3))
ts_SF_AWS3 = ds_SF[:, jAWS3, iAWS3].sel(time=slice(idate_AWS3, fdate_AWS3))
ts_TF_AWS3 = ts_RF_AWS3 + ts_SF_AWS3

ts_RF_AWS4 = ds_RF[:, jAWS4, iAWS4].sel(time=slice(idate_AWS4, fdate_AWS4))
ts_SF_AWS4 = ds_SF[:, jAWS4, iAWS4].sel(time=slice(idate_AWS4, fdate_AWS4))
ts_TF_AWS4 = ts_RF_AWS4 + ts_SF_AWS4

ts_RF_AWS5 = ds_RF[:, jAWS5, iAWS5].sel(time=slice(idate_AWS5, fdate_AWS5))
ts_SF_AWS5 = ds_SF[:, jAWS5, iAWS5].sel(time=slice(idate_AWS5, fdate_AWS5))
ts_TF_AWS5 = ts_RF_AWS5 + ts_SF_AWS5


# In[ ]:


##Nat geo
##
#rr_bc_daily = df_bc['PRECIP'].resample('D').sum()
#rr_phort_daily = df_phort['PRECIP'].resample('D').sum()
idate_bc     = str(rr_bc_daily.index[0].date())
fdate_bc     = str(rr_bc_daily.index[-1].date())

idate_phort  = str(rr_phort_daily.index[0].date())
fdate_phort  = str(rr_phort_daily.index[-1].date())

ts_RF_bc = ds_RF[:, jbc, ibc].sel(time=slice(idate_bc, fdate_bc))
ts_SF_bc = ds_SF[:, jbc, ibc].sel(time=slice(idate_bc, fdate_bc))
ts_TF_bc = ts_RF_bc + ts_SF_bc

# --- Phortse ---
ts_RF_phort = ds_RF[:, jphort, iphort].sel(time=slice(idate_phort, fdate_phort))
ts_SF_phort = ds_SF[:, jphort, iphort].sel(time=slice(idate_phort, fdate_phort))
ts_TF_phort = ts_RF_phort + ts_SF_phort


# In[ ]:


import matplotlib.pyplot as plt

# --- Observed daily precipitation series ---
stations_rr_daily_glacioclim = {
    "Pheriche": rr_daily_PH,
    "Khare": rr_daily_KH,
    "Pyramid": rr_daily_PY
}

# --- Model total fall (rain + snow) ---
ts_TF_model_glacioclim = {
    "Pheriche": ts_TF_PH,
    "Khare": ts_TF_KH,
    "Pyramid": ts_TF_PY
}

# --- Station elevations (manually defined or from metadata) ---
elev_station_glacioclim = {
    "Pheriche": 4240,  # m
    "Khare": 4900,
    "Pyramid": 5050
}

# --- Model elevations from dsSH field ---
elev_model_glacioclim = {
    "Pheriche": float(dsSH[jPH, iPH]),
    "Khare": float(dsSH[jKH, iKH]),
    "Pyramid": float(dsSH[jPY, iPY])
}


# In[ ]:


#rr_daily_PH


# In[ ]:


stations_rr_daily_glacioclim = {
    "Pheriche": rr_daily_PH,
    "Khare": rr_daily_KH,
    "Pyramid": rr_daily_PY
}

elev_station_glacioclim = {
    "Pheriche": 4240,  # m
    "Khare": 4900,
    "Pyramid": 5050
}

jjas_months = [6, 7, 8, 9]
year = 2016  # <-- selected year

print(f"JJAS means for {year}:")
for station, ds in stations_rr_daily_glacioclim.items():
    
    JJAS_year = ds.sel(time=slice(f"{year}-06-01", f"{year}-09-30"))
    JJAS_year_mean = JJAS_year.mean(dim="time")
    
    print(f"{station}','{elev_station_glacioclim[station]}','{float(JJAS_year_mean.values):.2f}")


# In[ ]:


#JJAS_year_PH=rr_daily_PH.sel(time=slice(str(year)+"-06-01",str(year)+"-09-30"))
#JJAS_year_PH_mean=JJAS_year_PH.mean(dim='time')
#JJAS_year_PH_mean


# In[ ]:





# In[ ]:





# In[ ]:


# --- Observed daily total precipitation ---
stations_rr_daily_salerno = {
    "AWS0": rr_AWS0_daily,
    "AWS1": rr_AWS1_daily,
    "AWS2": rr_AWS2_daily,
    "AWS3": rr_AWS3_daily,
    "AWS4": rr_AWS4_daily,
    "AWS5": rr_AWS5_daily,
}

# --- Model total fall (rain + snow) for each AWS station ---
ts_TF_model_salerno = {
    "AWS0": ts_TF_AWS0,
    "AWS1": ts_TF_AWS1,
    "AWS2": ts_TF_AWS2,
    "AWS3": ts_TF_AWS3,
    "AWS4": ts_TF_AWS4,
    "AWS5": ts_TF_AWS5,
}

# --- Station elevation (m) ---
elev_station_salerno = {
    "AWS0": elev_AWS0,
    "AWS1": elev_AWS1,
    "AWS2": elev_AWS2,
    "AWS3": elev_AWS3,
    "AWS4": elev_AWS4,
    "AWS5": elev_AWS5,
}

# --- Model grid elevation (from your elevation field, e.g. field_SH) ---
elev_model_salerno = {
    "AWS0": float(dsSH[jAWS0, iAWS0]),
    "AWS1": float(dsSH[jAWS1, iAWS1]),
    "AWS2": float(dsSH[jAWS2, iAWS2]),
    "AWS3": float(dsSH[jAWS3, iAWS3]),
    "AWS4": float(dsSH[jAWS4, iAWS4]),
    "AWS5": float(dsSH[jAWS5, iAWS5]),
}

# --- Create subplots ---


# In[ ]:


#rr_AWS0_daily


# In[ ]:


stations_rr_daily_salerno = {
    "AWS0": rr_AWS0_daily,
    "AWS1": rr_AWS1_daily,
    "AWS2": rr_AWS2_daily,
    "AWS3": rr_AWS3_daily,
    "AWS4": rr_AWS4_daily,
    "AWS5": rr_AWS5_daily,
}


# --- Station elevation (m) ---
elev_station_salerno = {
    "AWS0": elev_AWS0,
    "AWS1": elev_AWS1,
    "AWS2": elev_AWS2,
    "AWS3": elev_AWS3,
    "AWS4": elev_AWS4,
    "AWS5": elev_AWS5,
}

#

jjas_months = [6, 7, 8, 9]
year = 2016  # <-- selected year

print(f"JJAS means for {year}:")
for station, series in stations_rr_daily_salerno.items():

    # Select the JJAS period using pandas datetime index
    JJAS_year = series.loc[f"{year}-06-01":f"{year}-09-30"]

    # Compute mean
    JJAS_year_mean = JJAS_year.mean()

    print(f"{station}','{elev_station_salerno[station]}','{JJAS_year_mean:.2f}")


# In[ ]:





# In[ ]:


rr_phort_daily[rr_phort_daily < -100] = np.nan


# In[ ]:





# In[ ]:



# --- Observed daily total precipitation ---
stations_rr_daily_natgeo = {
    "BaseCamp": rr_bc_daily,
    "Phortse": rr_phort_daily,
}

# --- Model total fall (rain + snow) for each station ---
ts_TF_model_natgeo = {
    "BaseCamp": ts_TF_bc,
    "Phortse": ts_TF_phort,
}

# --- Station elevation (from your metadata) ---
elev_station_natgeo = {
    "BaseCamp": 5315,  # from your stations_info_everest
    "Phortse": 3810,
}

# --- Model grid elevation (from your elevation field) ---
elev_model_natgeo = {
    "BaseCamp": float(dsSH[jbc, ibc]),
    "Phortse": float(dsSH[jphort, iphort]),
}


# In[ ]:


#rmse,bias,r
import numpy as np
from scipy.stats import pearsonr

print("=== glacioclim Stations – TF vs Observations ===\n")
bias_list_glacioclim = []
rmse_list_glacioclim = []
corr_list_glacioclim = []
names_glacioclim= []
rbias_list_glacioclim=[]

for name in stations_rr_daily_glacioclim.keys():
    # Observed series
    obs = stations_rr_daily_glacioclim[name]

    # Model series (original)
    mod = ts_TF_model_glacioclim[name].to_pandas()
        
    # Mask model where obs is NaN
    mask = ~np.isnan(obs.values)
    obs_masked = obs.values[mask]
    mod_masked = mod.values[mask]
    mean_obs = np.mean(obs_masked)
    
    # --- Original model ---
    rmse = np.sqrt(np.mean((mod_masked - obs_masked)**2))
    bias = np.mean(mod_masked - obs_masked)
    corr = pearsonr(mod_masked, obs_masked)[0]
    if np.isclose(mean_obs, 0):
        rbias = np.nan

    rbias = (bias / mean_obs) * 100.0

    print(f"{name}  | Original: RMSE={rmse:.2f}, Bias={bias:.2f}, RBias={rbias:.2f}, meanobs={mean_obs:.2f}, R={corr:.2f}  ")
    # Store
    bias_list_glacioclim.append(bias)
    rmse_list_glacioclim.append(rmse)
    corr_list_glacioclim.append(corr)
    names_glacioclim.append(name)
    rbias_list_glacioclim.append(rbias)
 


# In[ ]:





# In[ ]:


print("=== Salerno Stations – TF vs Observations ===\n")
bias_list_salerno = []
rmse_list_salerno = []
corr_list_salerno = []
names_salerno = []
rbias_list_salerno=[]

for name in stations_rr_daily_salerno.keys():
    # Observed series
    obs = stations_rr_daily_salerno[name]

    # Model series (original)
    mod = ts_TF_model_salerno[name].to_pandas()
     
    # Mask model where obs is NaN
    mask = ~np.isnan(obs.values)
    obs_masked = obs.values[mask]
    mod_masked = mod.values[mask]
    mean_obs = np.mean(obs_masked)
    
    # --- Original model ---
    rmse = np.sqrt(np.mean((mod_masked - obs_masked)**2))
    bias = np.mean(mod_masked - obs_masked)
    corr = pearsonr(mod_masked, obs_masked)[0]
    if np.isclose(mean_obs, 0):
        rbias = np.nan

    rbias = (bias / mean_obs) * 100.0
    print(f"{name}  | Original: RMSE={rmse:.2f}, Bias={bias:.2f}, RBias={rbias:.2f}, meanobs={mean_obs:.2f}, R={corr:.2f}  ")

    # Store
    bias_list_salerno.append(bias)
    rmse_list_salerno.append(rmse)
    corr_list_salerno.append(corr)
    names_salerno.append(name)
    rbias_list_salerno.append(rbias)


# In[ ]:


print("=== natgeo Stations – TF vs Observations ===\n")
# --- Initialize lists for Salerno group ---
bias_list_natgeo = []
rmse_list_natgeo = []
corr_list_natgeo = []
names_natgeo = []
rbias_list_natgeo=[]

for name in stations_rr_daily_natgeo.keys():
    # Observed series
    obs = stations_rr_daily_natgeo[name]

    # Model series (original)
    mod = ts_TF_model_natgeo[name].to_pandas()
     # Mask model where obs is NaN
    mask = ~np.isnan(obs.values)
    obs_masked = obs.values[mask]
    mod_masked = mod.values[mask]
    mean_obs = np.mean(obs_masked)
    
    # --- Original model ---
    rmse = np.sqrt(np.mean((mod_masked - obs_masked)**2))
    bias = np.mean(mod_masked - obs_masked)
    corr = pearsonr(mod_masked, obs_masked)[0]
    if np.isclose(mean_obs, 0):
        rbias = np.nan

    rbias = (bias / mean_obs) * 100.0
    
    print(f"{name}  | Original: RMSE={rmse:.2f}, Bias={bias:.2f}, RBias={rbias:.2f}, meanobs={mean_obs:.2f}, R={corr:.2f}  ")

    
    # Store
    bias_list_natgeo.append(bias)
    rmse_list_natgeo.append(rmse)
    corr_list_natgeo.append(corr)
    names_natgeo.append(name)
    rbias_list_natgeo.append(rbias)


# In[ ]:


rbias_list_natgeo


# In[ ]:


# Groups
groups = ['Glacioclim', 'Ev-K2-CNR', 'NatGeo']


# In[ ]:


#names_lists


# In[ ]:


elev_stations= [elev_station_glacioclim, elev_station_salerno, elev_station_natgeo]

bias_lists = [bias_list_glacioclim, bias_list_salerno, bias_list_natgeo]
rbias_lists = [rbias_list_glacioclim, rbias_list_salerno, rbias_list_natgeo]
rmse_lists = [rmse_list_glacioclim, rmse_list_salerno, rmse_list_natgeo]
corr_lists = [corr_list_glacioclim, corr_list_salerno, corr_list_natgeo]
names_lists = [names_glacioclim, names_salerno, names_natgeo]


# In[ ]:





# In[ ]:


#              ERA5             HARv2
#              r   Bias SD RMSE r Bias SD RMSE
#P (mm day21) 0.63 0.5 3.7 3.7  0.60 0.9 5.2 5.3
#Pheriche
#P (mm day21) 0.62 1.4 4.6 4.8  0.67 1.1 5.4 5.5
#Khare
#P (mm day21) 0.68 1.8 6.0 6.3  0.66 2.8 8.8 9.2
#Khadka_et_al_2022 (a The subscript i stands for daily means, obtained from hourly values.When the hourly values from the AWS are missing, the corresponding
#hourly values from ERA5L and HARv2 are discarded. The overbar (i.e., x and y) stands for mean values over the entire studied period or
#over each season.)


# In[ ]:


print('ok')


# In[ ]:


print(groups, bias_lists, corr_lists, names_lists, elev_stations)


# In[ ]:


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm

# One marker per group (cycling)
group_markers = ['o', 's', '^', 'D', 'P', 'X', '*']

fig, ax = plt.subplots(figsize=(10,8))

# Correlation shading bins (0 → 1)
bins = np.arange(0., 1.05, 0.05)
norm = BoundaryNorm(bins, ncolors=256, clip=True)
cmap = cm.viridis   # better for correlation

legend_handles = []
added_groups = set()

# Loop over groups
for gi, (group, bias_list, corr_list, names_lr, elevs) in enumerate(
        zip(groups, bias_lists, corr_lists, names_lists, elev_stations)
    ):

    marker = group_markers[gi % len(group_markers)]

    for i, name in enumerate(names_lr):

        elev = elevs[name]          # y-axis
        bias = bias_list[i]      # x-axis
        r    = corr_list[i]      # shading

        # Scatter point
        sc = ax.scatter(
            bias, elev,
            s=220,
            marker=marker,
            c=[r], cmap=cmap, norm=norm,
            edgecolor='k', zorder=6
        )
        
        if name in ['MeraLa',]:
            ax.text(
            bias - 0.2,
            elev + 140,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )

        elif name in ['AWS0','AWS2']:
            ax.text(
            bias + 0.02,
            elev + 80,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )
        elif name in ['AWS4']:
            ax.text(
            bias+ 0.06 ,
            elev - 10,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )
        elif name in ['BishopRock']:
            ax.text(
            bias - 0.5,
            elev + 100,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )

        else:
        # Station label offset slightly
            ax.text(
            bias - 0.126,
            elev + 80,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )

    # Add legend entry (one per group)
    if group not in added_groups:
        added_groups.add(group)
        legend_handles.append(
            Line2D([0], [0],
                   marker=marker, linestyle='None',
                   markersize=12, markerfacecolor="white",
                   markeredgecolor='k',
                   label=group)
        )

# ---- Formatting ----
ax.set_xlabel('Bias [mm/day]', fontsize=16)
ax.set_ylabel('Elevation [m]', fontsize=16)
#ax.set_title('Temperature: Elevation vs LR-corrected Bias(R)',
#             fontsize=18)#, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.4)
#ax.axvline(x=0, linestyle='-', color='grey')
ax.tick_params(axis='both', labelsize=14)

ax.text(
    0.02, 0.98, 'c)',
    transform=ax.transAxes,
    fontsize=18,
    fontweight='bold',
    ha='left',
    va='top'
)

# ---- Legend ----
ax.legend(handles=legend_handles,
          fontsize=13,
          frameon=True,
          loc='lower left')

# ---- Colorbar: correlation ----
cbar = plt.colorbar(sc, ax=ax, boundaries=bins, ticks=bins)
cbar.set_label('R')#, fontsize=14)
#cbar.ax.tick_params(labelsize=12)

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "figure.titlesize": 18,
})

plt.tight_layout()

plotname = f'FIG8c_pre.bias_stations_{domainM}'
plt.savefig(f"{plotsDir}{plotname}.png", bbox_inches="tight", dpi=300)
print(f"Saved: {plotsDir}{plotname}.png")

plt.show()


# In[ ]:





# In[ ]:





# In[ ]:


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm

# One marker per group (cycling)
group_markers = ['o', 's', '^', 'D', 'P', 'X', '*']

fig, ax = plt.subplots(figsize=(10,8))

# Correlation shading bins (0 → 1)
bins = np.arange(0., 1.05, 0.05)
norm = BoundaryNorm(bins, ncolors=256, clip=True)
cmap = cm.viridis   # better for correlation

legend_handles = []
added_groups = set()

# Loop over groups
for gi, (group, rbias_list, corr_list, names_lr, elevs) in enumerate(
        zip(groups, rbias_lists, corr_lists, names_lists, elev_stations)
    ):

    marker = group_markers[gi % len(group_markers)]

    for i, name in enumerate(names_lr):

        elev = elevs[name]          # y-axis
        rbias = rbias_list[i]      # x-axis
        r    = corr_list[i]      # shading

        # Scatter point
        sc = ax.scatter(
            rbias, elev,
            s=220,
            marker=marker,
            c=[r], cmap=cmap, norm=norm,
            edgecolor='k', zorder=6
        )
        
        if name in ['MeraLa',]:
            ax.text(
            rbias - 0.2,
            elev + 140,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )

        elif name in ['AWS0','AWS2']:
            ax.text(
            rbias + 0.02,
            elev + 80,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )
        elif name in ['AWS4']:
            ax.text(
            rbias+ 0.06 ,
            elev - 10,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )
        elif name in ['BishopRock']:
            ax.text(
            rbias - 0.5,
            elev + 100,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )

        else:
        # Station label offset slightly
            ax.text(
            rbias - 0.126,
            elev + 80,
            name,
            fontsize=12,
            ha='left',
            va='bottom'
        )

    # Add legend entry (one per group)
    if group not in added_groups:
        added_groups.add(group)
        legend_handles.append(
            Line2D([0], [0],
                   marker=marker, linestyle='None',
                   markersize=12, markerfacecolor="white",
                   markeredgecolor='k',
                   label=group)
        )

# ---- Formatting ----
ax.set_xlabel('Relative Bias [%]', fontsize=16)
ax.set_ylabel('Elevation [m]', fontsize=16)
#ax.set_title('Temperature: Elevation vs LR-corrected Bias(R)',
#             fontsize=18)#, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.4)
#ax.axvline(x=0, linestyle='-', color='grey')
ax.tick_params(axis='both', labelsize=14)

ax.text(
    0.02, 0.98, 'c)',
    transform=ax.transAxes,
    fontsize=18,
    fontweight='bold',
    ha='left',
    va='top'
)

# ---- Legend ----
ax.legend(handles=legend_handles,
          fontsize=13,
          frameon=True,
          loc='lower right')

# ---- Colorbar: correlation ----
cbar = plt.colorbar(sc, ax=ax, boundaries=bins, ticks=bins)
cbar.set_label('R')#, fontsize=14)
#cbar.ax.tick_params(labelsize=12)

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "figure.titlesize": 18,
})

plt.tight_layout()


plotname = f'FIG8c_pre_LR_relbiasX_elevY_colorR_groupMarkers_{domainM}'
plt.savefig(f"{plotsDir}{plotname}.png", bbox_inches="tight", dpi=300)
print(f"Saved: {plotsDir}{plotname}.png")

plt.show()


# In[ ]:


fz=18


# In[ ]:


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm

# One marker per group (cycling)
group_markers = ['o', 's', '^', 'D', 'P', 'X', '*']

fig, ax = plt.subplots(figsize=(10,8))

# Correlation shading bins (0 → 1)
bins = np.arange(0., 1.05, 0.05)
norm = BoundaryNorm(bins, ncolors=256, clip=True)
cmap = cm.viridis   # better for correlation

legend_handles = []
added_groups = set()

# Loop over groups
for gi, (group, rbias_list, corr_list, names_lr, elevs) in enumerate(
        zip(groups, rbias_lists, corr_lists, names_lists, elev_stations)
    ):

    marker = group_markers[gi % len(group_markers)]

    for i, name in enumerate(names_lr):

        elev = elevs[name]          # y-axis
        rbias = rbias_list[i]      # x-axis
        r    = corr_list[i]      # shading

        # Scatter point
        sc = ax.scatter(
            rbias, elev,
            s=220,
            marker=marker,
            c=[r], cmap=cmap, norm=norm,
            edgecolor='k', zorder=6
        )
        
        if name in ['MeraLa',]:
            ax.text(
            rbias - 0.2,
            elev + 140,
            name,
            fontsize=fz,
            ha='left',
            va='bottom'
        )

        elif name in ['AWS0','AWS2']:
            ax.text(
            rbias + 0.02,
            elev + 80,
            name,
            fontsize=fz,
            ha='left',
            va='bottom'
        )
        elif name in ['AWS4']:
            ax.text(
            rbias+ 0.06 ,
            elev - 10,
            name,
            fontsize=fz,
            ha='left',
            va='bottom'
        )
        elif name in ['BishopRock']:
            ax.text(
            rbias - 0.5,
            elev + 100,
            name,
            fontsize=fz,
            ha='left',
            va='bottom'
        )

        else:
        # Station label offset slightly
            ax.text(
            rbias - 0.126,
            elev + 80,
            name,
            fontsize=fz,
            ha='left',
            va='bottom'
        )

    # Add legend entry (one per group)
    if group not in added_groups:
        added_groups.add(group)
        legend_handles.append(
            Line2D([0], [0],
                   marker=marker, linestyle='None',
                   markersize=12, markerfacecolor="white",
                   markeredgecolor='k',
                   label=group)
        )

# ---- Formatting ----
ax.set_xlabel('Relative Bias [%]', fontsize=fz)
ax.set_ylabel('Elevation [m]', fontsize=fz)
#ax.set_title('Temperature: Elevation vs LR-corrected Bias(R)',
#             fontsize=18)#, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.4)
#ax.axvline(x=0, linestyle='-', color='grey')
ax.tick_params(axis='both', labelsize=fz)

ax.text(
    0.02, 0.98, 'c)',
    transform=ax.transAxes,
    fontsize=fz,
    fontweight='bold',
    ha='left',
    va='top'
)

# ---- Legend ----
ax.legend(handles=legend_handles,
          fontsize=fz,
          frameon=True,
          loc='lower right')

# ---- Colorbar: correlation ----
cbar = plt.colorbar(sc, ax=ax, boundaries=bins, ticks=bins)
cbar.set_label('Correlation', fontsize=fz)
#cbar.ax.tick_params(labelsize=12)

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "figure.titlesize": 18,
})

plt.tight_layout()


plotname = f'FIG8c_pre_LR_relbiasX_elevY_colorR_groupMarkers_{domainM}_rev1'
plt.savefig(f"{plotsDir}{plotname}.png", bbox_inches="tight", dpi=300)
print(f"Saved: {plotsDir}{plotname}.png")

plt.show()


# In[ ]:


fz=18

station_acronyms = {}

for lst in [stations_info_everest,
            stations_info_salerno,
            stations_info_glacioclim]:
    for s in lst:
        station_acronyms[s["Name"]] = s["ID"]
        
station_acronyms.update({
    "MeraLa": "ML",
    "MeraNaulek": "MK",
    "MeraSummit": "MS",
    "Mera5770": "M57",
    "PyramidAWS": "PYG",
    "Pyramid": "PY",
    "BishopRock": "BIS",
    "SouthCol": "SC",
    "Phortse": "PHO",
    "Khare": "KH",
    "Pheriche": "PHE",
    "ChangriNup": "CNG",
    "CHA3": "CHA",
    "Camp2": "C2",
    "BaseCamp": "BC",
    "SouthCol": "SC",
    "BishopRock": "BIS",
    "Phortse": "PHO",
    "ChangriA3": "CHA",
    "MeraLa": "ML",
    "MeraNaulek": "MK",
    "MeraSummit": "MS",
    "Mera5770": "M57",

})


# In[ ]:


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm

# ----------------------------------------------------
# Manual label offsets (dx in % bias, dy in m)
# ----------------------------------------------------
label_offsets = {
    "ML":   (-0.20, 140),
    "MK":   ( 0.05,  80),
    "MS":   ( 0.08, 100),
    "M57":  (-0.10,  90),
    "PY":   ( 20,  60),
    "PYG":  ( 0.08,  80),
    "PHE":  ( 0.00, 100),
    "KH":   (20,  60),

    "BC":   (10,  60),
    "C2":   (-0.05,  80),
    "SC":   ( 0.00,  90),
    "PHO":  ( 0.05,  70),
    "BIS":  (-0.10, 100),

    "AWS0": ( 50.0,  80),
    "AWS1": (-20,  70),
    "AWS2": ( 0.02,  80),
    "AWS3": (-0.05,  70),
    "AWS4": ( -20., 50),
    "AWS5": (-0.05,  70),

    "CHA":  (-0.05,  80),
    "CNG":  (-0.05,  80),
}

# ----------------------------------------------------
# Figure
# ----------------------------------------------------
group_markers = ['o', 's', '^', 'D', 'P', 'X', '*']

fig, ax = plt.subplots(figsize=(10, 8))

bins = np.arange(0, 1.05, 0.05)
norm = BoundaryNorm(bins, ncolors=256, clip=True)
cmap = cm.viridis

legend_handles = []
added_groups = set()

# ----------------------------------------------------
# Plot
# ----------------------------------------------------
for gi, (group, rbias_list, corr_list, names_list, elevs) in enumerate(
    zip(groups, rbias_lists, corr_lists, names_lists, elev_stations)
):

    marker = group_markers[gi % len(group_markers)]

    for i, name in enumerate(names_list):

        elev = elevs[name]
        rbias = rbias_list[i]
        r = corr_list[i]

        sc = ax.scatter(
            rbias,
            elev,
            s=320,
            marker=marker,
            c=[r],
            cmap=cmap,
            norm=norm,
            edgecolor='k',
            linewidth=0.8,
            zorder=6
        )

        label = station_acronyms.get(name, name)

        dx, dy = label_offsets.get(label, (-0.05, 70))

        ax.text(
            rbias + dx,
            elev + dy,
            label,
            fontsize=fz,
            fontweight='bold',
            ha='center',
            va='bottom'
        )

    if group not in added_groups:
        added_groups.add(group)

        legend_handles.append(
            Line2D(
                [0], [0],
                marker=marker,
                linestyle='None',
                markersize=12,
                markerfacecolor='white',
                markeredgecolor='k',
                label=group
            )
        )

# ----------------------------------------------------
# Formatting
# ----------------------------------------------------
ax.set_xlabel('Relative Bias [%]', fontsize=fz)
ax.set_ylabel('Elevation [m]', fontsize=fz)
ax.set_ylim(2500,5800)

ax.grid(True, linestyle='--', alpha=0.4)
ax.tick_params(axis='both', labelsize=fz)

ax.text(
    0.02, 0.98,
    'c)',
    transform=ax.transAxes,
    fontsize=fz,
    fontweight='bold',
    ha='left',
    va='top'
)

ax.legend(
    handles=legend_handles,
    fontsize=22,
    frameon=True,
    loc='lower right'
)

cbar = plt.colorbar(
    sc,
    ax=ax,
    boundaries=bins,
    ticks=bins
)

cbar.set_label('Correlation', fontsize=fz)
plt.rcParams.update({
    "font.size": 18,
    "axes.labelsize": 18,
    "axes.titlesize": 18,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "legend.fontsize": 18,
    "figure.titlesize": 18,
})

plt.tight_layout()

plotname = f'FIG8c_pre_LR_relbiasX_elevY_colorR_groupMarkers_{domainM}_rev1'

plt.savefig(
    f"{plotsDir}{plotname}.png",
    dpi=300,
    bbox_inches='tight'
)

print(f"Saved: {plotsDir}{plotname}.png")

plt.show()


# In[ ]:





# In[ ]:


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm

# ----------------------------------------------------
# Label offsets (dx in mm/day, dy in m)
# ----------------------------------------------------
label_offsets = {
    # Glacioclim
    "ML":  (-0.08, 120),
    "MK":  ( 0.08,  70),
    "MS":  ( 0.08,  90),
    "M57": (-0.08,  80),
    "PY":  ( 0.06,  70),
    "PYG": ( 0.08,  80),
    "PHE": (-0.02,  70),
    "KH":  (-0.08,  70),

    # NatGeo
    "BC":  ( 0.10,  70),
    "C2":  (-0.08,  80),
    "SC":  ( 0.00,  90),
    "PHO": (-0.02,  70),
    "BIS": (-0.08, 100),

    # Ev-K2-CNR
    "AWS0": ( 0.08, 70),
    "AWS1": ( -0.08, 70),
    "AWS2": ( 0.04, 70),
    "AWS3": ( 0.00, 80),
    "AWS4": ( 0.06, 80),
    "AWS5": (-0.02, 70),

    # Other
    "CHA": (-0.05, 70),
    "CNG": (-0.05, 70),
}

# ----------------------------------------------------
# Figure
# ----------------------------------------------------
group_markers = ['o', 's', '^', 'D', 'P', 'X', '*']

fig, ax = plt.subplots(figsize=(10, 8))

bins = np.arange(0, 1.05, 0.05)
norm = BoundaryNorm(bins, ncolors=256, clip=True)
cmap = cm.viridis

legend_handles = []
added_groups = set()

# ----------------------------------------------------
# Plot
# ----------------------------------------------------
for gi, (group, bias_list, corr_list, names_list, elevs) in enumerate(
    zip(groups, bias_lists, corr_lists, names_lists, elev_stations)
):

    marker = group_markers[gi % len(group_markers)]

    for i, name in enumerate(names_list):

        bias = bias_list[i]
        elev = elevs[name]
        r = corr_list[i]

        sc = ax.scatter(
            bias,
            elev,
            s=320,
            marker=marker,
            c=[r],
            cmap=cmap,
            norm=norm,
            edgecolor='k',
            linewidth=0.8,
            zorder=6
        )

        label = station_acronyms.get(name, name)

        dx, dy = label_offsets.get(label, (0.05, 70))

        ax.text(
            bias + dx,
            elev + dy,
            label,
            fontsize=fz,
            fontweight='bold',
            ha='center',
            va='bottom'
        )

    if group not in added_groups:

        added_groups.add(group)

        legend_handles.append(
            Line2D(
                [0], [0],
                marker=marker,
                linestyle='None',
                markersize=12,
                markerfacecolor='white',
                markeredgecolor='k',
                label=group
            )
        )

# ----------------------------------------------------
# Formatting
# ----------------------------------------------------
ax.set_xlabel('Bias [mm/day]', fontsize=fz)
ax.set_ylabel('Elevation [m]', fontsize=fz)

ax.set_xlim(3.2, 6.3)
ax.set_ylim(2500, 6000)

ax.grid(True, linestyle='--', alpha=0.4)
ax.tick_params(axis='both', labelsize=fz)

ax.text(
    0.02,
    0.98,
    'c)',
    transform=ax.transAxes,
    fontsize=22,
    fontweight='bold',
    ha='left',
    va='top'
)

ax.legend(
    handles=legend_handles,
    fontsize=22,
    frameon=True,
    loc='lower left'
)

cbar = plt.colorbar(
    sc,
    ax=ax,
    boundaries=bins,
    ticks=bins
)

cbar.set_label('Correlation', fontsize=fz)

plt.rcParams.update({
    "font.size":18,
    "axes.labelsize":18,
    "axes.titlesize":18,
    "xtick.labelsize":18,
    "ytick.labelsize":18,
    "legend.fontsize":18,
    "figure.titlesize":18,
})

plt.tight_layout()

plotname = f'FIG8c_pre_biasX_elevY_colorR_groupMarkers_{domainM}_rev1'

plt.savefig(
    f"{plotsDir}{plotname}.png",
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {plotsDir}{plotname}.png")

plt.show()


# In[ ]:




