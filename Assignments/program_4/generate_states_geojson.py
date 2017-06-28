
import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'./state_borders.json',"r")

data = f.read()

data = json.loads(data)

all_states = []

#print(type(data))

range=1

for i in data:
	state={}
	state['type']="Feature"
	state['properties']=i
	state['geometry']={}
	state['geometry']['type']="Polygon"
	state['geometry']['coordinates']=state['properties']['borders']
	del state['properties']['borders']
	all_states.append(state)
	range=range+1
	if range == 1001:
		break

	
		
	
out = open(DIRPATH+'./geo_json/statesborders_geo_json.geojson',"w")

out.write(json.dumps(all_states, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()	
	
			
