#!/usr/bin/python3
"""
This module contains all the endpoints of the RESTFUL API V1 of ATCAS web application,
which the web app frontend uses to load the processed data in backend
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.airport import Airport
from models.aircraft import Aircraft
import json


@app_views.route('/airport', methods=['GET'], strict_slashes=False)
def create_airport():
    """returns information about the current working airport"""
    airport = Airport("MVD").to_dict()
    #airport = Aircraft.plane_list
    return jsonify(airport)


@app_views.route('/flights', methods=['GET'], strict_slashes=False)
def flights():
    """returns a json with information about all flights in the airspace"""
    """ret = []
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
        while (len(avion.suggested_flightpath) > 2):
            avion.suggested_flightpath.remove(avion.suggested_flightpath[1])
    print(Airport.map_collisions)          
    for elem in Airport.map_collisions:
        ret.append(elem)
    for avv in Aircraft.plane_list:
        ret.append(avv.to_dict())
    return jsonify(ret)"""
    with open("wopa.json", 'r') as f:
        stat = json.load(f)
    return jsonify(stat)
