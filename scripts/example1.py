import matplotlib.pyplot as plt
import geopandas as gpd

path = 'data/gz_2010_us_040_00_5m'
gdf = gpd.read_file(path)

fig,ax = plt.subplots(figsize=(7,7))
gdf.boundary.plot(ax=ax, 
    color='blue', linewidth=1)
    
plt.savefig('example.png', dpi=300)

