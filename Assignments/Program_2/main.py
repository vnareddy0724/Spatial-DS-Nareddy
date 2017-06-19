
"""
Program:
--------
    Program 2 - DrawCrime

Description:
------------
    This program plots points of crime data of NYC based on coordinatres.
Name: Vahini Nareddy
Date: 06 19 2017
"""
 
import pygame
import random
from dbscan import *
import sys,os
import pprint as pp


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

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
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs


def clean_area(screen,origin,width,height,color):
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1000, 1000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

epsilon = 20
min_pts = 5

#lists to store all files data

keys1 = []
crimes1= []
keys2=[]
keys3=[]
keys4=[]
keys5=[]
crimes2=[]
crimes3=[]
crimes4=[]
crimes5=[]
#Source Path

DIRPATH = os.path.dirname(os.path.realpath(__file__))
got_keys = False

#with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:

#Opens files and store required data into lits.

with open(DIRPATH+'/filtered_crimes_manhattan.csv') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys1 = line
            print(keys1)
            got_keys = True
            continue
        crimes1.append(line)
got_keys = False		

with open(DIRPATH+'/filtered_crimes_queens.csv') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys2 = line
            print(keys2)
            got_keys = True
            continue
        crimes2.append(line)		
got_keys = False	
	
with open(DIRPATH+'/filtered_crimes_staten_island.csv') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys3 = line
            print(keys3)
            got_keys = True
            continue
        crimes3.append(line)		
got_keys = False

with open(DIRPATH+'/filtered_crimes_bronx.csv') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys4 = line
            print(keys4)
            got_keys = True
            continue
        crimes4.append(line)	
got_keys = False

with open(DIRPATH+'/filtered_crimes_brooklyn.csv') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys5 = line
            print(keys5)
            got_keys = True
            continue
        crimes5.append(line)		
		
#Lists to store feature scaling data
		
crimecoords1 = []		
crimecoords2 = []		
crimecoords3 = []		
crimecoords4 = []		
crimecoords5 = []		
points1 = []
points2 = []
points3 = []
points4 = []
points5 = []
names = []	


	
for crime in crimes1:
	#crimecoords.append((crime[19],crime[20]))	
	if len(crime) == 24 and len(crime[19]) != 0 and len(crime[20]) != 0:
		crimecoords1.append((int(crime[19]),int(crime[20])))
		names.append(crime[9])
	else:
		continue
for crime in crimes2:
	#crimecoords.append((crime[19],crime[20]))	
	if len(crime) == 24 and len(crime[19]) != 0 and len(crime[20]) != 0:
		crimecoords2.append((int(crime[19]),int(crime[20])))
		names.append(crime[9])
	else:
		continue			
for crime in crimes3:
	#crimecoords.append((crime[19],crime[20]))	
	if len(crime) == 24 and len(crime[19]) != 0 and len(crime[20]) != 0:
		crimecoords3.append((int(crime[19]),int(crime[20])))
		names.append(crime[9])
	else:
		continue	
for crime in crimes4:
	#crimecoords.append((crime[19],crime[20]))	
	
	if len(crime) == 24 and len(crime[19]) != 0 and len(crime[20]) != 0:
		crimecoords4.append((int(crime[19]),int(crime[20])))
		names.append(crime[9])
	else:
		continue	
for crime in crimes5:
	#crimecoords.append((crime[19],crime[20]))	
	if len(crime) == 24 and len(crime[19]) != 0 and len(crime[20]) != 0:
		crimecoords5.append((int(crime[19]),int(crime[20])))
		names.append(crime[9])
	else:
		continue		
#crimecoords = map(int, crimecoords)
		

		
#Applying scaling formula based on screen width and height.
		
num_points = 500

maxvaluex=1067226
maxvaluey=271820
minvaluex=913357
minvaluey=121250
xlist=[]
ylist=[]

#converts all the coordinates using feature scaling formula based on the size of the screen

for i in crimecoords1:
	x = i[0]
	y = i[1]
	
	x1= (x-minvaluex)/(maxvaluex-minvaluex)
	y1=(y-minvaluey)/(maxvaluey-minvaluey)
	
	points1.append(((x1*width),((1-y1)*height)))
	


for i in crimecoords2:
	x = i[0]
	y = i[1]
	
	x1= (x-minvaluex)/(maxvaluex-minvaluex)
	y1=(y-minvaluey)/(maxvaluey-minvaluey)
	
	points2.append(((x1*width),((1-y1)*height)))
	

for i in crimecoords3:
	x = i[0]
	y = i[1]
	
	x1= (x-minvaluex)/(maxvaluex-minvaluex)
	y1=(y-minvaluey)/(maxvaluey-minvaluey)
	
	points3.append(((x1*width),((1-y1)*height)))

for i in crimecoords4:
	x = i[0]
	y = i[1]
	
	x1= (x-minvaluex)/(maxvaluex-minvaluex)
	y1=(y-minvaluey)/(maxvaluey-minvaluey)
	
	points4.append(((x1*width),((1-y1)*height)))
for i in crimecoords5:
	x = i[0]
	y = i[1]
	
	x1= (x-minvaluex)/(maxvaluex-minvaluex)
	y1=(y-minvaluey)/(maxvaluey-minvaluey)
	
	points5.append(((x1*width),((1-y1)*height)))
	



#mbrs = calculate_mbrs(points1, epsilon, min_pts)

running = True
count=0

while running:
	pygame.init() 
	myfont = pygame.font.SysFont("Ariel", 30)
	label = myfont.render("Program2", 1, (0,0,255))
	screen.blit(label, (0, 0))
	myfont = pygame.font.SysFont("Ariel", 30)
	label = myfont.render("Vahini Nareddy", 1, (0,0,255))
	screen.blit(label, (0, 25))
	for p in points1:
		pygame.draw.circle(screen,(194,35,38), (int(p[0]),int(p[1])), 1, 0)
	for p in points3:
		pygame.draw.circle(screen, (253,182,50), (int(p[0]),int(p[1])), 1, 0)
	for p in points2:
		pygame.draw.circle(screen, (243,115,56), (int(p[0]),int(p[1])), 1, 0)
	for p in points4:
		pygame.draw.circle(screen, (2,120,120), (int(p[0]),int(p[1])), 1, 0)	
	for p in points5:
		pygame.draw.circle(screen, (128,22,56), (int(p[0]),int(p[1])), 1, 0)	
	
	pygame.image.save(screen , "image.png")	
	'''
	for mbr in mbrs:
		pygame.draw.polygon(screen, black, mbr, 2)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clean_area(screen,(0,0),width,height,(255,255,255))
			points1.append(event.pos)
			mbrs = calculate_mbrs(points, epsilon, min_pts)
	'''		
	pygame.display.flip()

