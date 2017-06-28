
import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'/world_data/airports.json',"r")

data = f.read()

data = json.loads(data)

all_airports = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''
range = 1

for k,v in data.items():
	gj = collections.OrderedDict()
	gj['type'] = "Feature"
	gj['properties'] = v
	lat = v['lat']
	lon = v['lon']
	del gj['properties']['lat']
	del gj['properties']['lon']
	gj["geometry"] = {}
	gj["geometry"]["type"]="Point"
	gj["geometry"]["coordinates"] = [
		  lon,
		  lat
		]
	all_airports.append(gj)
	range=range + 1
	if range == 1001:
		break

	
#pp.pprint(all_airports)



out = open(DIRPATH+'./geo_json/airports_geo_json.geojson',"w")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()
