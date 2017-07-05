
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
		self.p=[]
		self.p1=[]
		self.p2=[]
		self.p3=[]
		self.p4=[]
		self.p5=[]
		self.p6=[]
		
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
		
	def get_nearest_neighbor(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
		air_res = self.db_ap.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		for ap in air_res:
			lon2 = ap['geometry']['coordinates'][0]
			lat2 = ap['geometry']['coordinates'][1]
			d = self._haversine(lon,lat,lon2,lat2)
			closest_ap .append(ap)

		return closest_ap
		
	def get_nearest_earthquake(self,lon,lat,r):
		closest_quake=[]
	
		quake = self.db_quakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		
		for ap in quake:
			lon2 = ap['geometry']['coordinates'][0]
			lat2 = ap['geometry']['coordinates'][1]
		
			closest_quake.append(ap)

		return closest_quake
		
		
	def get_given_earthquake(self,field,fieldvalue,minmax,result,lon,lat,r):
		closest_quake=[]
	
		quake = self.db_quakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		for ap in quake:
			if ap:
				if len(closest_quake) < int(result) and int(result) != 0:
					if minmax == "min":
						if float(ap['properties']['mag']) >= float(fieldvalue):
						
							closest_quake.append(ap)	
					elif minmax == "max":
						if float(ap['properties']['mag']) <= float(fieldvalue):
						
							closest_quake.append(ap)
							
				elif int(result) == 0:
					if minmax == "min":
						if float(ap['properties']['mag']) >= float(fieldvalue):
						
							closest_quake.append(ap)	
					elif minmax == "max":
						if float(ap['properties']['mag']) <= float(fieldvalue):
						
							closest_quake.append(ap)
			
				
			
		return closest_quake
		
		
	def get_given_volcano(self,field,fieldvalue,minmax,result,lon,lat,r):
		closest_volcano=[]
	
		volcano = self.db_volcanos.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		for ap in volcano:
			if ap:
				if len(closest_volcano) < int(result) and int(result) != 0:
					if minmax == "min":
						if len(ap['properties']['Altitude']) != 0 and int(ap['properties']['Altitude']) >= int(fieldvalue):
						
							closest_volcano.append(ap)	
					elif minmax == "max":
						if len(ap['properties']['Altitude']) != 0 and int(ap['properties']['Altitude']) <= int(fieldvalue):
						
							closest_volcano.append(ap)
							
				elif int(result) == 0:
					if minmax == "min":
						if len(ap['properties']['Altitude']) != 0 and int(ap['properties']['Altitude']) >= int(fieldvalue):
						
							closest_volcano.append(ap)	
					elif minmax == "max":
						if len(ap['properties']['Altitude']) != 0 and int(ap['properties']['Altitude']) <= int(fieldvalue):
						
							closest_volcano.append(ap)
			
				
		
		return closest_volcano	
		
		
	def get_given_meteorites(self,field,fieldvalue,minmax,result,lon,lat,r):
		closest_met=[]
	
		meteo = self.db_meteorites.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(r) / 3963.2 ] } }} )

		min = 999999
		
		for ap in meteo:
			if ap:
				if len(closest_met) < int(result) and int(result) != 0:
					if minmax == "min":
						if len(ap['properties']['mass']) != 0 and float(ap['properties']['mass']) >= float(fieldvalue):
						
							closest_met.append(ap)	
					elif minmax == "max":
						if len(ap['properties']['mass']) != 0 and float(ap['properties']['mass']) <= float(fieldvalue):
						
							closest_met.append(ap)
							
				elif int(result) == 0:
					if minmax == "min":
						if len(ap['properties']['mass']) != 0 and float(ap['properties']['mass']) >= float(fieldvalue):
						
							closest_met.append(ap)	
					elif minmax == "max":
						if len(ap['properties']['mass']) != 0 and float(ap['properties']['mass']) <= float(fieldvalue):
						
							closest_met.append(ap)
			
				
			
		return closest_met
	
		
		
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
		
	def clean_area(self,screen,origin,width,height,color):
		ox,oy = origin
		points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
		pygame.draw.polygon(screen, color, points, 0)	
			
   
	def showFeatures_air(self,lis):	
		cords=[]
		for k,v in lis.items():
			if k == "geometry":			
				air_x = (1024) * (180 + v['coordinates'][0]) / 360
				air_y = (512) * (90 - v['coordinates'][1]) / 180
				cords.append((air_x,air_y))
				
			
		return cords
		
	def showFeatures_quake(self,lis):	
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
			

			
		return cords	
		
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
		
		
	def showFeatures_volcano(self,lis):	
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
			
		return cords	
			
	def showFeatures_meteorite(self,lis):	
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
		return cords			
		
