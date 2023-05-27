# write new shapefiles
import geopandas as gpd
import pandas as pd

fipsD = { 'AZ':'04','CA':'06','CO':'08',
          'ID':'16','MT':'30','NV':'32',
          'NM':'35','OR':'41','TX':'48',
          'UT':'49','WA':'53','WY':'56'}

# 50 states + PR
df = gpd.read_file('data/gz_2010_us_040_00_5m')
tL = ['06','41','53']

# filter
CA = df[df['STATE'] == fipsD['CA']]
OR = df[df['STATE'] == fipsD['OR']]
WA = df[df['STATE'] == fipsD['WA']]

ID = df[df['STATE'] == fipsD['ID']]
NV = df[df['STATE'] == fipsD['NV']]
AZ = df[df['STATE'] == fipsD['AZ']]
MT = df[df['STATE'] == fipsD['MT']]
UT = df[df['STATE'] == fipsD['UT']]
CO = df[df['STATE'] == fipsD['CO']]
NM = df[df['STATE'] == fipsD['NM']]
WY = df[df['STATE'] == fipsD['WY']]

west_coast = pd.concat([CA,OR,WA])
west_region = pd.concat(
    [CA,OR,WA,ID,NV,AZ,MT,UT,CO,NM,WY])

ofn = 'west_coast.shp.zip'
west_coast.to_file(
    filename=ofn,
    driver='ESRI Shapefile')

ofn = 'western_states.shp.zip'
west_region.to_file(
    filename=ofn,
    driver='ESRI Shapefile')
