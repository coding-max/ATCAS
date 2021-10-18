#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import copy
import numpy as np
from models.airport import Airport
from math import radians, cos, sin, asin, sqrt, pow, atan2, pi
from datetime import datetime

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
		if (len(self.path) == 1):
			self.manifesto = False
		else:
			self.manifesto = True
		self.current_path = 0

		#collisions information
		self.collision_l = []
		self.suggested_flightpath = []
		self.estimated_flightpath = []

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
		if (self.manifesto):
			self.current_path += 1
		else:
			self.create_estimated_flightpath()

	#Collisons needs at least the current position of the aircraft loaded into the path
	def collision(self, avion2):
		"""detects a colision between 2 aircrafts"""
		pos = 0
		Airport.map_collisions = []
		if (self.manifesto):
			path1 = self.path
			starting_point1 = self.current_path
		else:
			path1 = self.estimated_flightpath
			starting_point1 = 0
		if (avion2.manifesto):
			path2 = avion2.path
			starting_point2 = avion2.current_path
		else:
			path2 = avion2.estimated_flightpath
			starting_point2 = 0
		for element in path1[starting_point1:]:
			if (len(path2) <= (starting_point2 + pos)):
				break
			lat1 = radians(element["latitude"])
			lat2 = radians(path2[(starting_point2) + pos]["latitude"])
			lon1 = radians(element["longitude"])
			lon2 = radians(path2[(starting_point2) + pos]["longitude"])
			dlon = lon2 - lon1 
			dlat = lat2 - lat1 
			a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
			c = 2 * asin(sqrt(a)) 
			r = 6371
			horizontal_distance = c * r * 1000
			vertical_distance = (element["altitude"] - path2[(starting_point2) + pos]["altitude"])
			if (horizontal_distance < Aircraft.safety_horizontal) and (vertical_distance < Aircraft.safety_horizontal):
				dic = {
					"ID1": self.IATA,
					"ID2": avion2.IATA,
					"crash_time": element["time"], #needs to change to current time
					"crash_latitude": (element["latitude"] + (element["latitude"] - path2[(starting_point2)  + pos]["latitude"]) / 2),
					"crash_longitude": (element["longitude"] + (element["longitude"] - path2[(starting_point2) + pos]["longitude"]) / 2),
					"crash_altitude": (element["altitude"] + (element["altitude"] - path2[(starting_point2) + pos]["altitude"]) / 2),
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

	#To create an estimated flightpath, an initial path list with current location and time is needed
	def create_estimated_flightpath(self):
		"""Method that creates a preliminar route for a plane"""
		flightpath = []
		next_location = self.point_ahead(self.path[self.current_path]["latitude"],
										 self.path[self.current_path]["longitude"],
										 self.path[self.current_path]["truck"],
										 self.path[self.current_path]["speed"],
										 self.path[self.current_path]["time"],
										 self.path[self.current_path]["altitude"])
		#This while needs to be corrected to fit critera inside airspace
		while((next_location["latitude"] > -40.6) and (next_location["longitude"] > -60)):
			next_location = self.point_ahead(next_location["latitude"],
											 next_location["longitude"],
											 self.path[self.current_path]["truck"],
											 self.path[self.current_path]["speed"],
											 self.path[self.current_path]["time"],
											 self.path[self.current_path]["altitude"])
			flightpath.append(copy.deepcopy(next_location))
		self.estimated_flightpath = flightpath
		return flightpath

	def point_ahead(self, lat, lon, truck, speed, time, altitude):
		"""
			Given a start point, initial bearing, and distance,
			this will calculate the destina­tion point and final bearing
			travelling along a (shortest distance) great circle arc.
		"""
		#Earth radious
		r = 6371
		d = speed / 120

		#Calculation of point in radians
		final_lat = asin(sin(radians(lat)) * cos(d/r) + cos(radians(lat)) * sin(d/r) * cos(radians(truck)))
		final_long = radians(lon) + atan2(sin(radians(truck)) * sin(d/r) * cos(radians(lat)), cos(d/r) - sin(radians(lat)) * sin(final_lat))

		#Conversiion to decimal degrees
		final_lat = final_lat * 180 / pi
		final_long = final_long * 180 / pi

		#Load into dictionary for return
		final_point = {
			"latitude": final_lat,
			"longitude": final_long,
			"altitude": altitude,
			"speed": speed,
			"truck": truck,
			"time": time
		}
		return final_point
