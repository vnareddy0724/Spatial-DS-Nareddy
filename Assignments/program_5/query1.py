
import json
import os,sys
import pygame
import random 
import math
from pymongo import MongoClient
import pprint as pp
from math import radians, cos, sin, asin, sqrt


# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__)) #current wrking directry

class mongoHelper(object):

	def __init__(self):
		self.client = MongoClient()
		self.db_ap = self.client.world_data.airports
		self.db_states = self.client.worlddata.states
		self.db_quakes = self.client.world_data.earthquakes
		self.db_volcanos=self.client.world_data.volcanos
		self.db_meteorites=self.client.world_data.meteorites
		self.checkedairports=[]
		self.visitedairports=[]
		self.name=None
		self.destination=None
		self.d_lon=0
		self.d_lat=0
		self.points=[]
		
	def _haversine(self,lon1, lat1, lon2, lat2):
		"""
		Calculate the great circle distance between two points 
		on the earth (specified in decimal degrees)
		"""
		# convert decimal degrees to radians 
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

		# haversine formula 
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 3956 # Radius of earth in kilometers. Use 6371 for km
		return c * r

	def get_nearest_earthquake(self,lon,lat,r):
		closest_quake=[]
	
		quake = self.db_quakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		
		for ap in quake:
			lon2 = ap['geometry']['coordinates'][0]
			lat2 = ap['geometry']['coordinates'][1]
		
			closest_quake.append(ap)

		return closest_quake


	def get_nearest_volcano(self,lon,lat,r):
	
		closest_volcano=[]
	
		volcano = self.db_volcanos.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		
		for ap in volcano:
			lon2 = ap['geometry']['coordinates'][0]
			lat2 = ap['geometry']['coordinates'][1]
			closest_volcano.append(ap)

		return closest_volcano

	def get_nearest_meteorite(self,lon,lat,r):
	
		
		closest_met=[]
	
		meteo = self.db_meteorites.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		
		for ap in meteo:
			lon2 = ap['geometry']['coordinates'][0]
			lat2 = ap['geometry']['coordinates'][1]
			d = self._haversine(lon,lat,lon2,lat2)
			
			closest_met.append(ap)

		return closest_met
		
		
	def show_quake(self,lis):
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
			

			
		return cords	
		
	def show_volcano(self,lis):
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
			

			
		return cords

	def show_meteorites(self,lis):
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
			

			
		return cords			
		
		
		
		
	def get_nearest_neighbor(self,lon,lat,r,source):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
		print(r)
		print(lon)
		air_res = self.db_ap.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )
		closest_ap=[]
		min = 999999
		level=1
		levellist=[]
		elelist=[]
		elefilter=[]
		desti=[]
		count=0
		
		matched=0
		filteredairports=[]
		
		for ap in air_res:
			if ap['properties']['ap_iata'] != source:
				closest_ap.append(ap)
				
		pp.pprint(len(closest_ap))		
				
		if len(self.checkedairports) == 0:
			for i in closest_ap:
				self.checkedairports.append(i['properties']['ap_iata'])
		
	
		
			
		elif len(self.checkedairports) != 0:
			for i in closest_ap:
				if i['properties']['ap_iata'] in self.checkedairports:
					matched=matched+1
				else:
					self.checkedairports.append(i['properties']['ap_iata'])
					
			
		pp.pprint(self.checkedairports)			
		
		print(matched)
		if matched == len(closest_ap):
			self.get_nearest_neighbor(lon,lat,(r+500),source)
			
			
		else:	
				
			min = 9999999
			
			for ap in closest_ap:
				d=self._haversine(ap['geometry']['coordinates'][0],ap['geometry']['coordinates'][1],self.d_lon,self.d_lat)
				if d < min:
					min=d
					self.name=ap['properties']['ap_iata']
					print(d)
			self.visitedairports.append(self.name)


		return self.name
			
		'''	
		
			
		for i in closest_ap:
			if i['properties']['ap_iata'] == "MNL":
				desti.append(i)
				return desti
			
		if len(closest_ap) <= 1:
			return closest_ap
			
		for i in closest_ap:
			levellist.append(int(i['properties']['ap_level']))
			
		x = 100
		for i in levellist:
			if i < x:
				x = i
			
		print(x)	

		for i in closest_ap:
			print(i['properties']['ap_level'])
			if int(i['properties']['ap_level']) == x:
				print("hello")
				filteredairports.append(i)
			
		return filteredairports	
				
		if len(filteredairports) > 1:
			for i in filteredairports:
				elelist.append(int(i['properties']['elevation']))
			y = 100
			for i in elelist:
				if i < y:
					y = i
			print(y)
			
			for i in filteredairports:
				if int(i['properties']['elevation']) == y:
					elefilter.append(i)
					
			return elefilter	
			
		'''
		
	def get_aircords(self,code):
		air_cords=self.db_ap.find({"properties.ap_iata":code})
		cords=[]
		for i in air_cords:
			cords.append((i['geometry']['coordinates'][0],i['geometry']['coordinates'][1]))
			
		return cords	
			
	def addtolist(self,code):
		air_cords=self.db_ap.find({"properties.ap_iata":code})
		
		cords=[]
		for i in air_cords:
			cords.append((i['geometry']['coordinates'][0],i['geometry']['coordinates'][1]))
			
		for i in cords:
			x=(1024)*(180+i[0])/360
			y=(512)*(90-i[1])/180
			self.points.append((x,y))
			
		
		
		
