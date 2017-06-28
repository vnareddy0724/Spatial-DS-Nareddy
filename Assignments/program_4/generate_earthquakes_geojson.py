
import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'/world_data/earthquakes-1960-2017.json',"r")

data = f.read()

data = json.loads(data)

all_earthquakes = []


#print(type(data))
count=0
range=1
for k,v in data.items():
	count=0
	for i in v:
		earth={}
		earth['type']="Feature"
		earth['properties']=v[count]
		earth['geometry']=earth['properties']['geometry']
		del earth['properties']['geometry']		
		all_earthquakes.append(earth)		
		count=count+1
		range=range+1
		if range == 1001:
			break
	if range == 1001:
		break
	

out = open(DIRPATH+'./geo_json/earthquakes-1960-2017_geo_json.geojson',"w")

out.write(json.dumps(all_earthquakes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()	
	
		
