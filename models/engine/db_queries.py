# !/usr/bin/env python
"""
This module contains all the queries that interact (read and write) with the ATCAS database.
"""

import pymysql
import json


def connect():
    """Load credentials from 'config.json' file to make the connection to the database"""
    with open('././config.json', 'r') as config:
        credentials = dict(json.load(config))["db_credentials"]
        host = credentials['host']
        user = credentials['user']
        password = credentials['password']
        database = credentials['database']
        return pymysql.connect(host=host, user=user, password=password, database=database)


def get_user(usr, pwd):
    """Returns a list that contains the IDs of all flights in the database"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT FirstName, LastName FROM Users WHERE User="{}" AND Password="{}"'.format(usr, pwd)
        cur.execute(query)
        return cur.fetchone()


def get_flights_ids():
    """Returns a list that contains the IDs of all flights in the database"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Id FROM Flights'
        cur.execute(query)
        flights = cur.fetchall()
        flights_list = []
        if len(flights) > 0:
            for flight in flights:
                flights_list.append(flight[0])
        return flights_list


def get_flight(flight_id):
    """Returns a tuple that contains all the information related to the flight ID passed as a parameter"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Flights.Id, Flights.IATA, Flights.ICAO,\
                 Aircrafts.Type, Aircrafts.Registration, Aircrafts.Airline,\
                 Dep.IATA, Dep.ICAO, Dep.Name, Dep.Time,\
                 Arr.IATA, Arr.ICAO, Arr.Name, Arr.Time\
                 FROM Flights\
                 JOIN Aircrafts ON Aircrafts.Id = Flights.Id\
                 JOIN (SELECT Id, IATA, ICAO, Name, Dep.Time FROM Airports JOIN Departures as Dep ON Dep.AirportIATA = Airports.IATA) as Dep ON Dep.Id = Flights.Id\
                 JOIN (SELECT Id, IATA, ICAO, Name, Arr.Time FROM Airports JOIN Arrivals as Arr ON Arr.AirportIATA = Airports.IATA) as Arr ON Arr.Id = Flights.Id\
                 WHERE Flights.Id = "{}"'.format(flight_id)
        cur.execute(query)
        return cur.fetchone()


def get_airports():
    """Returns a list that contains the IATA codes of all airports in the database"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT IATA FROM Airports'
        cur.execute(query)
        airports = cur.fetchall()
        airports_list = []
        if len(airports) > 0:
            for airport in airports:
                airports_list.append(airport[0])
        return airports_list


def get_airport(IATA_code):
    """Returns a tuple that contains all the information related to a given airport,
       It is required to pass the airport's IATA code as a parameter"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT * FROM Airports WHERE IATA = "{}"'.format(IATA_code)
        cur.execute(query)
        return cur.fetchone()


def get_departures(IATA_code):
    """Returns a tuple that contains all scheduled departures from a given airport,
       It is required to pass the airport's IATA code as a parameter""" 
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Flights.Id, Departures.Time FROM Flights\
                 JOIN Departures ON Departures.Id = Flights.Id\
                 JOIN Airports ON Airports.IATA = Departures.AirportIATA\
                 WHERE Departures.AirportIATA = "{}"'.format(IATA_code)
        cur.execute(query)
        return cur.fetchall()


def get_arrivals(IATA_code):
    """Returns a tuple that contains all scheduled arrivals from a given airport,
       It is required to pass the airport's IATA code as a parameter""" 
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Flights.Id, Arrivals.Time FROM Flights\
                 JOIN Arrivals ON Arrivals.Id = Flights.Id\
                 JOIN Airports ON Airports.IATA = Arrivals.AirportIATA\
                 WHERE Arrivals.AirportIATA = "{}"'.format(IATA_code)
        cur.execute(query)
        return cur.fetchall()


