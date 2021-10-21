# !/usr/bin/env python
"""
Database storage module, contains all queries to the database.
"""

import pymysql
import json


def connect():
    """ """
    with open('././config.json', 'r') as config:
        credentials = dict(json.load(config))["db_credentials"]
        host = credentials['host']
        user = credentials['user']
        password = credentials['password']
        database = credentials['database']
        return pymysql.connect(host=host, user=user, password=password, database=database)


def get_flights_ids():
    """
    Make a query to the database to obtain the Id (IATA code) of the flights in the airspace
    Returns a list with IATA code of all flights in the airspace
    """
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Id FROM Flights'
        cur.execute(query)
        flights = cur.fetchall()
        print(flights)
        flights_list = []
        if len(flights) > 0:
            for flight in flights:
                flights_list.append(flight[0])
        print(flights_list)
        return flights_list


def get_flight(flight_id):
    """
    Make a query to the database to obtain the data of the flights in the airspace.
    If no parameter is passed, returns the data of all the flights in the database.
    If the id (IATA code) of a flight is passed as a parameter, it returns all the data related to that specific flight.
    """
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
    """
    """
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
    """
    Make a query to the database to obtain information about a given Airport
    Takes the ICAO code of the airport as a parameter and returns a list with information releated with that airport
    """
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT * FROM Airports WHERE IATA = "{}"'.format(IATA_code)
        cur.execute(query)
        return cur.fetchone()


def get_departures(IATA_code):
    """
    Make a query to the database to obtain information about departures for a given Airport
    Takes the ICAO code of the airport as a parameter and
    returns a list with information of all departures scheduled to that airport.
    """
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
    """
    Make a query to the database to obtain information about arrivals for a given Airport
    Takes the ICAO code of the airport as a parameter and
    returns a list with information of all arrivals scheduled to that airport.
    """
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
    """
    """
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Time, Latitude, Longitude, Altitude, Truck, Speed FROM FlightStatus WHERE Id = "{}"\
                    ORDER BY IndexId DESC LIMIT 1'.format(flight_id)
        cur.execute(query)
        status = cur.fetchone()
        return status


def get_status_list(flight_id):
    """
    """
    connection = connect()
    with connection:
        cur = connection.cursor()
        query = 'SELECT Time, Latitude, Longitude, Altitude, Truck, Speed FROM FlightStatus WHERE Id = "{}"'.format(flight_id)
        cur.execute(query)
        return cur.fetchall()


def add_flight_to_db(flight, flight_data):
    """
    Make a query to the database...
    """
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
    """
    Make a query to the database...
    """
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
    """
    Make a query to the database...
    """
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
    """
    Make a query to the database...
    """
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
    """
    Make a query to the database...
    """
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
    """
    Make a query to the database...
    """
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
    """
    Make a query to the database...
    """
    try:
        connection = connect()
        with connection.cursor() as cursor:
            query = 'INSERT INTO Arrivals (Id, AirportIATA, Time)\
                     VALUES ("{}", "{}", "{}")'.format(id, iata, time)
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)


def update_status(flight):
    """
    """
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


#todo -> replace the way the flight path is loaded
    #method used for development purposes
def get_path(flight_id=None):
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
