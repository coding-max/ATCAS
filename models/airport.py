#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import numpy as np


class Airport():
	def __init__(self, args):

		airport_dict = models.storage.airport_query()
		self.airspace = np.zeros((2,2,2), dtype=dict)
		self.id = airport_dict["id"]
		self.ICAO = airport_dict["ICAO"]
		self.name = airport_dict["name"]
		self.city = airport_dict["city"]
		self.country = airport_dict["country"]
		self.arrivals = models.storage.airport_arrivals()
		self.departure = models.storage.airport_departures()

		for x in range(0, 2):
			for y in range(0, 2):
				for z in range(0, 2):
					self.airspace[x, y, z] = {}

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
		chocaron = False
		for x in range(0, 2):
			for y in range(0, 2):
				for z in range(0, 2):
					self.airspace[x, y, z][avion.flightpath[x, y, z]] = avion.id

	def can_add(self, avion):
		add = True
		for x in range(0, 2):
			for y in range(0, 2):
				for z in range(0, 2):
					if avion.flightpath[x, y, z] in self.airspace[x, y, z]:
						print("Collision; time: {:}".format(avion.flightpath[x, y, z]), end="")
						print(", place: [{:}, {:}, {:}],".format(x, y, z), end="")
						print(" with {:}".format(self.airspace[x, y, z][avion.flightpath[x, y, z]]))
						"""print("Collision; time: {:}, place: [{:}, {:}, {:}], with: {:}".format(avion.flightpath[x, y, z], x, y, z, ), self.airspace[x, y, z][avion.flightpath[x, y, z]])"""
						add = False
		return add
		
