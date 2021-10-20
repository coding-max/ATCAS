#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from math import cos
import json
import pymysql
import copy
import models.engine.db_queries as querys

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
			iata_list.append(iatas)
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
		flight = querys.get_flight(flight_id)
		aircraft_data = {
			"FlightID": flight[0],
			"IATA": flight[1],
			"ICAO": flight[2],

			#Aircaft data
			"type": flight[3],
			"registration": flight[4],
			"airline": flight[5],

			#Departure data
			"departure_IATA": flight[6],
			"departure_ICAO": flight[7],
			"departure_airport": flight[8],
			"departure_time": flight[9],

			#Arrival data
			"arrival_IATA": flight[10],
			"arrival_ICAO": flight[11],
			"arrival_airport": flight[12],
			"arrival_time": flight[13]
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
		lista_flightpath = [{
			"time": "2021-10-29t23:59:30z",
			"latitude": -30.540642,
			"longitude": -57.541443,
			"altitude": 37000,
			"truck": 437,
			"speed": 166,
		}]
		lista_flightpath = [querys.get_path(flight_id)]
		return lista_flightpath

	def airport_query(self, IATA):
		"""
			Returns a dictionary contaiinitn all information regarding
			airports
        """

		airport = querys.get_airport(IATA)
		airport_data = {
			"IATA": airport[0],
			"ICAO": airport[1],
			"name": airport[2],
		}
		return airport_data

	def airport_departures(self, FlightID):
		"""
			returns a dictionary containing all flight departuring from selected airport
		"""
		departure_list = []
		departures = querys.get_departures(FlightID)
		if departures:
			for departing in departures:
				departure_data = {
					"FlightID" : departing[0],
					"time": departing[1]
				}
			departure_list.append(copy.deepcopy(departure_data))
		return departure_list

	def airport_arrivals(self, FlightID=None):
		"""
			returns a dictionary containing all flight arrivals from selected airport
		"""
		arrival_list = []
		arrivals = querys.get_arrivals(FlightID)
		if arrivals:
			for arriving in arrivals:
				arrival_data = {
					"FlightID" : arriving[0],
					"time": arriving[1]
				}
			arrival_list.append(copy.deepcopy(arrival_data))
		return arrival_list
