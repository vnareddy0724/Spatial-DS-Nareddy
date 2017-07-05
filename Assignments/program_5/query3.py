
import json
import os,sys
import pygame
import random 
import math
from pymongo import MongoClient
import pprint as pp
from math import radians, cos, sin, asin, sqrt
from dbscan import *
import operator

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
		
		
		
	def getvolcanos(self):
		closest_volcano=[]
	
		volcano = self.db_volcanos.find( )
		
		for v in volcano:
			closest_volcano.append(v)
			
		return closest_volcano	
		
	def getearthquakes(self):
		closet_eq=[]
	
		quake = self.db_quakes.find({'properties.mag':{'$gt':6.0}})
		
		for v in quake:
			closet_eq.append(v)
			
			
		return closet_eq
		
	def getmeteorites(self):
		closet_met=[]
	
		met = self.db_meteorites.find({'properties.mass':{'$gt':'700'}})
		
		for v in met:
			closet_met.append(v)
			
			
		return closet_met
			
			
	def show_meteorites(self,lis):
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
		
	def show_earthquake(self,lis):
		cords=[]
		for i in lis:
			x=(1024)*(180+i['geometry']['coordinates'][0])/360
			y=(512)*(90-i['geometry']['coordinates'][1])/180
			cords.append((x,y))
			

			
		return cords		
		
		
	def adjust_location_coords(mbr_data,width,height):
		"""
		Adjust your point data to fit in the screen. 
		Expects a dictionary formatted like `mbrs_manhatten_fraud.json` with extremes in it.
		"""
		maxx = float(mbr_data['extremes']['max_x']) # The max coords from bounding rectangles
		minx = float(mbr_data['extremes']['min_x'])
		maxy = float(mbr_data['extremes']['max_y'])
		miny = float(mbr_data['extremes']['min_y'])
		deltax = float(maxx) - float(minx)
		deltay = float(maxy) - float(miny)

		adjusted = {}

		del mbr_data['extremes']

		for id,mbr in mbr_data.items():
			adjusted[id] = []
			for p in mbr:
				x,y = p
				x = float(x)
				y = float(y)
				xprime = (x - minx) / deltax         # val (0,1)
				yprime = 1.0 - ((y - miny) / deltay) # val (0,1)
				adjx = int(xprime*width)
				adjy = int(yprime*height)
				adjusted[id].append((adjx,adjy))
		return adjusted

	
	def calculate_mbrs(self,points, epsilon, min_pts):
		"""
		Find clusters using DBscan and then create a list of bounding rectangles
		to return.
		"""
		mbrs = []
		clusters =  dbscan(points, epsilon, min_pts)
		count=0
		topcluster={}
		finallis=[]
		"""
		Traditional dictionary iteration to populate mbr list
		Does same as below
		"""
		# for id,cpoints in clusters.items():
		#     xs = []
		#     ys = []
		#     for p in cpoints:
		#         xs.append(p[0])
		#         ys.append(p[1])
		#     max_x = max(xs) 
		#     max_y = max(ys)
		#     min_x = min(xs)
		#     min_y = min(ys)
		#     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
		# return mbrs

		"""
		Using list index value to iterate over the clusters dictionary
		Does same as above
		"""
		
		
		for id in range(len(clusters)-1):
			xs = []
			ys = []
			for p in clusters[id]:
				xs.append(p[0])
				ys.append(p[1])
			topcluster[count]=len(xs)
			count=count+1
		
		topcluster=sorted(topcluster.items(), key=operator.itemgetter(1),reverse=True)
		
		
		
		count=0
		
		for i in topcluster:
			finallis.append(i[1])
			count=count+1
			if count == 5 and sys.argv[1] != "meteorites":
				break
			elif count == 7 and sys.argv[1] == "meteorites":
				break
				
		
		pp.pprint(finallis)
		
		for id in range(len(clusters)-1):
			xs = []
			ys = []
			for p in clusters[id]:
				xs.append(p[0])
				ys.append(p[1])
				
			for i in finallis:
				if i == len(xs):				
					max_x = max(xs) 
					max_y = max(ys)
					min_x = min(xs)
					min_y = min(ys)
					mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
					
		return mbrs	
			
		
		
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
	lis=[]
	cords=[]
	lis1=[]
	cords1=[]
	lis2=[]
	cords2=[]
	bg = pygame.image.load(DIRPATH+'./image.png')	
	running=True
	display=False
	mbrs=[]
	while running:
		screen.blit(bg, (0, 0))
		
		if sys.argv[1] == "volcanos":
			epsilon=int(sys.argv[3])
			min_pts=int(sys.argv[2])
		
			lis=mh.getvolcanos()
			cords=mh.show_volcano(lis)
			mbrs = mh.calculate_mbrs(cords, epsilon, min_pts)
			
		elif sys.argv[1] == "earthquakes":	
			epsilon=int(sys.argv[3])
			min_pts=int(sys.argv[2])
		
			lis1=mh.getearthquakes()
			
			cords1=mh.show_earthquake(lis1)
			mbrs = mh.calculate_mbrs(cords1, epsilon, min_pts)
			
		elif sys.argv[1] == "meteorites":	
			epsilon=int(sys.argv[3])
			min_pts=int(sys.argv[2])
		
			lis2=mh.getmeteorites()
			
			cords2=mh.show_meteorites(lis2)
			mbrs = mh.calculate_mbrs(cords2, epsilon, min_pts)
				
			
			
		for i in cords:
			pygame.draw.circle(screen, (255,0,0), (int(i[0]),int(i[1])), 1,0)	
			
		for i in cords1:
			pygame.draw.circle(screen, (0,0,255), (int(i[0]),int(i[1])), 1,0)
			
		for i in cords2:
			pygame.draw.circle(screen, (0,128,0), (int(i[0]),int(i[1])), 1,0)		
			
		for mbr in mbrs:
			pygame.draw.polygon(screen, (255,255,255), mbr, 3)	
			
		
			
			
		pygame.display.flip()	
			
			
			
			
			
			
