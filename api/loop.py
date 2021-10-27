#!/usr/bin/python3
"""
This module contains all the endpoints of the RESTFUL API V1 of ATCAS web application,
which the web app frontend uses to load the processed data in backend
"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.airport import Airport
from models.aircraft import Aircraft

def recursiva():
    """recursiva"""
    ret = []
    for plane in Airport.airplane_list:
        if plane not in Airport.mapped_planes:
            avion = Aircraft(str(plane))
            Airport.mapped_planes.append(plane)
            avion.create_estimated_flightpath()
    print(Aircraft.plane_list)
    print(Aircraft.all_collision(Aircraft.plane_list))
    for avion in Aircraft.plane_list:
        avion.update()
        while (len(avion.estimated_flightpath) > 2):
            avion.estimated_flightpath.remove(avion.estimated_flightpath[1])
            avion.estimated_flightpath[1]["time"]
        while (len(avion.suggested_flightpath) > 2):
            avion.suggested_flightpath.remove(avion.suggested_flightpath[1])
    print(Airport.map_collisions)          
    for elem in Airport.map_collisions:
        #elem.crash_time.strftime()
        ret.append(elem)
    for avv in Aircraft.plane_list:
        avv.remove_datetime()
        ret.append(avv.to_dict())
    with open('IB420.json', 'w') as outfile:
        json.dump(ret, outfile)
    print("tuvieja")
    sleep(20)
    recursiva()

if __name__ == '__main__':
    recursiva()
