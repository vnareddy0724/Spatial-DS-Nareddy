
/**
* @ProgramName: Program-1
* @Author: Vahini Nareddy 
* @Description: 
*     This program highlights the country border and rectangle around the country in which user clicks and also prints the respective country name on the screen.
* @Course: 4553 Spatial DataStructure
* @Semester: Summer 1
* @Date: 14 06 2017
*/
import json
import os,sys
import pygame
import random 
import math

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__)) #current wrking directry

#####################################################################################
#####################################################################################

class Colors(object):
    """
    Opens a json file of web colors.
    """
    def __init__(self,file_name):
        
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_random_color(self):
        """
        Returns a random rgb tuple from the color dictionary
        Args:
            None
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            some_color = c.get_random_color()
            # some_color is now a tuple (r,g,b) representing some lucky color
        """
        r = random.randint(0,len(self.content)-1)
        c = self.content[r]
        return (c['rgb'][0],c['rgb'][1],c['rgb'][2])

    def get_rgb(self,name):
        """
        Returns a named rgb tuple from the color dictionary
        Args:
            name (string) : name of color to return
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            lavender = c.get_rgb('lavender')
            # lavender is now a tuple (230,230,250) representing that color
        """
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0],c['rgb'][1],c['rgb'][2])
        return None

    def __getitem__(self,color_name):
        """
        Overloads "[]" brackets for this class so we can treat it like a dict.
        Usage:
            c = Colors()
            current_color = c['violet']
            # current_color contains: (238,130,238)
        """
        return self.get_rgb(color_name)

#####################################################################################
#####################################################################################

class StateBorders(object):
    """
    Opens a json file of the united states borders for each state.
    """
    def __init__(self,file_name):
        """
        Args:
            filename (string) : The path and filename to open
        Returns:
            None
        """
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_state(self,name):
        """
        Returns a polygon of a single state from the US.
        Args:
            name (string): Name of a single state. 
        Returns:
            json (string object): Json representation of a state
        Usage:
            sb = StateBorders()
            texas = sb.get_state_polygon('texas')
            # texas is now a list object containing polygons
        """
        for s in self.content:
            if s['name'].lower() == name.lower() or s['code'].lower() == name.lower():
                t = []
                for poly in s['borders']:
                    np = []
                    for p in poly:
                        np.append((p[0],p[1]))
                    t.append(np)
                return(t)
                
        return None

    def get_continental_states(self):
        """
        Returns a list of all the continental us states as polygons.
        Args:
            None
        Returns:
            list (list object): list of Json objects representing each continental state.
        Usage:
            sb = StateBorders()
            states = sb.get_continental_states()
            # states is now a list object containing polygons for all the continental states
        """
        states = []
        for s in self.content:
            t = []
            if s['name'] not in ['Alaska','Hawaii']:
                for poly in s['borders']:
                    np = []
                    for p in poly:
                        np.append((p[0],p[1]))
                    t.append(np)
                states.append(t)
        return(states)

    def key_exists(self,key):
        """
        Returns boolean if key exists in json
        Args:
            key (string) : some identifier 
        Returns:
            T/F (bool) : True = Key exists
        """
        for s in self.content:
            if s['name'].lower() == key.lower():
                return True
            elif s['code'].lower() == key.lower():
                return True
        return False

#####################################################################################
#####################################################################################


class WorldCountries(object):
	"""
    Opens a json file of the united states borders for each state.
    """
	def __init__(self,file_name):
		with open(file_name, 'r') as content_file:
			content = content_file.read()

		self.content = json.loads(content)
		
	def get_all_countries(self):
		all_countries = []
		for c in self.content['features']:
			if c['id'] in ["ATA"]:
				continue
			all_countries.append(c['geometry']['coordinates'])
		return all_countries

	def get_country(self,id):
		"""
        Returns a list of one country.
        Args:
            None
        Returns:
            list (list object): List of Json object representing a country 
        Usage:
            wc = WorldCountries()
            country = wc.get_country('AFG')
            # country is now a list object containing polygons for 'Afghanistan'
        """
		country = []
		
		for c in self.content['features']:
			if c['id'].lower() == id.lower() or c['properties']['name'].lower() == id.lower():
				country.append(c['geometry']['coordinates'])
				gd.allinfo[id]=c['geometry']['coordinates']
		
		return country  

	def key_exists(self,key):
		"""
        Returns boolean if key exists in json
        Args:
            key (string) : some identifier 
        Returns:
            T/F (bool) : True = Key exists
        """
		for c in self.content['features']:
			if c['id'].lower() == key.lower():
				return True
			elif c['properties']['name'].lower() == key.lower():
				return True
		return False
			



