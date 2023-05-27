import subprocess
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


fn = 'data/tl_2019_us_primaryroads.zip'
df = gpd.read_file(fn)
df = df[df['FULLNAME'] == 'I- 5']

i5 = pd.concat([df, df.bounds], axis=1)

la_lat = 34.031350
sac_lat = 38.579285

i5 = i5[la_lat  < i5['miny']]
i5 = i5[sac_lat > i5['maxy']]


fn2 = 'data/west_coast.shp.zip'
west_coast = gpd.read_file(fn2)

def albers(df):
    return df.to_crs("ESRI:102003")
    
fig, ax = plt.subplots(figsize=(7,7))
albers(west_coast).boundary.plot(
    ax=ax, color='gray', linewidth=0.5)
albers(i5).plot(
    ax=ax, color='red', linewidth=2)

ofn = 'LA-SAC.png'
plt.savefig(ofn, dpi=300)

cmd = ['open','-a','Preview',ofn]
subprocess.run(cmd)
