# scrape data for a US Highway

'''
python3 scrape.py 101 CA,NV,WA
python3 scrape.py 24,40,50,160,285,491,550 CO
'''

import sys, subprocess
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

try:
    args = sys.argv[1:]
    highwayL = args[0].split(',')
    stateL = args[1].split(',')
    tmp = [int(hwy) for hwy in highwayL]  # just checking
except:
    print('example usage:')
    print('python3 scrape.py 101 CA,NV,WA')
    
# --------------------------------

fipsD = { 'AZ':'04','CA':'06','CO':'08',
          'ID':'16','MT':'30','NV':'32','NM':'35',
          'OR':'41','TX':'48','WA':'53','WY':'56'}

# sub for fips
template = 'data-us_highways/ tl_2020_%s_prisecroads.zip'

# --------------------------------

def get_df(state):
    fn = template % fipsD[state]
    return gpd.read_file(fn)

resultsL = list()
for state in stateL:
    df = get_df(state)
    sL = list()
    for hwy in highwayL:
        route = df[df['FULLNAME'] == 'US Hwy ' + hwy]
        sL.append(route)
    resultsL.append(pd.concat(sL))

if len(resultsL) > 1:
    results = pd.concat(resultsL)
else:
    results = resultsL[0]

ofn = 'us%s.shp.zip' % hwy
results.to_file(
    filename=ofn,
    driver='ESRI Shapefile')

# --------------------------------
# quick look

df = results
states = gpd.read_file('data/gz_2010_us_040_00_5m')

xmin,ymin,xmax,ymax = -125,25,-104,49
df = df.cx[xmin:xmax, ymin:ymax]
us48 = states.cx[xmin:xmax, ymin:ymax]

def albers(df):
    return df.to_crs("ESRI:102003")
    
fig, ax = plt.subplots(figsize=(7,7))
albers(us48).boundary.plot(
    ax=ax, color='gray', linewidth=0.5)
albers(df).plot(
    ax=ax, color='red', linewidth=1)

ofn = 'US Hwy %s.png' % hwy
plt.savefig(ofn, dpi=300)

cmd = ['open','-a','Preview',ofn]
subprocess.run(cmd)