class DrawGeoJson(object):
	__shared_state = {}        
	def __init__(self,screen,width,height):
		"""
        Converts lists (polygons) of lat/lon pairs into pixel coordinates in order to do some 
        simple drawing using pygame. 
        """
		self.__dict__ = self.__shared_state
		self.wc = WorldCountries(DIRPATH + '/countries.geo.json')

		self.screen = screen    # window handle for pygame drawing

		self.polygons = []      # list of lists (polygons) to be drawn

		self.all_lats = []      # list for all lats so we can find mins and max's
		self.all_lons = []
		self.allinfo={}
		self.mapWidth = width       # width of the map in pixels
		self.mapHeight = height     # height of the map in pixels
		self.mapLonLeft = -180.0    # extreme left longitude
		self.mapLonRight = 180.0    # extreme right longitude
		self.mapLonDelta = self.mapLonRight - self.mapLonLeft # difference in longitudes
		self.mapLatBottom = 0.0     # extreme bottom latitude
		self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0 # bottom in degrees
		
		self.colors = Colors(DIRPATH + '/colors.json')

	def convertGeoToPixel(self,lon, lat):
	
		"""
        Converts lat/lon to pixel within a set bounding box
        Args:
            lon (float): longitude
            lat (float): latitude
        Returns:
            point (tuple): x,y coords adjusted to fit on print window
        """
		x = (lon - self.mapLonLeft) * (self.mapWidth / self.mapLonDelta)

		lat = lat * math.pi / 180.0
		self.worldMapWidth = ((self.mapWidth / self.mapLonDelta) * 360) / (2 * math.pi)
		self.mapOffsetY = (self.worldMapWidth / 2 * math.log((1 + math.sin(self.mapLatBottomDegree)) / (1 - math.sin(self.mapLatBottomDegree))))
		y = self.mapHeight - ((self.worldMapWidth / 2 * math.log((1 + math.sin(lat)) / (1 - math.sin(lat)))) - self.mapOffsetY)

		return (x, y)


	def add_polygon(self,poly):
	
		"""
        Add a polygon to local collection to be drawn later
        Args:
            poly (list): list of lat/lons
        Returns:
            None
        """
	
		self.polygons.append(poly)
		for p in poly:
			x,y = p
			self.all_lons.append(x)
			self.all_lats.append(y)
		self.__update_bounds()

	def printpoly(self,pos):
		"""
		Add BORDER and RECTANGLE around the country and displays respective country NAME
		Args:
		pos (tuple): position where it is clicked
		Returns:
		None
		"""

		black = (0,0,0)
		red = (255,0,0)
		white = (255,255,255)
		lons=[]
		lats=[]
		totalinfo=[]
		allpolygons=[]

		for poly in self.polygons:
			adjusted = []
			for p in poly:
				x,y = p
				adjusted.append(self.convertGeoToPixel(x,y))
				
			result=self.point_inside_polygon(pos[0],pos[1],adjusted)
			print(result)

			if result == True:
				for i in adjusted:
					lons.append(i[0])
					lats.append(i[1])
					print(i)
				maxlon=max(lons)
				minlat=min(lats)
				maxlat=max(lats)
				minlon=min(lons)
				width=(maxlon-minlon)
				height=(maxlat-minlat)
				#maxlat=maxlat+10
				x=0
				y=0
				#pygame.draw.rect(screen, color, (x,y,width,height), thickness)
				
				pygame.draw.polygon(self.screen, black, adjusted, 6)
				pygame.draw.rect(self.screen, red, (minlon,minlat,int(width),int(height)),4)
				print(poly)
				for c in self.wc.content['features']:
					for i in c['geometry']['coordinates']:
						if type(i[0][0]) is float:
							if i == poly:
								print(c['properties']['name'])
								pygame.init() 
								myfont = pygame.font.SysFont("Ariel", 35)
								label = myfont.render(c['properties']['name'], 1, (0,0,255))
								screen.blit(label, (671, 96))
			else:
				del adjusted[:]


	def point_inside_polygon(self,x,y,poly):
    
		n = len(poly)
		inside =False

		p1x,p1y = poly[0]
		for i in range(n+1):
			p2x,p2y = poly[i % n]
			if y > min(p1y,p2y):
				if y <= max(p1y,p2y):
					if x <= max(p1x,p2x):
						if p1y != p2y:
							xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
						if p1x == p2x or x <= xinters:
							inside = not inside
			p1x,p1y = p2x,p2y

		return inside


	
	def draw_polygons(self):
		"""
        Draw our polygons to the screen
        Args:
            None
        Returns:
            None
        """ 
		black = (0,0,0)
		for poly in self.polygons:
			self.adjusted = []
			for p in poly:
				x,y = p
				self.adjusted.append(self.convertGeoToPixel(x,y))
			pygame.draw.polygon(self.screen, self.colors.get_random_color(), self.adjusted, 0)

	
			
	def __update_bounds(self):
		"""
        Updates the "extremes" of all the points added to be drawn so
        the conversion to x,y coords will be adjusted correctly to fit
        the "bounding box" surrounding all the points. Not perfect.
        Args:
            None
        Returns:
            None
        """  
	
		self.mapLonLeft = min(self.all_lons)
		self.mapLonRight = max(self.all_lons)
		self.mapLonDelta = self.mapLonRight - self.mapLonLeft  
		self.mapLatBottom = min(self.all_lats)
		self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0


	def __str__(self):
		return "[%d,%d,%d,%d,%d,%d,%d]" % (self.mapWidth,self.mapHeight,self.mapLonLeft,self.mapLonRight,self.mapLonDelta,self.mapLatBottom,self.mapLatBottomDegree)




