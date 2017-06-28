
import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'./world_volcanos.json',"r")

data = f.read()

data = json.loads(data)

all_volcanos = []


#pp.pprint(data)

#print(type(data))

range=1

for i in data:
	vol={}
	vol['type']="Feature"
	vol['properties']=i
	if len(i['Lat']) == 0:
		pass
	else:	
		lat = float(i['Lat'])
		lon = float(i['Lon'])
	del vol['properties']['Lat']
	del vol['properties']['Lon']
	vol["geometry"] = {}
	vol["geometry"]["type"]="Point"
	vol["geometry"]["coordinates"] = [
		  (lon),
		  (lat)
		]
	all_volcanos.append(vol)
	range=range+1
	if range == 1001:
		break



out = open(DIRPATH+'./geo_json/volcanos_geo_json.geojson',"w")

out.write(json.dumps(all_volcanos, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()	
	
	
	
	
	
