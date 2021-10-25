#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import numpy as np
import json

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

	def add_plane(self, avion):
		"""adds plane to airspace"""
	
	def arrivals(self):
		"""returns all arrivals from this airport"""

	def departures(self):
		"""returns all departures from this airport"""

	def can_add(self, avion):
		"""checks if a plane can be added to airspace"""

	"""
	def desired_runway(self, avion):
		Chooses a runway for landing or takeoff based on destination and weather conditions
		weather_runway = "query result"
		weather_direction = "pal otro lado"
		if self.runway[weather_runway] == "enabled":
			avion.takeoff = weather_runway
			avion.takeoff_direction = weather_direction
			return weather_runway
		else:
			return weather_runway

	def dinamic_runway(self, avion):
		allows change of runway made
		avion.takeoff = avion.dinamic_takeoff
		avion.takeoff_direction = avion.dinamic_takeoff_direction 
		avion.path = avion.create_estimated_flightpath(9000)
		for crash in models.Aircraft.plane_list:
			avion.collision(crash)
	"""