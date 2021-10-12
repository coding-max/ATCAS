#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import copy
import numpy as np
from math import sqrt
from math import pow

class Aircraft(object):
	"Class model for all aircrafts"

	instancecount = 0
	plane_list = []
	safety_vertical = 304.8
	safety_horizontal = 4828.03
	refresh_rate = 2

	def __init__(self, args):
		"""method to assign all variables when creating an instance of Aircraft"""
		aircraft_dict = models.storage.aircraft_query_id(args) #toaddid
		self.id = str(args) #aircraft_dict["id"]
		self.type = aircraft_dict["type"]
		self.registration = aircraft_dict["registration"]
		self.airline = aircraft_dict["airline"]
		self.country = aircraft_dict["country"]
		self.ICAO = aircraft_dict["ICAO"]

		self.path = models.storage.aircraft_query_update(args)
		self.current_path = 0
		self.collision_l = []


		Aircraft.plane_list.append(self)
		Aircraft.instancecount += 1

	def __str__(self):
		"""String representation of the Aircraft class"""
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

	def update(self):
		"""update all information of aircraft"""
		aircraft_dict = models.storage.aircraft_query_update()
		self.path = aircraft_dict
		self.current_path += 1

	def collision(self, avion2):
		"""detects a colision between 2 aircrafts"""
		pos = 0
		collision_list = []
		for element in self.path[self.current_path:]:
			a = pow((element["latitud"] - avion2.path[(avion2.current_path) + pos]["latitud"]), 2)
			b = pow((element["longitud"] - avion2.path[(avion2.current_path) + pos]["longitud"]), 2)
			horizontal_distance = sqrt(a + b)
			vertical_distance = (element["altitude"] - avion2.path[(avion2.current_path) + pos]["altitude"])
			if (horizontal_distance < Aircraft.safety_horizontal) and (vertical_distance < Aircraft.safety_horizontal):
				dic = {
					"ID1": self.id,
					"ID2": avion2.id,
					"crash_time": element["departure_time"], #needs to change to current time
					"crash_latitude": (element["latitud"] + (element["latitud"] - avion2.path[(avion2.current_path)  + pos]["latitud"]) / 2),
					"crash_longitud": (element["longitud"] + (element["longitud"] - avion2.path[(avion2.current_path) + pos]["longitud"]) / 2),
					"crash_altitude": (element["altitude"] + (element["altitude"] - avion2.path[(avion2.current_path) + pos]["altitude"]) / 2),
					"crash_radious": horizontal_distance / 2
				}
				collision_list.append(dic)
			pos += 1
		self.collision_l = self.collision_l + collision_list
		avion2.collision_l = avion2.collision_l + copy.deepcopy(collision_list)
		return collision_list

	def all_collision(obj_list):
		"""checks collision between all aircrafts"""
		pos = 0
		total_collisions = []
		print
		for plane in obj_list:
			pos+=1
			for plane2 in obj_list[pos:]:
				total_collisions = total_collisions + plane.collision(plane2)
		return total_collisions


	def new_route(self):
		"""Preliminar suggestion of deviating route based on altitude"""
		descent_rate = 305 / Aircraft.refresh_rate
