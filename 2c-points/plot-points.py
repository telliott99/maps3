# we get the highway data directly from the shapefile

import sys
import subprocess, csv
from stuff import geto

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# -------------

def get_highway(name,fn):
    df = gpd.read_file(fn)
    df = df[df['FULLNAME'] == name]
    return df

def filter_bounds(
    df,vmin,vmax,latitude=True):
    # the pandas way
    df = pd.concat([df, df.bounds], axis=1)
    if latitude:
        df = df[df['miny'] > vmin]
        df = df[df['maxy'] < vmax]
    else:
        df = df[df['minx'] > vmin]
        df = df[df['maxx'] < vmax]
    return df

# -------------

# plot and show

def albers(df):
    return df.to_crs("ESRI:102003")

def plot(hwy,df,region):
    # outlines of region
    fn = 'data/%s.shp.zip' % region
    outlines = gpd.read_file(fn)
    
    fig, ax = plt.subplots(figsize=(7,7))
    
    albers(outlines).boundary.plot(
        ax=ax, color='green', linewidth=0.75)
        
    albers(hwy).plot(
        ax=ax, color='blue', linewidth=2)

    albers(df).plot(
        ax=ax, color='red', linewidth=2)

def save_and_show(ofn):
    plt.savefig(ofn, dpi=300)
    cmd = ['open','-a','Preview',ofn]
    subprocess.run(cmd)
    
# -------------

def get_city_data(c1,c2):
    fn = 'data/us-cities-top-1k.csv'
    D = dict()
    with open(fn) as fh:
        data = csv.reader(fh)
        for row in data:
            city,state,zip,lat,lon = row
            loc = ', '.join([city,state])
            if loc == c1 or loc == c2:
                lat = round(float(lat),6)
                lon = round(float(lon),6)
                cD = {'lat':lat,
                      'lon':lon}
                D[loc] = cD
    return D

def get_bounds(start,end):
    D = get_city_data(start,end)  
    lat1 = D[start]['lat']
    lat2 = D[end]['lat']
    lon1 = D[start]['lon']
    lon2 = D[end]['lon']
    dx = lon2 - lon1
    dy = lat2 - lat1
    o = geto(dx,dy)
    # filter for latitude if NS, otherwise lon
    north = 0 < o < 45 or 360 - o < 45
    south = abs(180 - o) < 45
    if north or south:
        return (True,lat1,lat2)
    else:
        return (False,lon1,lon2)

def get_ofn(start,end):
    start = start.split(',')[0]
    end = end.split(',')[0]
    return start + '-' + end + '.png'

# -------------

def doOne(start,end,hwy):
    use_lat,v1,v2 = get_bounds(start,end)
    fn = 'data/tl_2019_us_primaryroads.zip'
    hwy = get_highway(hwy,fn)    
    sub = filter_bounds(
        hwy,v1,v2,latitude=use_lat)
    plot(hwy, sub, 'west_coast')
    ofn = get_ofn(start,end)
    save_and_show(ofn)

start = 'Bakersfield, California'
end = 'Eugene, Oregon'
hwy = 'I- 5'
doOne(start,end,hwy)

