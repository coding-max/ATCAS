#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from math import cos
import json

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

	def aircraft_query_id(self, id=None):
		"""
			aircraft, flight status, departure and arrivals query
			Makes query and returns a dictionary with all components
			from a specific flight (aircrafts, flightstatus, with departures
			and arrivals). If id is None, return a list of dictionaries with
			all fligths in the data base, with their repsective information
			ex: ["id": 7439395, "type": 747-800, etc...]
		"""
		current_location = {
		}

		thisdict = {
			"id": "21312",
			"type": "747-800",
			"registration": "Cuba",
			"airline": "copailines",
			"country": "uruguay",
			"current_location": current_location,
			"ICAO": "ICAO"
		}
		return thisdict
	
	def aircraft_query_update(self, id=None):
		"""
			query of all updated values, returns a dictionary
			with all the information
		"""
		with open("/home/ubuntu/atcas/ATCAS/test_flights/{:}.json".format(id), 'r') as f:
			dic_load = dict(json.load(f))
			listaaaa = dic_load["Path"]
		lista_flightpath = dic_load["Path"]
		"""
		for element in lista_flightpath:
			element["latitud"] = float(111320 * element["latitud"])
			element["longitud"] = (element["longitud"] * (float(111319.444 * cos(element["longitud"]))
			element["altitude"] = float(0.3048 * element["altitude"])
		"""
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
