#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from math import cos

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
			"latitud": int(54.56),
			"longitud": int(58.69),
			"altitude": int(44390),
			"truck": "90",
			"speed": "144",
			"vertical_speed": "66",
			"departure_date": "hoy",
			"departure_time": "ocho y cuarto",
			"arrival_date": "ayer",
			"arrival_time": "69"
		}
		current_location["latitud"] = int(111320 * current_location["latitud"])
		current_location["longitud"] = int(40075000 * cos(current_location["longitud"]) / 360)
		current_location["altitude"] = int(0.3048 * current_location["altitude"])

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
		thisdict = {
			"latitud": int(69.69),
			"longitud": int(69.69),
			"altitude": int(6969),
			"truck": "6969",
			"speed": "6969",
			"vertical_speed": "6969",
			"departure_date": "6969",
			"departure_time": "6969",
			"arrival_date": "6969",
			"arrival_time": "6969"
		}
		lista_flightpath = [thisdict, thisdict, thisdict]
		for element in lista_flightpath:
			element["latitud"] = int(111320 * element["latitud"])
			element["longitud"] = int(40075000 * cos(element["longitud"]) / 360)
			element["altitude"] = int(0.3048 * element["altitude"])

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
