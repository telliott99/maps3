import sys
import stuff as utils

target = sys.argv[1]
# the number of the first segment to use

D = { 'I-5':'4r',
      'I-10':'110r' }
      
try:
    first = sys.argv[2]
except:
    first = D[target]

with open(target + '-ends.txt') as fh:
    short_segments = fh.read().strip().split('\n\n')
    
# alter sys.path to add our utils

# ----------------------------

# each item or segment will be [index, p1, p2]
short_segments = utils.preprocess(short_segments)

# locate the first segment based on CL arg first
# results saved in this list
route = list()

# segments in L don't have 'r' yet
# and are not yet oriented along the route
# by using 'r' here
# we are saying, use segment xxx but in reverse order

# new logic:  save all good points to a list
all_points = list()

rev = first.endswith('r')

if rev:
    j = first[:-1]
else:
    j = first

for segment in short_segments:
    i,p,q,o,b = segment
    if i == j:
        if rev:
            segment = utils.reverse_segment(segment) 
        route.append(segment)
        break
    
# ----------------------------
    
# extension phase

def search():
    # previous segment guaranteed in fwd order
    prev = route[-1]
    i,s,t,n,a = prev

    seen_before = [e[0] for e in route]
        
    # we search from largest to smallest
    # so return the first match
    for segment in short_segments:
        j,p,q,o,b = segment
        
        # this should eliminate prev
        if j in seen_before:
            continue
        elif j + 'r' in seen_before:
            continue
                      
        # so the points we are thinking about are
        # in the candidate segment:  p and q
        # I like this better than p1 and p2
        
        # and in the prev accepted segment s and t
        # t is the same as prev[2]
        # t for target, s as the letter before t
        
        # test for close matches
        t_eq_p = p == t or utils.close_enough(p,t)
        t_eq_q = q == t or utils.close_enough(q,t)

       # neither of the points is a close match
        if not (t_eq_p or t_eq_q):
            continue
                        
        # if this is precisely the same segment, skip
        # i should already be in seen_before
        # so we should not get here
        if prev == segment:
            seen_before.append(j)
            continue
                
        # or reversed
        if s == q and t == p:
            seen_before.append(j)
            continue

        # perhaps just a real close match
        if t_eq_q and utils.close_enough(p,s):
            seen_before.append(j)
            continue
            
        # close match but exactly reversed
        if t_eq_p and utils.close_enough(q,s):
            seen_before.append(j)
            continue
                                
        # Looks like we found an extension:
        if t_eq_q:
            # reverse before saving
            segment = utils.reverse_segment(segment)  
                      
        route.append(segment)
        seen_before.append(j)
        return

    return 'stop search'
            
def get_next():
    result_code = search()
    return result_code
    
# -------------------------------

# we want to terminate gracefully when things go awry

counter = 0
while True:
    result_code = get_next()
    if result_code == 'stop search':
        break
    
    counter += 1
    if counter > 150:
        print('runaway process')
        break

pL = [utils.string_fmt(item) for item in route]
print('\n\n'.join(pL))