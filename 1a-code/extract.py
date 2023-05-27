# rewrite to extract target from shapefile
# w/o first getting all_roads.txt

# focus here on interstates

import sys
import geopandas as gpd
from stuff import fmt, get_number, dist
from stuff import geto

target = sys.argv[1]  # I-5, etc
assert target[0] == 'I'

target = target[2:]

fn = 'data/tl_2019_us_primaryroads.zip'
df = gpd.read_file(fn)
         
def parse(df):
        
    # not the Pandas way, but it works
    # must not have previously removed any rows   
    row_count = df.shape[0]
    rL = list()

    for i in range(row_count):
        item = df.loc[i]
        if not item['RTTYP'] == 'I':
            continue
            
        # some are marked as '(Hov)'
        number = get_number(item['FULLNAME'])
        if number != target:
            continue
            
        # got one
        sL = list()

        g = item['geometry']
        X,Y = g.xy
        
        # these X and Y lists have floats
        X = list(X)
        Y = list(Y)
        
        xmin = fmt(min(X))
        ymin = fmt(min(Y))
        
        xmax = fmt(max(X))
        ymax = fmt(max(Y))
        
        # endpoints
        x1 = X[0]
        y1 = Y[0]
        x2 = X[-1]
        y2 = Y[-1]
        
        orientation = geto(x2-x1,y2-y1)
        seg_length = dist((x1,y1),(x2,y2))
        
        # fmt rounds the values to 'precision' 
        # (4) defined in stuff
        # and converts to string
        
        X = [fmt(x) for x in X]
        Y = [fmt(y) for y in Y]
        XY = [x + ',' + y for x,y in zip(X,Y)]
        sL.append('\n'.join(XY))
        
        sL.append(str(int(orientation))) 
        sL.append(','.join([xmin,ymin,xmax,ymax]))                          
        
        s = '\n'.join(sL)
        rL.append((s,seg_length))  # for sorting
        
    return rL

full_results = parse(df)

full_results = sorted(
    full_results, reverse = True, 
    key = lambda e: e[1])

final = list()
for i,e in enumerate(full_results):
    final.append(str(i) + '\n' + e[0])

ofn = 'I-' + target + '.txt'
with open(ofn,'w') as fh:
    fh.write('\n\n'.join(final))
