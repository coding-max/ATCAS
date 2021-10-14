# !/usr/bin/env python
import pymysql
import json

with open('config.json', 'r') as config:
    credentials = dict(json.load(config))["db_credentials"]
    host = credentials['host']
    user = credentials['user']
    password = credentials['password']
    database = credentials['database']


def get_flight(flight_id = None):
    """
    Make a query to the database to obtain the data of the flights in the airspace.
    If no parameter is passed, return the data of all the flights in the database.
    If the id (IATA code) of a flight is passed as a parameter, it returns all the data related to that specific flight.
    """
    connection = pymysql.connect(host, user, password, database)
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
        flights = cur.fetchall()
        print(flights)


if __name__ == '__main__':
    get_flight(input('file_name: '))
