
import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'./countries.geo.json',"r")

data = f.read()

data = json.loads(data)

all_country = []

range=1

del data [999: len(data)-1]
	

	
out = open(DIRPATH+'./geo_json/countries_geo_json.geojson',"w")

out.write(json.dumps(data, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()	
		
