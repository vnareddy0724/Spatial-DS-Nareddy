
import pygame
import sys,os
import json
from dbscan import *

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)
def calculate_mbrs(points, epsilon, min_pts,debug=False):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = {}
    clusters =  dbscan(points, epsilon, min_pts,distance=euclidean,debug=debug)
    extremes = {'max_x':sys.maxint * -1,'max_y':sys.maxint*-1,'min_x':sys.maxint,'min_y':sys.maxint}

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    for id,cpoints in clusters.items():
        print(id)
        xs = []
        ys = []
        for p in cpoints:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        if max_x > extremes['max_x']:
            extremes['max_x'] = max_x
        if max_y > extremes['max_y']:
            extremes['max_y'] = max_y
        if min_x < extremes['min_x']:
            extremes['min_x'] = min_x
        if min_y < extremes['min_y']:
            extremes['min_y'] = min_y

        mbrs[id]=[(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)]
    mbrs['extremes'] = extremes
    return mbrs
if __name__=='__main__':

	background_colour = (255,255,255)
	black = (0,0,0)
	(width, height) = (1024, 512)

	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('MBRs')
	screen.fill(background_colour)
	pygame.init()
	bg = pygame.image.load("./image.png")

	# Put this in your game loop:
	screen.blit(bg, (0, 0))
	count=1960
	years = [x for x in range(1960,2017)]
	pygame.display.flip()
	values=[]
	running = True
	xlist=[]
	ylist=[]
	'''
	for i in years:
		f = open('./quake-'+str(count)+'-adjusted.json','r')
		points = json.loads(f.read())
		print(type(points))
		for j in points:
			for val in j:
				values.append(j)		
		count=count+1
		f.close()
	print(values)	
	exit(1)
	for i in values:
		xlist.append(i[0])
		ylist.append(i[1])
	maxx=max(xlist)
	maxy=max(ylist)
	minx=min(xlist)
	miny=min(ylist)
	print(maxx)
	print(maxy)
	print(minx)
	print(miny)
	
	exit(1)
	'''
	while running:
		if count == 2017:
			count=1960
			points=[]
			values=[]
		screen.blit(bg, (0, 0))
		f = open('quake-'+str(count)+'-adjusted.json','r')
		points = json.loads(f.read())
		for j in points:
			values.append((j[0],j[1]))
		count=count+1
		f.close()
		
		for p in values:
			pygame.draw.circle(screen, (255,255,0), p, 1,0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				clean_area(screen,(0,0),width,height,(255,255,255))
		
	
		pygame.display.flip()
		pygame.time.wait(10)	
		
