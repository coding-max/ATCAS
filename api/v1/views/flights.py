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


@app_views.route('/airport', methods=['GET'], strict_slashes=False)
def create_airport():
    """returns information about the current working airport"""
    airport = Airport("MVD").to_dict()
    airport = Aircraft.plane_list
    return jsonify(airport)


@app_views.route('/flights', methods=['GET'], strict_slashes=False)
def flights():
    """returns a json with information about all flights in the airspace"""
    ret = []
    for plane in Airport.airplane_list:
        if plane not in Airport.mapped_planes:
            avion = Aircraft(str(plane))
            Airport.mapped_planes.append(plane)
            avion.create_estimated_flightpath()
    for avion in Aircraft.plane_list:
        avion.update()
        while (len(avion.estimated_flightpath) > 2):
            avion.estimated_flightpath.remove(avion.estimated_flightpath[1])
    for avv in Aircraft.plane_list:
        ret.append(avv.to_dict())
    return jsonify(ret)


@app_views.route('/collitions', methods=['GET'], strict_slashes=False)
def collitions():
    """returns a json with data about all flights involved in a possible collision"""
    ret = []
    Aircraft.all_collision(Aircraft.plane_list)
    allcollision_list = Airport.map_collisions
    for elem in allcollision_list:
        ret.append(elem.to_dict())
    return jsonify(ret)


@app_views.route('/new_route', methods=['GET'], strict_slashes=False)
def new_route():
    """returns a suggested route for a flight involved in a possible collision"""
    ret = []
    for plane in Aircraft.plane_list:
        if len(plane.collision_l) != 0:
            plane.suggested_flightpath = plane.create_estimated_flightpath(-1000)
            for positions in plane.suggested_flightpath:
                ret.append(positions.__dict__())
    return jsonify(ret)


@app_views.route('/accept_new_path/<string:id>', methods=['POST'], strict_slashes=False)
def accept_new_path(id=None):
    """"accepts new route of changes"""
    if id is None:
        for avion in Aircraft.plane_list:
            if len(avion.suggested_flightpath) > 0:
                avion.switch_manifesto()
                avion.estimated_flightpath = avion.suggested_flightpath
                avion.suggested_flightpath = []
    else:
        for avion in Aircraft.plane_list:
            if str(avion.FlightID) == str(id):
                if len(avion.suggested_flightpath) > 0:
                    avion.switch_manifesto()
                    avion.estimated_flightpath = avion.suggested_flightpath
                    avion.suggested_flightpath = []
