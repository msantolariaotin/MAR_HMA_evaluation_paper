This repository contains the code ( DOI: 10.5281/zenodo.23344344)  used to perform the analyses presented in the paper submitted to Geoscientific Model Development (GMD): 

**Contrasted climatologies in Pamir and Central Himalaya highlighted
from MAR high-resolution atmospheric reanalysis over 1950-2025**

María Santolaria-Otín<sup>1</sup>, Charles Amory<sup>1</sup>, Martin Ménégoz<sup>1</sup>, Fanny Brun<sup>1</sup>, Xavier Faïn<sup>1</sup>, Xavier Fettweis<sup>2</sup>,
Mondher Chekki<sup>1</sup>, Patrick Wagnon<sup>1</sup>, Dibas Shrestha<sup>3</sup>, Arbindra Khadka<sup>1</sup><sup>,3</sup>

<sup>1</sup>Univ. Grenoble Alpes, CNRS, INRAE, IRD, Grenoble INP, IGE, 38000 Grenoble, France
<sup>2</sup>Laboratory of Climatology, Department of Geography, SPHERES research unit, University of Liège, Liège, 4000, Belgium
<sup>3</sup>Central Department of Hydrology and Meteorology, Tribhuvan University, Kirtipur, Nepal

Correspondence to: María Santolaria-Otín (maria.santolaria-otin@univ-grenoble-alpes.fr)

**Abstract**
High Mountain Asia (HMA) hosts the largest mass of terrestrial ice outside the polar regions, where combined
glacier and snow melting with high precipitation rates supplies water to hundreds of millions of people. HMA hydroclimate is
controlled by complex topography that shapes the contrasting atmospheric circulation patterns of the monsoon influence in the
South and the westerly fluxes on the West, making particularly challenging the understanding of climate variability in this
area. Despite its importance, large observational gaps persist, particularly at high elevation, while the coarse resolution of
global climate products and the limited spatial or temporal coverage of existing high-resolution simulations hinder robust
analyses of long-term climate variability and trends. Here, we present high-resolution (7 km) simulations performed with the
regional climate model MARv3.14 over two climatically contrasted regions of HMA: the westerly-dominated Pamir and the
monsoon-dominated Central Himalaya. Covering the 1950–2025 period, these experiments constitute, to our knowledge, one
of the longest continuous high-resolution regional climate simulations available over these regions. Model skill is evaluated
using multiple gridded observational and reanalysis datasets, satellite-derived snow products, and extensive in situ
observations, with a particular focus on temperature, precipitation, snow cover, and strong precipitation events. MAR
successfully reproduces the main hydroclimatic characteristics of both regions despite their contrasting climatic influences. It
captures the seasonal evolution of temperature, ranging from nearly 30 °C in the lowlands to below −20 °C at the highest
elevations, the winter–spring precipitation maximum in the Pamir (up to ~110 mm × month⁻¹), the summer monsoon peak in
the Central Himalaya (up to ~550 mm × month⁻¹), and the seasonal migration of the snowline from ~3800 to ~4800 m in the
Pamir and from ~4700 to ~5400 m in the Central Himalaya. The evaluation reveals an elevation-dependent precipitation bias,
characterized by underestimated precipitation at low elevations (<40-60 mm × month⁻¹), and excessive snowfall accumulation
 at high elevations, which is associated with cold temperature bias (<2-4°C) and an excessive snow persistence. High-resolution
dynamical downscaling substantially improves the representation of orographic precipitation and its spatial distribution over
the Khumbu area compared to the driving ERA5 reanalysis. These simulations provide a new long-term climatic reference for
the Pamir and Central Himalaya and a validated modelling framework for investigating climate variability, cryosphere
evolution, and natural hazards, as well as high-resolution atmospheric forcing for impact models such as glacier mass balance,
snowpack, and hydrological models. The validated model configuration also provides a robust and 35 transferable framework for
extending the simulations to the entire High Mountain Asia domain.


**MAR model**
The MAR model code and additional documentation are available at:
https://gitlab.uliege.be/especes/mar/stable/

Further information on how to run the MAR model can be found in the https://gitlab.uliege.be/groups/especes/mar/-/wikis/home/ 

The MAR model simulations and associated outputs are permanently archived on Zenodo and are publicly available for the two study regions: Pamir (https://doi.org/10.5281/zenodo.23921900; Santolaria-Otín et al., 2026a) and Central Himalaya (https://doi.org/10.5281/zenodo.24011336; Santolaria-Otín et al., 2026b).  The specific configuration used to run the simulations over the High Mountain Asia region region is described in both Zenodo repositories.



**Data**

The observational and reanalysis datasets used in this study are publicly available from their respective repositories. 

-ERA5 reanalysis data are available from the Copernicus Climate Data Store (https://cds.climate.copernicus.eu/) and have been used at different temporal resolutions  (hourly, dailly and monthly; DOI: 10.24381/cds.adbb2d47, DOI: 10.24381/cds.50314f4c, DOI: 10.24381/cds.6860a573 , respectively). 

-ERA5-Land reanalysis data are also available from the Copernicus Climate Data Store  (https://cds.climate.copernicus.eu/, DOI: 10.24381/cds.e9c9c792 ). 

-HAR v2 can be obtained from the High Asia Refined Analysis project website (https://www.tu.berlin/klima/forschung/regionalklimatologie/hochasien/har/; https://data.klima.tu-berlin.de/HAR/v2/ ). 

-CRU TS4.05 is distributed by the Climatic Research Unit (University of East Anglia; https://crudata.uea.ac.uk/cru/data/hrg/; https://catalogue.ceda.ac.uk/uuid/c26a65020a5e4b80b20018f148556681/ ). 

-CHIRPS precipitation data are available from the Climate Hazards Center (https://www.chc.ucsb.edu/data/chirps/).

-APHRODITE precipitation data from the APHRODITE project (http://aphrodite.st.hirosaki-u.ac.jp/download/).

-GPCP monthly precipitation data from the NOAA Physical Sciences Laboratory (https://psl.noaa.gov/data/gridded/data.gpcp.html).

-The High Mountain Asia Snow Reanalysis (HMA-SR, Version 1) is available from the NASA National Snow and Ice Data Center (NSIDC; https://nsidc.org/data/hma_sr_d/versions/1)

-ESA Snow CCI SCFG v2.0 product is available through the ESA Climate Change Initiative data portal (https://climate.esa.int/en/projects/snow/). 

The in situ observations over the Khumbu region are publicly available from:

-The GLACIOCLIM programme (https://glacioclim.osug.fr)
-The National Geographic Perpetual Planet Everest expedition (https://www.nationalgeographic.org/projects/perpetual-planet/everest/weather-data/ ; Matthews et al., 2020)
-The Ev-K2-CNR project (https://doi.org/10.5281/zenodo.15211352 ; Salerno et al., 2025).

The GMTED2010 digital elevation model is available from the TEMIS data portal (https://www.temis.nl/data/gmted2010/index.php).

