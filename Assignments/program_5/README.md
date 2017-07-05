
## Name of the MongoDB is   :   world_data

## Collections:

      airports 
      earthquakes
      meteorites
      volcanos
      states


## Batch file : 
     load_mongo.sh is in geojson folder in program_5 floder  with all geojson files within the same folder.

## Example queries :

## Query1 : 
      python query1.py MCZ MNL 500
      python query1.py DFW BOM 500


## Query2 : 
      	python query2.py volcanos altitude 4000 min 0 1000		  
			
	 python query2.py earthquakes magnitude 8 max 5 1000		  	

	 python query2.py meteorites mass 1000 min 0 1000	

	 python query2.py 500

	 python query2.py 1000


## Query3 : 
      python query3.py volcanos 5 20
		
      python query3.py earthquakes 5 20
		 
		 

		 
