#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models


class DBStorage:
	"""class to interact with database"""

	def __init__(self):
		"""instantiate a DBstorage object"""

	def aircraft_query_id(self, id=None):
		"""
			aircraft, flight status, departure and arrivals query
			Makes query and returns a dictionary with all components
			from a specific flight (aircrafts, flightstatus, with departures
			and arrivals). If id is None, return a list of dictionaries with
			all fligths in the data base, with their repsective information
			ex: ["id": 7439395, "type": 747-800, etc...]
		"""
		thisdict = {
			"id": "21312",
			"type": "747-800",
			"registration": "Cuba",
			"airline": "copailines",
			"country": "uruguay",
			"ICAO": "ICAO",
			"latitud": "54.56",
			"longitud": "58.69",
			"truck": "90",
			"speed": "144",
			"vertical_speed": "66",
			"departure_date": "hoy",
			"departure_time": "ocho y cuarto",
			"arrival_date": "ayer",
			"arrival_time": "69"
		}
		return thisdict

	def airport_query(self):
		"""
			Returns a dictionary contaiinitn all information regarding
			airports, with ids of all flights departuring and arriving
        """
