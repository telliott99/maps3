import sys, subprocess
import geopandas as gpd
import matplotlib.pyplot as plt

def albers(df):
    return df.to_crs("ESRI:102003")

target = sys.argv[1]
df = gpd.read_file(target + '.shp.zip')

#------------------------------------
    
fig, ax = plt.subplots(figsize=(7,7))
albers(df).boundary.plot(
    ax=ax, color='gray', linewidth=0.5)

ofn = '%s.png' % target
plt.savefig(ofn, dpi=300)

cmd = ['open','-a','Preview',ofn]
subprocess.run(cmd)
