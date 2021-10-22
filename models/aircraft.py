#!/usr/bin/python3
"""
Contains class Airacft
"""

import models
import copy
import json
import numpy as np
from models.airport import Airport
from math import radians, cos, sin, asin, sqrt, pow, atan2, pi
from datetime import date, datetime, timedelta

class Aircraft(object):
	"Class model for all aircrafts"

	#class needed information
	instancecount = 0
	plane_list = []

	#default safety measures and rate of refresh of the data (amount of refresh's in a minute)
	safety_vertical = 1000
	safety_horizontal = 4828.03
	refresh_rate = 3
	descent_rate = 1000 / refresh_rate
	permited_altitudes = {
		"truck0": [2000, 3900, 5900, 7900,
				   9800, 11800, 13800, 15700,
				   17700, 19700, 21700, 23600,
				   25600, 28200, 31500, 34800,
				   38100, 43000, 49500],
				   #and evey 2000 meters after
		"truck1": [3000, 4900, 6900, 8900,
				   10800, 12800, 14800, 16700,
				   18700, 20700, 22600, 24600,
				   26600, 29900, 33100, 36400,
				   39700, 46300]
				   #and evey 2000 meters after
	}

	def __init__(self, args):
		"""method to assign all variables when creating an instance of Aircraft"""
		#Query for all data
		aircraft_data = models.storage.aircraft_query_id(args)
		self.FlightID = aircraft_data["FlightID"]
		self.IATA = aircraft_data["IATA"]
		self.ICAO = aircraft_data["ICAO"]

		#Load departure information
		self.departure_IATA = aircraft_data["departure_IATA"]
		self.departure_ICAO = aircraft_data["departure_ICAO"]
		self.departure_time = aircraft_data["departure_time"]
		self.departure_airport = aircraft_data["departure_airport"]

		#Load arrival information
		self.arrival_IATA = aircraft_data["arrival_IATA"]
		self.arrival_ICAO = aircraft_data["arrival_ICAO"]
		self.arrival_time = aircraft_data["arrival_time"]
		self.arrival_airport = aircraft_data["arrival_airport"]

		#load info regarding aircraft
		self.type = aircraft_data["type"]
		self.registration = aircraft_data["registration"]
		self.airline = aircraft_data["airline"]
		self.working_altitude = 0

		#Queries for dinamic information
		self.path = models.storage.aircraft_query_update(args)
		if (len(self.path) == 1):
			self.manifesto = False
		else:
			self.manifesto = True
		self.current_path = 0
		wpa = 0
		while (datetime.strptime(self.path[wpa]["time"], '%Y-%m-%dt%H:%M:%Sz') -
				datetime.now() > timedelta(0, 60 / Aircraft.refresh_rate)):
			try:
				self.path[self.current_path]["time"]
				self.status = "On air"
			except:
				self.status = "Outside Airspace"
				break
			wpa += 1
		self.status = "Outside Airspace"

		#collisions information
		self.collision_l = []
		self.suggested_flightpath = []
		self.estimated_flightpath = []

		#adds to list of instances
		Aircraft.plane_list.append(self)
		Aircraft.instancecount += 1


	def __str__(self):
		"""String representation of the Aircraft class"""
		return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.FlightID,
										 self.__dict__)

	def to_dict(self):
		"""returns a dictionary containing all keys/values of the instance"""
		new_dict = self.__dict__.copy()
		return new_dict

	def to_geojson(self):
		"""converts aircraft object to geojson serializable"""
		
		geojson = {
			"type": "FeatureCollection",
			"features": [
			{
				"type": "Feature",
				"geometry" : {
						"type": "Point",
						"coordinates": [self.path[0]["longitude"], self.path[0]["latitude"]],
				},
				"properties" : self.to_dict(),
			},
			{
				"type": "Feature",
				"geometry" : {
					"type": "Point",
					"coordinates": [self.estimated_flightpath[1]["longitude"], self.estimated_flightpath[1]["latitude"]],
				},
				"properties" : {},
			}
			]
		}
		return geojson

	def update(self):
		"""update all information of aircraft"""
		pos = 0
		if (self.manifesto):
			path1 = self.path
			self.current_path += 1
			starting_point1 = self.current_path
		else:
			path1 = self.estimated_flightpath
			starting_point1 = 0
		coso = path1[starting_point1]
		next_location = self.point_ahead(coso["latitude"], coso["longitude"], coso["truck"],
								 		 coso["speed"], coso["time"], coso["altitude"])
		if (((next_location["latitude"] > -35.15 and next_location["latitude"] < -34.65) and (next_location["longitude"] > -57.20 and next_location["longitude"] < -53.25))
			  or ((next_location["latitude"] > -34.65 and next_location["latitude"] < -34.25) and (next_location["longitude"] > -58.15 and next_location["longitude"] < -53.25))
			  or ((next_location["latitude"] > -34.25 and next_location["latitude"] < -33.05) and (next_location["longitude"] > -58.75 and next_location["longitude"] < -53.25))
			  or ((next_location["latitude"] > -33.05 and next_location["latitude"] < -31.40) and (next_location["longitude"] > -58.50 and next_location["longitude"] < -54.30))
			  or ((next_location["latitude"] > -33.05 and next_location["latitude"] < -32.50) and (next_location["longitude"] > -54.30 and next_location["longitude"] < -52.95))
			  or ((next_location["latitude"] > -32.50 and next_location["latitude"] < -31.75) and (next_location["longitude"] > -54.30 and next_location["longitude"] < -53.50))
			  or ((next_location["latitude"] > -31.40 and next_location["latitude"] < -30.00) and (next_location["longitude"] > -58.15 and next_location["longitude"] < -56.00))
			  or ((next_location["latitude"] > -31.40 and next_location["latitude"] < -30.75) and (next_location["longitude"] > -56.00 and next_location["longitude"] < -54.80))):
			self.create_estimated_flightpath()
			if (path1[starting_point1]["truck"] > 180):
				side = "truck0"
			else:
				side = "truck1"
			for elem in Aircraft.permited_altitudes[side]:
				if (abs(elem - path1[starting_point1]["altitude"]) < 500):
					self.working_altitude = pos
					break
				pos += 1
			self.path = models.storage.aircraft_query_update(self.FlightID)
			return 1
		else:
			Airport.mapped_planes.remove(self.FlightID)
			Aircraft.plane_list.remove(self)
			return 0

	#Collisons needs at least the current position of the aircraft loaded into the path
	def collision(self, avion2):
		"""detects a colision between 2 aircrafts"""
		pos = 0
		if (self.status == "Landed" or avion2.status == "Landed"):
			return Airport.map_collisions
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
			vertical_distance = abs(element["altitude"] - path2[(starting_point2) + pos]["altitude"])
			print(vertical_distance)
			print(horizontal_distance)
			if (horizontal_distance < Aircraft.safety_horizontal) and (vertical_distance < Aircraft.safety_horizontal):
				dic = {
					"ID1": self.FlightID,
					"ID2": avion2.FlightID,
					"crash_time": element["time"], #needs to change to current time
					"crash_latitude": (element["latitude"] + (element["latitude"] - path2[(starting_point2)  + pos]["latitude"]) / 2),
					"crash_longitude": (element["longitude"] + (element["longitude"] - path2[(starting_point2) + pos]["longitude"]) / 2),
					"crash_altitude": (element["altitude"] + (element["altitude"] - path2[(starting_point2) + pos]["altitude"]) / 2),
					"crash_radious": horizontal_distance / 2,
					"crash_id": self.FlightID + avion2.FlightID + element["time"],
					"crash_id2": avion2.FlightID + self.FlightID + element["time"]
				}
				flag = 0
				for elements in Airport.map_collisions:
					if (dic["crash_id"] == elements["crash_id"]) or (dic["crash_id2"] == elements["crash_id"]):
						flag = 1
						break
				if flag == 0:
					Airport.map_collisions.append(copy.deepcopy(dic))
					self.collision_l.append(copy.deepcopy(dic))
					avion2.collision_l.append(copy.deepcopy(dic))
					self.new_route()
			pos += 1
		return self.collision_l

	def all_collision(obj_list):
		"""checks collision between all aircrafts"""
		pos = 0
		Airport.map_collisions = []
		for plane in obj_list:
			pos+=1
			for plane2 in obj_list[pos:]:
				plane.collision(plane2)
		return Airport.map_collisions

	def new_route(self, target=None):
		"""Preliminar suggestion of deviating route based on altitude"""
		self.suggested_flightpath = self.create_estimated_flightpath(-2000)
		#self.collision(target)
		
	#To create an estimated flightpath, an initial path list with current location and time is needed
	def create_estimated_flightpath(self, altitude_to_descend=0):
		"""Method that creates a preliminar route for a plane"""
		flightpath = []
		current_time = datetime.strptime(self.path[self.current_path]["time"], '%Y-%m-%dt%H:%M:%Sz')
		current_time = current_time + timedelta(0, 60 / Aircraft.refresh_rate)
		if altitude_to_descend == 0:
			delta_altitude = 0
		else:
			if altitude_to_descend > 0:
				delta_altitude = 1000 / Aircraft.refresh_rate
			else:
				delta_altitude = -1000 / Aircraft.refresh_rate

		altitude_to_descend -= delta_altitude
		next_location = self.point_ahead(self.path[self.current_path]["latitude"],
										 self.path[self.current_path]["longitude"],
										 self.path[self.current_path]["truck"],
										 self.path[self.current_path]["speed"],
										 current_time.strftime('%Y-%m-%dt%H:%M:%Sz'),
										 self.path[self.current_path]["altitude"] + delta_altitude)
		flightpath.append(copy.deepcopy(next_location))
		#This while needs to be corrected to fit critera inside airspace
		while(((next_location["latitude"] > -35.15 and next_location["latitude"] < -34.65) and (next_location["longitude"] > -57.20 and next_location["longitude"] < -53.25))
				or ((next_location["latitude"] > -34.65 and next_location["latitude"] < -34.25) and (next_location["longitude"] > -58.15 and next_location["longitude"] < -53.25))
				or ((next_location["latitude"] > -34.25 and next_location["latitude"] < -33.05) and (next_location["longitude"] > -58.75 and next_location["longitude"] < -53.25))
				or ((next_location["latitude"] > -33.05 and next_location["latitude"] < -31.40) and (next_location["longitude"] > -58.50 and next_location["longitude"] < -54.30))
				or ((next_location["latitude"] > -33.05 and next_location["latitude"] < -32.50) and (next_location["longitude"] > -54.30 and next_location["longitude"] < -52.95))
				or ((next_location["latitude"] > -32.50 and next_location["latitude"] < -31.75) and (next_location["longitude"] > -54.30 and next_location["longitude"] < -53.50))
				or ((next_location["latitude"] > -31.40 and next_location["latitude"] < -30.00) and (next_location["longitude"] > -58.15 and next_location["longitude"] < -56.00))
				or ((next_location["latitude"] > -31.40 and next_location["latitude"] < -30.75) and (next_location["longitude"] > -56.00 and next_location["longitude"] < -54.80))):

			if (altitude_to_descend > -500) and (altitude_to_descend < 500):
				delta_altitude = altitude_to_descend
			else:
				altitude_to_descend -= delta_altitude
			current_time = current_time + timedelta(0, 60 / Aircraft.refresh_rate)
			next_location = self.point_ahead(next_location["latitude"],
											 next_location["longitude"],
											 self.path[self.current_path]["truck"],
											 self.path[self.current_path]["speed"],
											 current_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
											 next_location["altitude"] + delta_altitude)
			flightpath.append(copy.deepcopy(next_location))
		self.estimated_flightpath = flightpath
		return flightpath

	def switch_manifesto(self):
		"""switches between manifestos"""
		#self.manifesto = False

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

	def accept_route(self):
		"""accepts routes and deploys thems to testing jsons"""
		self.suggested_flightpath = self.create_estimated_flightpath(-1000)
		data = json.dumps(self.suggested_flightpath)
		with open("{:}.json".format(self.FlightID), "w") as f:
			json.dump(data, f)
