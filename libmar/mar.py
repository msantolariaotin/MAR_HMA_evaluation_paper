##
##
#
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

import xarray as xr
#field10=dsM.rename({'TIME': 'time'})

def compute_snow_height(ZN2_k1,ZN3_k2,ICE):
    """
    Reconstruct snow thickness from
        ‑ ZN2 at k=1   (full‑ice sector)
        ‑ ZN3 at k=2   (land‑sector)
        ‑ ICE mask (%) on the same (Y, X) grid
    and return it as an xarray.DataArray with dims (TIME, Y, X).

    All three inputs must share the same Y and X dimension *names*.
    The ICE mask may lack the TIME axis; it is broadcast across TIME.
    """
    ICE_expanded = ICE.expand_dims(TIME=ZN2_k1.TIME)

    # ── 2. core formula, pure xarray so it stays lazy / dask‑aware ───
    snow = xr.where(
        ICE_expanded.values == 100,
        ZN2_k1.values,                                        # full ice
        xr.where(
            ICE_expanded.values == 0,
            ZN3_k2.values,                                    # no ice
            (ZN2_k1.values * ICE_expanded.values +
             ZN3_k2.values * (100 - ICE_expanded.values)) / 100      # mixed
        )
    )
    snow_da = xr.DataArray(
    snow,
    coords={
        "TIME": ZN2_k1["TIME"],
        "Y":    ZN2_k1["Y"],
        "X":    ZN2_k1["X"],
    },
    dims=("TIME", "Y", "X"),
    name="snow_height",
    attrs={
        "long_name": "Reconstructed snow thickness",
        "units":     ZN2_k1.attrs.get("units", "mm"),
        "notes":     "Computed from ZN2[k=1], ZN3[k=2] and ICE mask"
    },
)
    return snow_da


def xy_sel_dom(ds,domain):
    latS,latN,lonW,lonE,latlim,lonlim=dom.coord_domain(domain)
    lat_str = ''
    lon_str = ''
    other_dims_str = []
    for dim in ds.coords:
        print(dim)
        if dim in ['lat', 'latitude','LON']:
            lat_str = dim
        elif dim in ['lon', 'longitude','LAT']:
            lon_str = dim
        else:
            other_dims_str.append(dim)
    mask = (
        (latS < ds[lat_str]) & ( ds[lat_str] < latN)
    & (lonW < ds[lon_str]) & ( ds[lon_str] < lonE)
    )
    field_dom=ds.where(mask,drop=True)
    return field_dom

'''
Snow correction from spin up
# Extract the TIME coordinate
time = ds.TIME

# Find all 1st of January dates (excluding the first one, since nothing before it)
jan1 = time.where((time.dt.month == 1) & (time.dt.day == 1), drop=True)
jan1 = jan1[1:]  # skip very first Jan 1

# Prepare a cumulative correction array
correction = xr.zeros_like(ds.isel(TIME=0))

total_correction = []
current_shift = 0

for date in jan1:
    # Previous Dec 31
    prev_dec31 = date - np.timedelta64(1, "D")

    # Compute difference for all pixels
    diff = ds.sel(TIME=prev_dec31) - ds.sel(TIME=date)

    # Update cumulative correction
    current_shift = current_shift + diff

    # Store the correction valid for all times >= this Jan 1
    mask = time >= date
    correction = correction + xr.where(mask, diff, 0)

# Apply correction
ds_corrected = ds+ correction
'''