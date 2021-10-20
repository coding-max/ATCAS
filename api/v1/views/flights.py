#!/usr/bin/python3
"""view for 'Flights'"""

import cmd
import json
import models
from models.aircraft import Aircraft
from models.airport import Airport
import math
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.aircraft import Aircraft
from models import storage


@app_views.route('/airport', methods=['GET'], strict_slashes=False)
def create_airport():
    """ #todo """
    airport = Airport("MVD").to_dict()
    airport = Aircraft.plane_list
    return jsonify(airport)

@app_views.route('/flights', methods=['GET'], strict_slashes=False)
def flights():
    """ prints all flight information based on ID's given"""
    ret = []
    for plane in Airport.airplane_list:
        if plane not in Airport.mapped_planes:
            avion = Aircraft(str(plane))
            Airport.mapped_planes.append(plane)
            #avion.create_estimated_flightpath()
    for avion in Aircraft.plane_list:
        avion.update()
        while (len(avion.estimated_flightpath) > 1):
            avion.estimated_flightpath.remove(avion.estimated_flightpath[0])
    #Aircraft.all_collision(Aircraft.plane_list)
    #Aircraft.all_collision(Aircraft.plane_list)
    for avv in Aircraft.plane_list:
        ret.append(avv.to_dict())
    return jsonify(ret)

@app_views.route('/collitions', methods=['GET'], strict_slashes=False)
def collitions():
    """ prints all flight information based on ID's given"""
    ret = []
    Aircraft.all_collision(Aircraft.plane_list)
    allcollision_list = Airport.map_collisions
    for elem in allcollision_list:
        ret.append(elem.to_dict())
    return jsonify(ret)


@app_views.route('/new_route', methods=['GET'], strict_slashes=False)
def new_route():
    """creates a plane based in its id, if id is none, create all planes"""
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