if __name__ == '__main__':

	mh=mongoHelper()
	background_colour = (255,255,255)
	black = (0,0,0)
	(width, height) = (1024, 512)

	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('MBRs')
	screen.fill(background_colour)
	pygame.init()
	bg = pygame.image.load(DIRPATH+'./image.png')	
	running=True
	display=False
	print(type(sys.argv))
	
	while running:
		screen.blit(bg, (0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False			
			if event.type == pygame.MOUSEBUTTONDOWN:
				mh.clean_area(screen,(0,0),width,height,(255,255,255))
				print(event.pos)
				pos=event.pos				
				lon= (pos[0]*360)/1024
				lon=lon-180
				lat=(pos[1]*180)/512  
				lat=90-lat
				print(lat)
				print(lon)
				
				if len(sys.argv) == 2:
					radius=sys.argv[1]	
					print(radius)
					lis1=mh.get_nearest_earthquake(lon,lat,radius)
					lis2=mh.get_nearest_volcano(lon,lat,radius)
					lis3=mh.get_nearest_meteorite(lon,lat,radius)
					mh.p1=mh.showFeatures_quake(lis1)
					mh.p2=mh.showFeatures_volcano(lis2)
					mh.p3=mh.showFeatures_meteorite(lis3)
					print(len(lis1))
					print(len(lis2))
					print(len(lis3))
				if len(sys.argv) == 7:
					feature=sys.argv[1]
					field=sys.argv[2]
					fieldvalue=sys.argv[3]
					minmax=sys.argv[4]                  #self,field,fieldvalue,minmax,result,lon,lat,r
					maxresults=sys.argv[5]
					radius=sys.argv[6]
					if feature == "earthquakes":
						lis4=mh.get_given_earthquake(field,fieldvalue,minmax,maxresults,lon,lat,radius)
						mh.p4=mh.show_quake(lis4)
						print(len(lis4))
					elif feature == "volcanos":
						lis5=mh.get_given_volcano(field,fieldvalue,minmax,maxresults,lon,lat,radius)
						mh.p5=mh.show_volcano(lis5)
					
						print(len(lis5))
						
						
					elif feature == "meteorites":
						lis6=mh.get_given_meteorites(field,fieldvalue,minmax,maxresults,lon,lat,radius)
						mh.p6=mh.show_meteorites(lis6)
					
				
				
		for i in mh.p1:
			x=int(i[0])
			y=int(i[1])
			pygame.draw.circle(screen, (0,0,255), (x,y), 1,0)	
		for i in mh.p2:
			x=int(i[0])
			y=int(i[1])
			pygame.draw.circle(screen, (255,0,0), (x,y), 1,0)	
		for i in mh.p3:
			x=int(i[0])
			y=int(i[1])
			pygame.draw.circle(screen, (0,128,0), (x,y), 1,0)	
		for i in mh.p4:
			x=int(i[0])
			y=int(i[1])
			pygame.draw.circle(screen, (0,0,255), (x,y), 1,0)	
		for i in mh.p5:
			x=int(i[0])
			y=int(i[1])
			pygame.draw.circle(screen, (255,0,0), (x,y), 1,0)	
		for i in mh.p6:
			x=int(i[0])
			y=int(i[1])
			pygame.draw.circle(screen, (0,128,0), (x,y), 1,0)			
		pygame.display.flip()
