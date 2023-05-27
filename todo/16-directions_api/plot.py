import sys, os, json
import plotly.graph_objects as go
from ellipsoid import project

fn = sys.argv[1]
with open(fn,'r') as fh:
    route = json.load(fh)
    
p0 = 23
l0 = -96
print('p0: %.1f' % p0)
print('l0: %.1f' % l0)
f = project((p0,l0))

multi = route["features"][0]
vL = multi['geometry']['coordinates'][0]
# vL = [f(t) for t in vL]

X = [t[0] for t in vL]
Y = [t[1] for t in vL]

poly = go.Scatter(
    x=X,y=Y,
    line={'color':'blue', 'width':3},
    #marker={'size':10, 'color':'blue'},
    mode='lines')
        
fig = go.Figure()
fig.add_trace(poly)
    
fig.update_layout(
    width = 500,
    height = 500,
    yaxis = dict(
      scaleanchor = "x",
      scaleratio = 1.2,
    )
)

fig.show()