def get_status(flight_id):
    """Returns the most recent position information for a given flight,
       It is required to pass the flight ID as a parameter"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Time, Latitude, Longitude, Altitude, Truck, Speed FROM FlightStatus WHERE Id = "{}"\
                 ORDER BY IndexId DESC LIMIT 1'.format(flight_id)
        cur.execute(query)
        status = cur.fetchone()
        return status


def get_status_list(flight_id):
    """Returns all position history for a given flight,
       It is required to pass the flight ID as a parameter"""
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Time, Latitude, Longitude, Altitude, Truck, Speed FROM FlightStatus WHERE Id = "{}"'.format(flight_id)
        cur.execute(query)
        return cur.fetchall()


def add_flight_to_db(flight, flight_data):
    """Add a flight to the database,
       It consists of adding all the information collected from both APIs"""
    id = flight[2]
    lat = flight[5]
    if lat == '':
        lat = -1
    lon = flight[6]
    if lon == '':
        lon = -1
    alt = flight[7]
    if alt == '':
        alt = -1
    trk = flight[8]
    if trk == '':
        trk = -1
    spd = flight[9]
    if spd == '':
        spd = -1
    reg = flight[3]
    type = flight[4]
    time = flight[0]
    if flight_data != []:
        iata = flight_data[0]
        icao = flight_data[1]
        airline = flight_data[2]
        dep_icao = flight_data[3]
        dep_iata = flight_data[4]
        dep_name = flight_data[5]
        dep_time = flight_data[6]
        arr_icao = flight_data[7]
        arr_iata = flight_data[8]
        arr_name = flight_data[9]
        arr_time = flight_data[10]
    else:
        iata = ""
        icao = flight[1]
        airline = ""
        dep_iata = dep_icao = dep_name = dep_time = ""
        arr_iata = arr_icao = arr_name = arr_time = ""
    insert_flights(id, iata, icao)
    insert_flightstatus(id, lat, lon, alt, trk, spd, time)
    insert_aircraft(id, type, reg, airline)
    airports = get_airports()
    if dep_iata not in airports and dep_iata != '':
        insert_airport(dep_iata, dep_icao, dep_name)
    if arr_iata not in airports and arr_iata != '':
        insert_airport(arr_iata, arr_icao, arr_name)
    insert_departure(id, dep_iata, dep_time)
    insert_arrival(id, arr_iata, arr_time)
    print("Flight added to the ATCAS database")


def insert_flights(id, iata, icao):
    """Adds a new row to the database's 'Flights' table
       where is stored the data that identifies the flight.
       The flight's ID, ICAO and IATA code are required,
       <id> must be non-empty string, <iata> and <icao> can be empty strings"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO Flights (Id, IATA, ICAO)\
                     VALUES ("{}", "{}", "{}")'.format(id, iata, icao)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def insert_flightstatus(id, lat, lon, alt, trk, spd, time):
    """Adds a new row to the database's 'FlightStatus' table
       where is stored flight's position information"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO FlightStatus (Id, Latitude, Longitude, Altitude, Truck, Speed, Time)\
                        VALUES ("{}", {}, {}, {}, {}, {}, "{}")'.format(id, lat, lon, alt, trk, spd, time)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def insert_aircraft(id, type, reg, airline):
    """Adds a new row to the database's 'Aircrafts' table
       where is stored flight's aircraft information"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO Aircrafts (Id, Type, Registration, Airline)\
                     VALUES ("{}", "{}", "{}", "{}")'.format(id, type, reg, airline)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def insert_airport(iata, icao, name):
    """Adds a new row to the database's 'Airports' table
       where is stored the airport's identification data"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO Airports (IATA, ICAO, Name)\
                     VALUES ("{}", "{}", "{}")'.format(iata, icao, name)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def insert_departure(id, iata, time):
    """Adds a new row to the database's 'Departures' table
       where is stored the flight's departures data"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO Departures (Id, AirportIATA, Time)\
                     VALUES ("{}", "{}", "{}")'.format(id, iata, time)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def insert_arrival(id, iata, time):
    """Adds a new row to the database's 'Departures' table
       where is stored the flight's arrivals data"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO Arrivals (Id, AirportIATA, Time)\
                     VALUES ("{}", "{}", "{}")'.format(id, iata, time)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def remove_flight(id):
    """Removes a Flight from the database"""
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'DELETE FROM Flights WHERE Id = "{}"'.format(id)
            cursor.execute(query)
            query = 'DELETE FROM FlightStatus WHERE Id = "{}"'.format(id)
            cursor.execute(query)
            query = 'DELETE FROM Departures WHERE Id = "{}"'.format(id)
            cursor.execute(query)
            query = 'DELETE FROM Arrivals WHERE Id = "{}"'.format(id)
            cursor.execute(query)
            query = 'DELETE FROM Aircrafts WHERE Id = "{}"'.format(id)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


#todo: this function is obsolete, it performs the same function as "insert_flightstatus". Remove the calls to this function and replace them with a call to "insert_flightstatus".
def update_status(flight):
    """Adds a new row to the database's 'FlightStatus' table
       where is stored flight's position information"""
    for i in range(5, 9):
        if flight[i] == '':
            flight[i] = -1
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO FlightStatus (Id, Latitude, Longitude, Altitude, Truck, Speed, Time)\
                     VALUES ("{}", {}, {}, {}, {}, {}, "{}")'.format(flight[2], flight[5], flight[6], flight[7], flight[8], flight[9], flight[0])
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def get_path(flight_id):
    try:
        with open("././test_flights/{:}.json".format(flight_id), 'r') as f:
            return dict(json.load(f))
    except:
        status_list = get_status(flight_id)
        dictionary = {
                    "time": status_list[0],
                    "latitude": status_list[1],
                    "longitude": status_list[2],
                    "altitude": status_list[3],
                    "truck": status_list[4],
                    "speed": status_list[5],
        }
        return dictionary
