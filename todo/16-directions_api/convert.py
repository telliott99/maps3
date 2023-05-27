import json
import polyline

with open('results.json') as fh:
    data = json.load(fh)

r = data["routes"][0]
points = r['overview_polyline']['points']

s='''
{"type":"FeatureCollection",
 "features": [
    {
      "type":"Feature",
      "properties":{"name":"LA-SF"},
      "geometry": {"type":"MultiLineString",
                   "coordinates":[[
'''
print(s)

p = polyline.decode(points, geojson=True)
for lon,lat in p[:-1]:
   print('[%.8f, %.8f],' % (lon,lat))
print('[%.8f, %.8f]' % p[-1])

s = '''
         ]]
      }
    }
  ]
}
'''
print(s)