class DrawingFacade(object):
	def __init__(self,width,height):
	    
		self.sb = StateBorders(DIRPATH + '/state_borders.json')
		self.wc = WorldCountries(DIRPATH + '/countries.geo.json')
		self.gd = DrawGeoJson(screen,width,height)

	def add_polygons(self,ids):
	    
		for id in ids:
			if self.wc.key_exists(id):
				self.__add_country(self.wc.get_country(id))
			elif self.sb.key_exists(id):
				self.__add_state(self.sb.get_state(id))         

	def __add_country(self,country):
		for polys in country:
			for poly in polys:
				if type(poly[0][0]) is float:
					gd.add_polygon(poly)
				else:
					for sub_poly in poly:
						self.gd.add_polygon(sub_poly)

	def __add_state(self,state):
		for poly in state:
			self.gd.add_polygon(poly)



	def point_inside_polygon(x,y,poly):
		"""
		determine if a point is inside a given polygon or not
		Polygon is a list of (x,y) pairs.
		http://www.ariel.com.au/a/python-point-int-poly.html
		"""
		n = len(poly)
		inside =False

		p1x,p1y = poly[0]
		for i in range(n+1):
			p2x,p2y = poly[i % n]
			if y > min(p1y,p2y):
				if y <= max(p1y,p2y):
			
					if x <= max(p1x,p2x):
						if p1y != p2y:
							xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
						if p1x == p2x or x <= xinters:
							inside = not inside
			p1x,p1y = p2x,p2y

		return inside

def mercator_projection(latlng,zoom=0,tile_size=256):
    x = (latlng[0] + 180) / 360 * tile_size
    y = ((1 - math.log(math.tan(latlng[1] * math.pi / 180) + 1 / math.cos(latlng[1] * math.pi / 180)) / math.pi) / 2 * pow(2, 0)) * tile_size
   
    return (x,y)

if __name__ == '__main__':

	if len(sys.argv) == 1:
		width = 1024   
		height = 512
	else:
		width = int(sys.argv[1])
		height = int(sys.argv[2])

		

	screen = pygame.display.set_mode((width, height)) 


	pygame.display.set_caption('Draw World Polygons')


	screen.fill((255,255,255))
	
	pygame.display.flip()
	

	gd = DrawGeoJson(screen,width,height)
	df = DrawingFacade(width,height)
	df.add_polygons(['Spain','Belgium','Iran','Ireland','Greenland','Germany','Egypt','Morocco','India'])

	running = True
	while running:
		gd.draw_polygons()       
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False			
			if event.type == pygame.MOUSEBUTTONDOWN:
				print(event.pos)
				gd.printpoly(event.pos)
				
			pygame.display.flip()
