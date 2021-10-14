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
		id_dick = {
			"ibe01",
			"pluna89"
		}

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
		""""
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

	def airport_query(self):
		"""
			Returns a dictionary contaiinitn all information regarding
			airports
        """
		thisdict = {
			"id": "MVD",
			"ICAO": "SUMU",
			"name": "Carrasco International Airport",
			"city": "Montevideo",
			"country": "Uruguay",
		}
		return thisdict

	def airport_departures(self):
		"""
			returns a dictionary containing all flight departuring from selected airport
		"""
		thisdict = {
			"5.35": "1",
			"5.45": "2",
			"5.55": "3",
			"6.35": "4",
			"6.45": "5",
			"6.45": "6",
		}
		return thisdict

	def airport_arrivals(self):
		"""
			returns a dictionary containing all flight arrivals from selected airport
		"""
		thisdict = {
			"5.35": "7",
			"5.45": "8",
			"5.55": "9",
			"6.35": "10",
			"6.45": "11",
			"6.45": "12",
		}
		return thisdict
