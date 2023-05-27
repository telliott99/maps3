import sys
from math import cos, radians, atan, degrees

precision = 4 # for rounding

def fmt(f):  
    # make sure format string matches precision
    format_str = "%." + str(precision) + "f"
    return format_str % round(f,precision)

def point_to_string(p):
    # internally, points are x,y
    # externally, they are LAT,LON
    LON,LAT = [str(v) for v in p]
    return ','.join([LAT,LON])

def string_fmt(segment):
    i,p,q,o,b = segment
    i = str(i)
    p = point_to_string(p)
    q = point_to_string(q)
    o = str(o)
    # leave bounds off for now
    return '\n'.join((i,p,q,o))

# switched order to y,x to have LAT,LON
def preprocess(L):
    rL = list()
    for e in L:
        sL  = e.split('\n')
        # convert selected values to floats
        idx, first, last, orient, bounds = sL
        
        # changed to work with floats
        y1,x1 = first.split(',')
        x1,y1 = float(x1),float(y1)
        
        y2,x2 = last.split(',')
        x2,y2 = float(x2),float(y2)
        
        orient = int(orient)
        b = [float(v) for v in bounds.split(',')]
        bounds = [b[1],b[0],b[3],b[2]]
        
        rL.append([idx, [x1,y1], [x2,y2], orient, bounds])
        
    return rL

# this isn't really correct, but it's close
def dist(p1,p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx < 0:  dx = -dx
    if dy < 0:  dy = -dy
    
    # 1 deg of LAT is 69 miles
    # 1 deg of LON depends on LAT
    # for LAT = 38, cos 38 = 0.788
    
    dy = dy * 69
    #dx = dx * 69 * (cos(radians(p1[1])))
    # for now:
    dx = dx * 69 * 0.788
    
    # miles
    return (dx**2 + dy**2)**0.5

# a surprising variety of 'FULLNAME' 
# even for interstates

# this works for interstates but not some highways
# find all the digits only in the last word w/digits

def get_number(fullname):
    def get_digits(s):
        return [c for c in s if c in '0123456789']
    rL = reversed(fullname.split())
    for s in rL:
        sL = get_digits(s)
        if sL != []:
            return ''.join(sL)
    return 'parse error'

#--------------------------------------

def geto(dx,dy):
    if dx == 0 and dy == 0:
        return 0   # correct solution?
    
    if dx == 0:
        if dy > 0:
            return 0
        else:
            return 180
    if dy == 0:
        if dx > 0:
            return 90
        else:
            return 270
        
    m = dy/dx    
    # sign of m doesn't care *which* of dx,dy is negative
        
    # Q1
    if dx > 0 and dy > 0:
        at = degrees(atan(m))
        return  90 - at

    # Q2, make the slope positive
    # this makes it a mirror image of Q1
    if dx < 0 and dy > 0:
        m *= -1
        at = degrees(atan(m))
        return 270 + at
        
    # Q3
    if dx < 0 and dy < 0:
        at = degrees(atan(m))
        return 270 - at
        
    # Q4, slope is negative, but we work with pos number
    if dx > 0 and dy < 0:
        m *= -1
        at = degrees(atan(m))
        return  90 + at

#-----------------------------

def get_floats(s):
    # coords, each a tuple of x,y
    x,y = s.split(',')
    x,y = float(x),float(y)
    return (x,y)

def close_enough(p1,p2):
    return dist(p1,p2) < 1

def reverse_orientation(o):
    # 0..359
    if 0 <= o < 180:
        return o + 180
    return o - 180

def reverse_segment(segment):
    i,p,q,o,b = segment
    o = reverse_orientation(o)
    if i. endswith('r'): 
        i = i[:-1]
    else:  
        i += 'r'
    return [i,q,p,o,b]

if __name__ == "__main__":
    L = [0,1,2,-1,-2]
    for dx in L:
        for dy in L:
            print('%3d %3d %3.0f' % (dx,dy,geto(dx,dy)))

'''
> p3 stuff.py
  0   0   0
  0   1   0
  0   2   0
  0  -1 180
  0  -2 180
  1   0  90
  1   1  45
  1   2  27
  1  -1 135
  1  -2 153
  2   0  90
  2   1  63
  2   2  45
  2  -1 117
  2  -2 135
 -1   0 270
 -1   1 315
 -1   2 333
 -1  -1 225
 -1  -2 207
 -2   0 270
 -2   1 297
 -2   2 315
 -2  -1 243
 -2  -2 225
> 
'''