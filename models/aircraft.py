#!/usr/bin/python3
"""
Contains class BaseModel
"""

import models
import copy
from weakref import WeakSet
import numpy from np

class Aircraft(object):
	"Class model for all aircrafts"

	instances = WeakSet()
	instancecount = 0

	def __init__(self, args):

		aircraft_dict = models.storage.aircraft_query_id(args) #toaddid
		self.id = str(Aircraft.instancecount) #aircraft_dict["id"]
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


		self.coordiantesA = np.zeros((10,10,10))
		self.coordiantesB = np.zeros((10,10,10))
		
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
		"""detects a colision"""
		self.update()
		avion2.update()

		print("explota, todo")
