#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from math import cos
import json
import pymysql
import copy
import models.engine.db_querys as querys

class DBStorage:
	"""class to interact with database"""

	def __init__(self):
		"""instantiate a DBstorage object"""

	def all_ids(self):
		"""
			returns a list of all flight id's
		"""
		iata_list = []
		for iatas in querys.get_flights_ids():
			iata_list.append(iatas[0])
		return iata_list

	def aircraft_query_id(self, flight_id=None):
		"""
			aircraft, flight status, departure and arrivals query
			Makes query and returns a dictionary with all components
			from a specific flight (aircrafts, flightstatus, with departures
			and arrivals). If id is None, return a list of dictionaries with
			all fligths in the data base, with their repsective information
			ex: ["id": 7439395, "type": 747-800, etc...]
		"""
		flights = querys.get_flight(flight_id)
		current_location = {
		}
		flight = flights[0]
		aircraft_data = {
			"IATA": flight[0],
			"ICAO": flight[1],

			#Departure data
			"departure_IATA": flight[2],
			"departure_ICAO": flight[3],
			"departure_airport": flight[4],
			"departure_city": flight[5],
			"departure_country": flight[6],
			"departure_time": flight[7],
			"departure_latitude": flight[8],
			"departure_longitude": flight[9],

			#Arrival data
			"arrival_IATA": flight[10],
			"arrival_ICAO": flight[11],
			"arrival_airport": flight[12],
			"arrival_city": flight[13],
			"arrival_country": flight[14],
			"arrival_time": flight[15],
			"arrival_latitude": flight[16],
			"arrival_longitude": flight[17],

			#Aircaft data
			"registration": flight[18],
			"type": flight[19],
			"airline": flight[20],

			"current_location": current_location
		}
		return aircraft_data
	
	def aircraft_query_update(self, flight_id=None):
		"""
			query of all updated values, returns a dictionary
			with all the information
		"""

		#this is to taste collisions

		"""
		thisdict = {
			"latitude": int(69.69),
			"longitude": int(69.69),
			"altitude": int(6969),
			"speed": "6969",
			"truck": "6969",
			"time": "6969",
			"vertical_speed": "0",
		}
		lista_flightpath = [thisdict, thisdict, thisdict]"""

		lista_flightpath = querys.get_path(flight_id)["Path"]
		return lista_flightpath

	def airport_query(self, IATA):
		"""
			Returns a dictionary contaiinitn all information regarding
			airports
        """

		airports = querys.get_airport(IATA)
		airport = airports[0]
		airport_data = {
			"IATA": airport[0],
			"name": airport[1],
			"country": airport[2],
			"city": airport[3],
			"latitude": airport[4],
			"longitude":airport[5],
			"ICAO": airport[6]
		}
		return airport_data

	def airport_departures(self, IATA):
		"""
			returns a dictionary containing all flight departuring from selected airport
		"""
		departure_list = []
		departures = querys.get_departures(IATA)
		if departures:
			for departing in departures:
				departure_data = {
					"IATA" : departing[0],
					"time": departing[1]
				}
			departure_list.append(copy.deepcopy(departure_data))
		return departure_list

	def airport_arrivals(self, IATA=None):
		"""
			returns a dictionary containing all flight arrivals from selected airport
		"""
		arrival_list = []
		arrivals = querys.get_arrivals(IATA)
		if arrivals:
			for arriving in arrivals:
				arrival_data = {
					"IATA" : arriving[0],
					"time": arriving[1]
				}
			arrival_list.append(copy.deepcopy(arrival_data))
		return arrival_list
