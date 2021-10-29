#!/usr/bin/python3
"""
Contains class Airacft
"""

import models


class Airport():
	airplane_list = models.storage.all_ids()
	map_collisions = []
	mapped_planes = []
	

	def __init__(self, args):
		"""firs load of the airport instance"""
		airport_dict = models.storage.airport_query(args)
		self.id = airport_dict["IATA"]
		self.ICAO = airport_dict["ICAO"]
		self.name = airport_dict["name"]
		self.arrivals = models.storage.airport_arrivals(args)
		self.departure = models.storage.airport_departures(args)
		#Enabled by default, can be disabled
		self.runways = {
			"06/24": "enabled", 
			"01/19": "enabled"
		}

	def reload(self):
		Airport.airplane_list = models.storage.all_ids()

	def __str__(self):
		"""String representation of the BaseModel class"""
		return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
										 self.__dict__)
 
	def to_dict(self):
		"""returns a dictionary containing all keys/values of the instance"""
		new_dict = self.__dict__.copy()
		if "type" in new_dict:
			new_dict["type"] = new_dict["type"].strftime(time)
		if "registration" in new_dict:
			new_dict["registration"] = new_dict["registration"].strftime(time)
		new_dict["__class__"] = self.__class__.__name__
		return new_dict
