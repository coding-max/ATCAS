# !/usr/bin/env python
"""
Database storage module, contains all queries to the database.
"""

import pymysql
import json

#todo -> change config file location and set relative path
with open('/home/ubuntu/atcas/ATCAS/models/engine/config.json', 'r') as config:
	credentials = dict(json.load(config))["db_credentials"]
	host = credentials['host']
	user = credentials['user']
	password = credentials['password']
	database = credentials['database']
	connection = pymysql.connect(host, user, password, database)


def get_flight(flight_id = None):
	"""
	Make a query to the database to obtain the data of the flights in the airspace.
	If no parameter is passed, returns the data of all the flights in the database.
	If the id (IATA code) of a flight is passed as a parameter, it returns all the data related to that specific flight.
	"""
	with connection:
		cur = connection.cursor()
		query = 'SELECT Flights.Id, Flights.ICAO,\
					Dep.Id, Dep.ICAO, Dep.Name, Dep.City, Dep.Country, Dep.Time, Dep.Latitude, Dep.Longitude,\
					Arr.Id, Arr.ICAO, Arr.Name, Arr.City, Arr.Country, Arr.Time, Arr.Latitude, Arr.Longitude,\
					Aircrafts.Id, Aircrafts.Type, Aircrafts.Airline\
				FROM Flights\
				JOIN (SELECT Departures.Id as depId, Departures.time , Airports.*\
					FROM Departures JOIN Airports ON Departures.AirportId = Airports.Id) as Dep\
					ON Flights.DepartureId = Dep.depId\
				JOIN (SELECT Arrivals.Id as arrId, Arrivals.time , Airports.*\
					FROM Arrivals JOIN Airports ON Arrivals.AirportId = Airports.Id) as Arr\
					ON Flights.ArrivalId = Arr.arrId\
				JOIN Aircrafts ON Aircrafts.Id = Flights.AircraftId'
		if (flight_id is None or flight_id == ''):
			cur.execute(query)
		else:
			cur.execute(query + ' WHERE Flights.Id = "{}"'.format(flight_id))
		return cur.fetchall()


def get_flights_ids():
	"""
	Make a query to the database to obtain the Id (IATA code) of the flights in the airspace
	Returns a list with IATA code of all flights in the airspace
	"""
	with connection:
		cur = connection.cursor()
		query = 'SELECT Id FROM Flights'
		cur.execute(query)
		return cur.fetchall()


def get_airport(IATA_code):
	"""
	Make a query to the database to obtain information about a given Airport
	Takes the ICAO code of the airport as a parameter and returns a list with information releated with that airport
	"""
	with connection:
		cur = connection.cursor()
		query = 'SELECT * FROM Airports WHERE Id = "{}"'.format(IATA_code)
		cur.execute(query)
		return cur.fetchall()


def get_departures(IATA_code):
	"""
	Make a query to the database to obtain information about departures for a given Airport
	Takes the ICAO code of the airport as a parameter and
	returns a list with information of all departures scheduled to that airport.
	"""
	with connection:
		cur = connection.cursor()
		query = 'SELECT Flights.Id, Departures.Time FROM Flights\
				 JOIN Departures ON Flights.DepartureId = Departures.Id\
				 WHERE Departures.AirportId = "{}"'.format(IATA_code)
		cur.execute(query)
		return cur.fetchall()


def get_arrivals(IATA_code):
	"""
	Make a query to the database to obtain information about arrivals for a given Airport
	Takes the ICAO code of the airport as a parameter and
	returns a list with information of all arrivals scheduled to that airport.
	"""
	with connection:
		cur = connection.cursor()
		query = 'SELECT Flights.Id, Arrivals.Time FROM Flights\
				 JOIN Arrivals ON Flights.ArrivalId = Arrivals.Id\
				 WHERE Arrivals.AirportId = "{}"'.format(IATA_code)
		cur.execute(query)
		return cur.fetchall()


#todo -> replace the way the flight path is loaded
#method used for development purposes
def get_path(flight_id=None):
	with open("/home/ubuntu/atcas/ATCAS/test_flights/{:}.json".format(flight_id), 'r') as f:
		return dict(json.load(f))
