import sys
import stuff as ut

target = sys.argv[1]

with open(target,'r') as fh:
    data = fh.read()

L = data.strip().split('\n\n')
L.reverse()

rL = list()
for e in L:
    segment = e.strip().split('\n')
    
    # have to rewrite locally b/c no bounds
    i,p,q,o = segment
    o = ut.reverse_orientation(int(o))
    if i. endswith('r'): 
        i = i[:-1]
    else:  
        i += 'r'
    rev = [i,q,p,str(o)]
    rL.append('\n'.join(rev))
    
result = '\n\n'.join(rL)
print(result)

