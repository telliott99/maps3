# takes a target that's already been extracted

# python3 endpoints.py target > target-ends.txt

import sys
target = sys.argv[1]

fn = target + '.txt'

with open(fn) as fh:
    data = fh.read().strip().split('\n\n')
    
def switch(p):
    x,y = p.split(',')
    return ','.join((y,x)) 
    
# -------

pL = list()

for e in data:
    feature = e.strip().split('\n')
    
    i,first = feature[:2]
    last,o,b = feature[-3:]
    
    # display LAT, LON
    first = switch(first)
    last = switch(last)        
    sL = [i,first,last,o]
    
    p,q,r,s = b.split(',')
    b = ','.join((q,p,s,r))
    sL.append(b)
        
    pL.append('\n'.join(sL))

with open (target + '-ends.txt', 'w') as fh:
    fh.write('\n\n'.join(pL))

    