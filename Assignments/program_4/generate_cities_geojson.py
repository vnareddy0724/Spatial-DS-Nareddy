
import pprint as pp
import os,sys
import json
import collections
DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'./world_cities_large.json',"r")

data = f.read()

data = json.loads(data)

all_cities = []
count=0
range=1
for k,v in data.items():
	count=0
	for i in v:
		city={}
		city['type']="Feature"
		city['properties']=v[count]	
		lat=float(city['properties']['lat'])
		lon=float(city['properties']['lon'])
		del city['properties']['lat']
		del city['properties']['lon']
		city['geometry']={}
		city['geometry']['type']="Point"
		city['geometry']['coordinates']=[lon,lat]
		
		count=count+1
		
		all_cities.append(city)
		range=range+1
		if range == 1001:
			break
		
	if range == 1001:
		break
	
out = open(DIRPATH+'./geo_json/world_large_cities_geo_json.geojson',"w")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()		
		
