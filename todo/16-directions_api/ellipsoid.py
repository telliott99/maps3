import sys
from math import pi, sin, cos, log

def rad(d):  return (d/360.0) * 2 * pi

# format: lat,lon
def project(t,v=False):
    p0,l0 = t
    a = 6378206.4  # m
    e = 0.0822719
    e_sq = 0.00676866
    
    # standard calcs
    P0 = rad(p0)   
    L0 = rad(l0)

    # reference latitudes
    p1,p2 = 29.5, 45.5
    if v:  print('p1: %.1f' % p1)
    if v:  print('p2: %.1f' % p2)
    P1,P2 = rad(p1),rad(p2)
        
    S1 = sin(P1)
    S2 = sin(P2)
    C1 = cos(P1)
    C2 = cos(P2)
            
    # ------
    
    def get_q(p):
        P = rad(p)
        SP = sin(P)
        f = e * SP
                
        g1 = 1 - e_sq
        g2 = SP/(1-f**2)
        g3 = 1.0/(2*e)
        g4 = log((1 - f)/(1 + f))
        return g1 * (g2 - (g3 * g4))
    
    q0 = get_q(p0)
    q1 = get_q(p1)
    q2 = get_q(p2)
    
    if v:  print('q0: %.7f' % q0)
    if v:  print('q1: %.7f' % q1)
    if v:  print('q2: %.7f' % q2)
    
    def get_m(p):
        P = rad(p)
        SP = sin(P)
        f = (1 - e_sq * SP**2)**0.5
        return cos(P)/f
    
    m1 = get_m(p1)
    m2 = get_m(p2)
    
    if v:  print('m1: %.7f' % m1)
    if v:  print('m2: %.7f' % m2)

    n = (m1**2 - m2**2)/(q2 - q1)
    if v:  print('n:  %.7f' % n)
        
    C = m1**2 + n * q1
    if v:  print('C:  %.7f' % C)
    
    def rho(q):
        part = (C - (n * q))**0.5
        return a * part / n
         
    R0 = rho(q0)
    if v:  print('R0: %.1f' % R0)
    
    # specific calcs
    def f(t):
        p,l = t
        P = rad(p)
        q = get_q(p)
        if v:  print('q:  %.7f' % q)
        
        R = rho(q)
        if v:  print('R:  %.1f' % R)
        
        theta = n * (l - l0)
        if v:  print('t:  %.7f' % theta)
        T = rad(theta)
        
        x = R * sin(T)
        y = R0 - R * cos(T)
        return (x,y)
    return f

def test1():
    print('test1')
    p0 = 23
    l0 = -96
    print('p0: %.1f' % p0)
    print('l0: %.1f' % l0)
    
    g = project((p0,l0))
    
    p = 35
    l = -75
    print('p:  %.1f' % p)
    print('l:  %.1f' % l)

    x,y = g((p,l))
    
    print('x:  %.1f' % x)
    print('y:  %.1f' % y)

if __name__ == "__main__":
    test1()
    
    