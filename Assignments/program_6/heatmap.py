
"""
Program:
--------
    Program 6 - Heat map implementation

Description:
------------
    This program generates heat map based on terrorism attacks.
    
Name: Vahini Nareddy
Date: 07 July 2017
"""

import pprint as pp
import os,sys
import json
import collections
import pygame
import random 
import math

#Opens source file

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH+'/files/attacks.json',"r")

data = f.read()

#loads the json file data

data = json.loads(data)

all_attacks = []

#pp.pprint(data)

citycount={}


#Storing coordinates and attacks count into dictionary

for k,v in data.items():
	for k1,v1 in v.items():
				
		if k1 not in citycount:
			citycount[k1]={}
			citycount[k1]['count']=(v1['count'])
			citycount[k1]['geometry']=v1['geometry']['coordinates']
			
		elif k1 in citycount:
			for k2,v2 in citycount.items():
				if k1 == k2:
					citycount[k1]['count']=v2['count']+v1['count']
		

checked=[]
#pp.pprint(citycount)

grid=[]
height=512
width=1024

#Creating grid based on screen size

for i in range(height):
	grid.append([0 for x in range(width)])

	
#Converting lon and lats to x,y coordinates	
		
for k,v in citycount.items():
	
	x=int((1024)*(180+v['geometry'][0])/360)
	y=int((512)*(90-v['geometry'][1])/180)
	
	grid[y][x]=v['count']



max=grid[0][0]
radiuscount={}
radius=0
row=0
col=0
steps=0
cords=[]
values=[]
maxcoordinates=[]

#Storing values into grid based on city coordinates

for i in range(height):
	col=0
	for x in range(width):
		if grid[row][col] != 0:
			steps=steps+1
			value=grid[row][col]
			#radiuscount[value]=value
			cords.append((row,col))
			values.append(value)
			if max < value:
				max=value
				maxcoordinates=(row,col)
		col=col+1	
		
		
	row=row+1
	
	
print(max)

min=1

EPSILON = sys.float_info.epsilon  # smallest possible difference

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))
		
		
minval, maxval = min, max
colordetect={}
radius=1
delta = float(maxval-minval) / steps
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
#print('  Val       R    B    G')

for i in range(steps+1):
	val = minval + i*delta
	r, g, b = convert_to_rgb(minval, maxval, val, colors)
	#print('{:.3f} -> ({:3d}, {:3d}, {:3d})'.format(val, r, g, b))	
	
	colordetect[int(val)]=(r,g,b)
	
colordetect[999]=(255,0,0)

#Setting radius of points based on occurances of attacks

for i in values:
	if i not in radiuscount:
		if i <= 35:
			radiuscount[i]=1
			
		elif i > 35 and i <= 93:
			radiuscount[i]=8	
			
		elif i > 93 and i <= 979:
			radiuscount[i]=15
			
		
			
#Pygame display			


background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)
radius=500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('attacks')
screen.fill(background_colour)
pygame.init()
row=0
col=0
bg = pygame.image.load(DIRPATH+'./image.png')	
running=True
while running:
	row=0
	col=0
	screen.blit(bg, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False		
		
	for i in range(height):
		col=0
		for x in range(width):
			if grid[row][col] != 0:	
				if grid[row][col] == max:
					color=colordetect[grid[row][col]]					
					pygame.draw.circle(screen, color, (col,row), 40,5)	
					continue
				
				color=colordetect[grid[row][col]]
				radius=radiuscount[grid[row][col]]
				if radius == 1:
					pygame.draw.circle(screen, color, (col,row),radius,0)
				elif radius == 8:
					pygame.draw.circle(screen, color, (col,row),radius,2)
				else:
					pygame.draw.circle(screen, color, (col,row),radius,3)
				
			col=col+1
		row=row+1		

	pygame.image.save(screen , "attacks.png")	
		
	pygame.display.flip()
			
						
