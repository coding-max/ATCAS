#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import copy
import numpy as np
from models.airport import Airport
from math import radians, cos, sin, asin, sqrt, pow

class Aircraft(object):
	"Class model for all aircrafts"

	#class needed information
	instancecount = 0
	plane_list = []

	#default safety measures and rate of refresh of the data (amount of refresh's in a minute)
	safety_vertical = 304.8
	safety_horizontal = 4828.03
	refresh_rate = 2
	descent_rate = 305 / refresh_rate

	def __init__(self, args):
		"""method to assign all variables when creating an instance of Aircraft"""
		#Query for all data
		aircraft_data = models.storage.aircraft_query_id(args)
		self.IATA = aircraft_data["IATA"]
		self.ICAO = aircraft_data["ICAO"]

		#Load departure information
		self.departure_IATA = aircraft_data["departure_IATA"]
		self.departure_ICAO = aircraft_data["departure_ICAO"]
		self.departure_airport = aircraft_data["departure_airport"]
		self.departure_city = aircraft_data["departure_city"]
		self.departure_country = aircraft_data["departure_country"]
		self.departure_time = aircraft_data["departure_time"]
		self.departure_latitude = aircraft_data["departure_latitude"]
		self.departure_longitude = aircraft_data["departure_longitude"]

		#Load arrival information
		self.arrival_IATA = aircraft_data["arrival_IATA"]
		self.arrival_ICAO = aircraft_data["arrival_ICAO"]
		self.arrival_airport = aircraft_data["arrival_airport"]
		self.arrival_city = aircraft_data["arrival_city"]
		self.arrival_country = aircraft_data["arrival_country"]
		self.arrival_time = aircraft_data["arrival_time"]
		self.arrival_latitude = aircraft_data["arrival_latitude"]
		self.arrival_longitude = aircraft_data["arrival_longitude"]

		#load info regarding aircraft
		self.registration = aircraft_data["registration"]
		self.type = aircraft_data["type"]
		self.airline = aircraft_data["airline"]

		#Queries for dinamic information
		self.path = models.storage.aircraft_query_update(args)
		self.current_path = 0

		#collisions information
		self.collision_l = []
		self.newpath = []

		#adds to list of instances
		Aircraft.plane_list.append(self)
		Aircraft.instancecount += 1

	def __str__(self):
		"""String representation of the Aircraft class"""
		return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.IATA,
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
		aircraft_data = models.storage.aircraft_query_update()
		self.path = aircraft_data
		self.current_path += 1

	#still need to fix when the length of one of the lists is longer, and fails on index´s
	def collision(self, avion2):
		"""detects a colision between 2 aircrafts"""
		pos = 0
		Airport.map_collisions = []
		for element in self.path[self.current_path:]:
			if (avion2.path[(avion2.current_path) + pos] is None):
				break
			lat1 = radians(element["latitude"])
			lat2 = radians(avion2.path[(avion2.current_path) + pos]["latitude"])
			lon1 = radians(element["longitude"])
			lon2 = radians(avion2.path[(avion2.current_path) + pos]["longitude"])
			dlon = lon2 - lon1 
			dlat = lat2 - lat1 
			a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
			c = 2 * asin(sqrt(a)) 
			r = 6371
			horizontal_distance = c * r * 1000
			vertical_distance = (element["altitude"] - avion2.path[(avion2.current_path) + pos]["altitude"])
			if (horizontal_distance < Aircraft.safety_horizontal) and (vertical_distance < Aircraft.safety_horizontal):
				dic = {
					"ID1": self.IATA,
					"ID2": avion2.IATA,
					"crash_time": element["time"], #needs to change to current time
					"crash_latitude": (element["latitude"] + (element["latitude"] - avion2.path[(avion2.current_path)  + pos]["latitude"]) / 2),
					"crash_longitude": (element["longitude"] + (element["longitude"] - avion2.path[(avion2.current_path) + pos]["longitude"]) / 2),
					"crash_altitude": (element["altitude"] + (element["altitude"] - avion2.path[(avion2.current_path) + pos]["altitude"]) / 2),
					"crash_radious": horizontal_distance / 2
				}
				if dic not in Airport.map_collisions:
					Airport.map_collisions.append(dic)
				if dic not in self.collision_l:
					self.collision_l.append(dic)
				if dic not in avion2.collision_l:
					avion2.collision_l.append(dic)
			pos += 1

		return Airport.map_collisions

	def all_collision(obj_list):
		"""checks collision between all aircrafts"""
		pos = 0
		total_collisions = []
		for plane in obj_list:
			pos+=1
			for plane2 in obj_list[pos:]:
				total_collisions = total_collisions + plane.collision(plane2)
		return total_collisions

	def new_route(plane1, plane2):
		"""Preliminar suggestion of deviating route based on altitude"""
		route_for1 = {

		}

		route_for2 = {
			
		}


