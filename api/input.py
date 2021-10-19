#!/usr/bin/python3
"""
API input
"""

import json
import pymysql
import requests
import time
from datetime import datetime, timedelta
from models.engine import db_queries


with open('./config.json', 'r') as config_file:
    config = dict(json.load(config_file))
    #set api keys
    keys = config['api_keys']
    rapidapi_key = keys['rapidapi']
    aviationstack_key = keys['aviationstack']
    #set latitude and longitude
    positions = config['positions']
    latitude = positions['latitude']
    longitude = positions['longitude']


def run_radar():
    """ """
    pichu = 0
    while (1):
        if pichu < 10:
            print("-------------------------- [{}] --------------------------".format(pichu))
        else:
            print("-------------------------- [{}] -------------------------".format(pichu))
        pichu += 1
        get_flights()
        print("---------------------------------------------------------")
        time.sleep(15)
        print("\n")


def custom_time():
    time = (datetime.now() - timedelta(hours=3))
    time = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    seconds = int(time[17:-1])
    if (seconds >= 0 and seconds < 20):
        time = time[:16] + ':00Z'
    elif (seconds >= 20 and seconds < 40):
        time = time[:16] + ':20Z'
    else:
        time = time[:16] + ':40Z'
    return time


def get_flights():
    """returns basic data of flights 250NM around a given position"""

    url = "https://adsbexchange-com1.p.rapidapi.com/json/lat/{}/lon/{}/dist/250/".format(str(latitude), str(longitude))
    headers = {
        'x-rapidapi-host': "adsbexchange-com1.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
        }
    #make a request to get the flights on the radar and save the data in a list
    response = requests.request("GET", url, headers=headers)
    response = json.loads(response.text)
    detected_flights = []
    if response['ac'] is not None:
        print("Flights in the airspace:")
        for i in range(len(response['ac'])):
            data = []
            data.append(custom_time())
            data.append(response['ac'][i]['call'])
            data.append(response['ac'][i]['icao'])
            data.append(response['ac'][i]['reg'])
            data.append(response['ac'][i]['type'])
            data.append(response['ac'][i]['lat'])
            data.append(response['ac'][i]['lon'])
            data.append(response['ac'][i]['alt'])
            data.append(response['ac'][i]['trak'])
            data.append(response['ac'][i]['spd'])
            detected_flights.append(data)
    for flight in detected_flights:
        print(flight)
    #get the flights in the database
    known_flights = db_queries.get_flights_ids()
    print("---------------------------------------------------------")
    print("Flights in database:")
    print(known_flights)
    for flight in detected_flights:
        print("---------------------------------------------------------")
        if flight[2] not in known_flights:
            #add flight and related information to the database
            print("{} (ICAO: {}) not in ATCAS database, getting data...".format(flight[2], flight[1]))
            flight_data = []
            if flight[1] != '':
                flight_data = get_flight_data(flight[1])
            db_queries.add_flight_to_db(flight, flight_data)
        else:
            #update flightstatus in the database
            print("{} (ICAO: {}) in ATCAS database".format(flight[2], flight[1]))
            print("Last status: {}".format(db_queries.get_status(flight[2])))
            db_queries.update_status(flight)
            print("New status: {}".format(db_queries.get_status(flight[2])))


def get_flight_data(flight_id):
    """returns complete data of a given flight"""

    params = {
    'access_key': aviationstack_key,
    'flight_icao': flight_id
    }
    #make a request to get detailed information about a given flight and save the data in a list
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    api_response = api_result.json()
    flight_data = []
    if api_response['data'] != []:
        #the api returns useful information about the given flight
        print("IATA: {}".format(api_response['data'][0]['flight']['iata']))
        print("ICAO: {}".format(api_response['data'][0]['flight']['icao']))
        print("Airline: {}".format(api_response['data'][0]['airline']['name']))
        print("Departure:")
        print("    IATA: {}".format(api_response['data'][0]['departure']['iata']))
        print("    ICAO: {}".format(api_response['data'][0]['departure']['icao']))
        print("    Name: {}".format(api_response['data'][0]['departure']['airport']))
        print("    Time: {}".format(api_response['data'][0]['departure']['scheduled']))
        print("Arrival:")
        print("    IATA: {}".format(api_response['data'][0]['arrival']['iata']))
        print("    ICAO: {}".format(api_response['data'][0]['arrival']['icao']))
        print("    Name: {}".format(api_response['data'][0]['arrival']['airport']))
        print("    Time: {}".format(api_response['data'][0]['arrival']['scheduled']))
        flight_data.append(api_response['data'][0]['flight']['iata'])
        flight_data.append(api_response['data'][0]['flight']['icao'])
        flight_data.append(api_response['data'][0]['airline']['name'])
        flight_data.append(api_response['data'][0]['departure']['icao'])
        flight_data.append(api_response['data'][0]['departure']['iata'])
        flight_data.append(api_response['data'][0]['departure']['airport'])
        flight_data.append(api_response['data'][0]['departure']['scheduled'])
        flight_data.append(api_response['data'][0]['arrival']['icao'])
        flight_data.append(api_response['data'][0]['arrival']['iata'])
        flight_data.append(api_response['data'][0]['arrival']['airport'])
        flight_data.append(api_response['data'][0]['arrival']['scheduled'])
    else:
        #the api does not return information about the given flight
        print("no data was obtained")
    return (flight_data)


if __name__ == '__main__':
    run_radar()