if __name__ == '__main__':

	mh=mongoHelper()
	background_colour = (255,255,255)
	black = (0,0,0)
	(width, height) = (1024, 512)
	radius=500
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('MBRs')
	screen.fill(background_colour)
	pygame.init()
	bg = pygame.image.load(DIRPATH+'./image.png')	
	running=True
	display=False
	count=0
	run=True
	features=[]
	features1=[]
	features2=[]
	features3=[]
	
	#d=mh._haversine(-142.71800231934,46.888698577881,-117.900138,33.626395)
	#print(d)
	#exit(1)
	
	while running:
		drawlist=[]
		draw=[]
		screen.blit(bg, (0, 0))
	
		source=sys.argv[1]
		mh.destination=sys.argv[2]
		dest_cords=mh.get_aircords(mh.destination)
		for i in dest_cords:
			mh.d_lon=i[0]
			mh.d_lat=i[1]
		while(run):
			lis=[]
			lis=mh.get_aircords(source)
			for i in lis:
				source=mh.get_nearest_neighbor(i[0],i[1],radius,source)
				count=count+1
				print(source)
				print(mh.destination)
			if source == mh.destination:	
				run=False
			
		for i in mh.visitedairports:
			mh.addtolist(i)
		
		for i in mh.points:
			pygame.draw.circle(screen, (255,255,255), (int(i[0]),int(i[1])), 3,0)	
			
			
		for i in mh.points:
			lon1= (i[0]*360)/1024
			lon1=lon1-180
			lat1=(i[1]*180)/512  
			lat1=90-lat1
			features=mh.get_nearest_earthquake(lon1,lat1,radius)
			cords=mh.show_quake(features)
			for j in cords:
				features1.append(j)
			features=mh.get_nearest_volcano(lon1,lat1,radius)
			cords=mh.show_volcano(features)
			for j in cords:
				features2.append(j)	
			features=mh.get_nearest_meteorite(lon1,lat1,radius)
			cords=mh.show_meteorites(features)
			for j in cords:
				features3.append(j)
		
		for i in mh.points:
			drawlist.append(i[0])
			draw.append(i[0])
			
			
		for i in features1:
			pygame.draw.circle(screen, (0,0,255), (int(i[0]),int(i[1])), 1,0)	
			
		for i in features2:
			pygame.draw.circle(screen, (255,0,0), (int(i[0]),int(i[1])), 1,0)	

		for i in features3:
			pygame.draw.circle(screen, (0,128,0), (int(i[0]),int(i[1])), 1,0)			
			
		
		x=min(drawlist)
		
		drawlist=[]
		draw=[]
		match=0
		
		if x < width/2:
			for i in mh.points:
				if i[0] == x:
					drawlist.append(i)
					match=1
					
				elif match == 1:
					draw.append(i)
					
				else:
					drawlist.append(i)
					
		
				
		if x < width/2:
			pygame.draw.lines(screen, (255,255,255),False, drawlist, 3)	
			pygame.draw.lines(screen, (255,255,255),False, draw, 3)
			
		else:
			pygame.draw.lines(screen, (255,255,255),False, mh.points, 3)
			
		
		del mh.points[:]
		
		#pygame.draw.lines(screen, (255,0,0),False, draw, 1)
		
		pygame.display.flip()
