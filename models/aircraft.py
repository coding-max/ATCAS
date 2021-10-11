#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import copy
from weakref import WeakSet
import numpy as np

class Aircraft(object):
	"Class model for all aircrafts"

	instances = WeakSet()
	instancecount = 0

	def __init__(self, args):

		aircraft_dict = models.storage.aircraft_query_id(args) #toaddid
		self.id = str(args) #aircraft_dict["id"]
		self.type = aircraft_dict["type"]
		self.registration = aircraft_dict["registration"]
		self.airline = aircraft_dict["airline"]
		self.country = aircraft_dict["country"]
		self.ICAO = aircraft_dict["ICAO"]
		self.latitud = aircraft_dict["latitud"]
		self.longitud = aircraft_dict["longitud"]
		self.truck = aircraft_dict["truck"]
		self.speed = aircraft_dict["speed"]
		self.vertical_speed = aircraft_dict["vertical_speed"]
		self.departure_date = aircraft_dict["departure_date"]
		self.departure_time = aircraft_dict["departure_time"]
		self.arrival_date = aircraft_dict["arrival_date"]
		self.arrival_time = aircraft_dict["arrival_time"]

		self.flightpath = np.zeros((2,2,2), dtype=float)
		self.flightpath[0, 0, 0] = float(args)
		self.flightpath[0, 0, 1] = float(args)
		self.flightpath[0, 1, 0] = float(args)
		self.flightpath[0, 1, 1] = float(args)
		self.flightpath[1, 0, 0] = float(args)
		self.flightpath[1, 0, 1] = float(args)
		self.flightpath[1, 1, 0] = float(args)
		self.flightpath[1, 1, 1] = 5.35


		Aircraft.instancecount += 1
		Aircraft.instances.add(self)

	@classmethod
	def get_instances(cls):
		return list(Aircraft.instances)

	def __str__(self):
		"""String representation of the BaseModel class"""
		return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
										 self.__dict__)
 
	def aprint(self):
		print("id = {:}\ntype = {:}\nregistration = {:s}\nairline = {:s}\ncountry = {:s}\nICAO = {:s}\n".format(self.id, self.type, self.registration, self.airline, self.country, self.ICAO))

	def save(self):
		models.storage.save()

	def to_dict(self):
		"""returns a dictionary containing all keys/values of the instance"""
		new_dict = self.__dict__.copy()
		if "type" in new_dict:
			new_dict["type"] = new_dict["type"].strftime(time)
		if "registration" in new_dict:
			new_dict["registration"] = new_dict["registration"].strftime(time)
		new_dict["__class__"] = self.__class__.__name__
		return new_dict

	def update(self):
		"""update all information of aircraft"""
		aircraft_dict = models.storage.aircraft_query_update()
		self.latitud = aircraft_dict["latitud"]
		self.longitud = aircraft_dict["longitud"]
		self.truck = aircraft_dict["truck"]
		self.speed = aircraft_dict["speed"]
		self.vertical_speed = aircraft_dict["vertical_speed"]
		self.departure_date = aircraft_dict["departure_date"]
		self.departure_time = aircraft_dict["departure_time"]
		self.arrival_date = aircraft_dict["arrival_date"]
		self.arrival_time = aircraft_dict["arrival_time"]

	def collision(self, avion2):
		"""detects a colision between 2 aircrafts"""
		for x in range(0, 2):
			for y in range(0, 2):
				for z in range(0, 2):
					if self.flightpath[x, y, z] == avion2.flightpath[x, y, z]:
						print("collision between {:} and {:}".format(self.id, avion2.id), end="")
						print(" at {:}, on grid value [{:}, {:}]".format(self.flightpath[x, y, z], x, y, z))

	def all_collision(obj_list):
		"""checks collision between all aircrafts"""
		pos = 0
		for plane in obj_list:
			pos+=1
			for plane2 in obj_list[pos:]:
				plane.collision(plane2)







