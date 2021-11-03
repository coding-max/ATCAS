#!/usr/bin/python3
"""
This module contains all the endpoints of the RESTFUL API V1 of ATCAS web application,
which the web app frontend uses to load the processed data in backend
"""

from models.airport import Airport
from models.aircraft import Aircraft
import json
from time import sleep

def feeder():
    """function that creates teh new data and feeds it to webapp"""
    ret = []
    
    for plane in Airport.airplane_list:
        print(plane)
        if plane not in Airport.mapped_planes:
            Airport.mapped_planes.append(plane)
            avion = Aircraft(str(plane))
    for avion in Aircraft.plane_list:
        avion.create_estimated_flightpath()
        avion.update()
        avion.create_estimated_flightpath()
    Aircraft.all_collision(Aircraft.plane_list)
    for avion in Aircraft.plane_list:
        while (len(avion.estimated_flightpath) > 2):
            avion.estimated_flightpath.remove(avion.estimated_flightpath[1])
        while (len(avion.suggested_flightpath) > 2):
            avion.suggested_flightpath.remove(avion.suggested_flightpath[1])
    #for elem in Airport.map_collisions:
    ret.append(Airport.map_collisions)
    for avv in Aircraft.plane_list:
        ret.append(avv.to_dict())
    with open('./api/views/output.json', 'w') as outfile:
        json.dump(ret, outfile, default=str)
    print("**tick**")

if __name__ == '__main__':
    feeder()
